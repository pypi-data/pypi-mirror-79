# Code dedicated to the cache of 'max(merge()) and ::X'
#
# These stable ranges are use for obsolescence markers discovery
#
# Copyright 2017 Pierre-Yves David <pierre-yves.david@ens-lyon.org>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from __future__ import absolute_import

import array

from mercurial import (
    localrepo,
    node as nodemod,
)

from mercurial.utils.stringutil import forcebytestr

from . import (
    compat,
    error,
    exthelper,
    genericcaches,
    utility,
)

filterparents = utility.filterparents

eh = exthelper.exthelper()

@eh.reposetup
def setupcache(ui, repo):

    class firstmergecacherepo(repo.__class__):

        @localrepo.unfilteredpropertycache
        def firstmergecache(self):
            cache = firstmergecache()
            cache.update(self)
            return cache

        @localrepo.unfilteredmethod
        def destroyed(self):
            if r'firstmergecach' in vars(self):
                self.firstmergecache.clear()
            super(firstmergecacherepo, self).destroyed()

        @localrepo.unfilteredmethod
        def updatecaches(self, tr=None, **kwargs):
            if utility.shouldwarmcache(self, tr):
                self.firstmergecache.update(self)
                self.firstmergecache.save(self)
            super(firstmergecacherepo, self).updatecaches(tr, **kwargs)

    repo.__class__ = firstmergecacherepo

class firstmergecache(genericcaches.changelogsourcebase):

    _filepath = b'evoext-firstmerge-00'
    _cachename = b'evo-ext-firstmerge'

    def __init__(self):
        super(firstmergecache, self).__init__()
        self._data = array.array(r'l')

    def get(self, rev):
        if len(self._data) <= rev:
            raise error.ProgrammingError(b'firstmergecache must be warmed before use')
        return self._data[rev]

    def _updatefrom(self, repo, data):
        """compute the rev of one revision, assert previous revision has an hot cache
        """
        cl = repo.unfiltered().changelog
        total = len(data)

        def progress(pos, rev=None):
            revstr = b'' if rev is None else (b'rev %d' % rev)
            compat.progress(repo.ui, b'updating firstmerge cache',
                            pos, revstr, unit=b'revision', total=total)
        progress(0)
        for idx, rev in enumerate(data, 1):
            assert rev == len(self._data), (rev, len(self._data))
            self._data.append(self._firstmerge(cl, rev))
            if not (idx % 10000): # progress as a too high performance impact
                progress(idx, rev)
        progress(None)

    def _firstmerge(self, changelog, rev):
        cl = changelog
        ps = filterparents(cl.parentrevs(rev))
        if not ps:
            return nodemod.nullrev
        elif len(ps) == 1:
            # linear commit case
            return self.get(ps[0])
        else:
            return rev

    # cache internal logic

    def clear(self, reset=False):
        """invalidate the cache content

        if 'reset' is passed, we detected a strip and the cache will have to be
        recomputed.

        Subclasses MUST overide this method to actually affect the cache data.
        """
        super(firstmergecache, self).clear()
        self._data = array.array(r'l')

    # crude version of a cache, to show the kind of information we have to store

    def load(self, repo):
        """load data from disk"""
        assert repo.filtername is None

        data = repo.cachevfs.tryread(self._filepath)
        self._data = array.array(r'l')
        if not data:
            self._cachekey = self.emptykey
        else:
            headerdata = data[:self._cachekeysize]
            self._cachekey = self._deserializecachekey(headerdata)
            compat.arrayfrombytes(self._data, data[self._cachekeysize:])
        self._ondiskkey = self._cachekey

    def save(self, repo):
        """save the data to disk

        Format is pretty simple, we serialise the cache key and then drop the
        bytearray.
        """
        if self._cachekey is None or self._cachekey == self._ondiskkey:
            return

        try:
            cachefile = repo.cachevfs(self._filepath, b'w', atomictemp=True)
            headerdata = self._serializecachekey()
            cachefile.write(headerdata)
            cachefile.write(compat.arraytobytes(self._data))
            cachefile.close()
            self._ondiskkey = self._cachekey
        except (IOError, OSError) as exc:
            repo.ui.log(b'firstmergecache', b'could not write update %s\n' % forcebytestr(exc))
            repo.ui.debug(b'firstmergecache: could not write update %s\n' % forcebytestr(exc))
