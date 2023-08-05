# Code dedicated to the caching of changeset depth
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
    scmutil,
)

from mercurial.utils.stringutil import forcebytestr

from . import (
    compat,
    error,
    exthelper,
    genericcaches,
    utility,
)

from mercurial.i18n import _

filterparents = utility.filterparents

eh = exthelper.exthelper()

def simpledepth(repo, rev):
    """simple but obviously right implementation of depth"""
    return len(repo.revs(b'::%d', rev))

@eh.command(
    b'debugdepth',
    [
        (b'r', b'rev', [], b'revs to print depth for'),
        (b'', b'method', b'cached', b"one of 'simple', 'cached', 'compare'"),
    ],
    _(b'REVS'))
def debugdepth(ui, repo, **opts):
    """display depth of REVS
    """
    revs = scmutil.revrange(repo, opts['rev'])
    method = opts['method']
    if method in (b'cached', b'compare'):
        cache = repo.depthcache
        cache.save(repo)
    for r in revs:
        ctx = repo[r]
        if method == b'simple':
            depth = simpledepth(repo, r)
        elif method == b'cached':
            depth = cache.get(r)
        elif method == b'compare':
            simple = simpledepth(repo, r)
            cached = cache.get(r)
            if simple != cached:
                raise error.Abort(b'depth differ for revision %s: %d != %d'
                                  % (ctx, simple, cached))
            depth = simple
        else:
            raise error.Abort(b'unknown method "%s"' % method)
        ui.write(b'%s %d\n' % (ctx, depth))

@eh.reposetup
def setupcache(ui, repo):

    class depthcacherepo(repo.__class__):

        @localrepo.unfilteredpropertycache
        def depthcache(self):
            cache = depthcache()
            cache.update(self)
            return cache

        @localrepo.unfilteredmethod
        def destroyed(self):
            if r'depthcache' in vars(self):
                self.depthcache.clear()
            super(depthcacherepo, self).destroyed()

        @localrepo.unfilteredmethod
        def updatecaches(self, tr=None, **kwargs):
            if utility.shouldwarmcache(self, tr):
                self.depthcache.update(self)
                self.depthcache.save(self)
            super(depthcacherepo, self).updatecaches(tr, **kwargs)

    repo.__class__ = depthcacherepo

class depthcache(genericcaches.changelogsourcebase):

    _filepath = b'evoext-depthcache-00'
    _cachename = b'evo-ext-depthcache'

    def __init__(self):
        super(depthcache, self).__init__()
        self._data = array.array(r'l')

    def get(self, rev):
        if len(self._data) <= rev:
            raise error.ProgrammingError(b'depthcache must be warmed before use')
        return self._data[rev]

    def _updatefrom(self, repo, data):
        """compute the rev of one revision, assert previous revision has an hot cache
        """
        cl = repo.unfiltered().changelog
        total = len(data)

        def progress(pos, rev=None):
            revstr = b'' if rev is None else (b'rev %d' % rev)
            compat.progress(repo.ui, b'updating depth cache',
                            pos, revstr, unit=b'revision', total=total)
        progress(0)
        for idx, rev in enumerate(data, 1):
            assert rev == len(self._data), (rev, len(self._data))
            self._data.append(self._depth(cl, rev))
            if not (idx % 10000): # progress as a too high performance impact
                progress(idx, rev)
        progress(None)

    def _depth(self, changelog, rev):
        cl = changelog
        ps = filterparents(cl.parentrevs(rev))
        if not ps:
            # root case
            return 1
        elif len(ps) == 1:
            # linear commit case
            return self.get(ps[0]) + 1
        # merge case, must find the amount of exclusive content
        p1, p2 = ps
        depth_p1 = self.get(p1)
        depth_p2 = self.get(p2)
        # computing depth of a merge
        ancnodes = cl.commonancestorsheads(cl.node(p1), cl.node(p2))
        if not ancnodes:
            # unrelated branch, (no common root)
            revdepth = depth_p1 + depth_p2 + 1
        elif len(ancnodes) == 1:
            # one unique branch point:
            # we can compute depth without any walk
            ancrev = cl.rev(ancnodes[0])
            depth_anc = self.get(ancrev)
            revdepth = depth_p1 + (depth_p2 - depth_anc) + 1
        else:
            # we pick the parent that is that is
            # * the deepest (less changeset outside of it),
            # * lowest revs because more chance to have descendant of other "above"
            parents = [(p1, depth_p1), (p2, depth_p2)]
            parents.sort(key=lambda x: (x[1], -x[0]))
            revdepth = parents[1][1]
            revdepth += len(cl.findmissingrevs(common=[parents[1][0]],
                                               heads=[parents[0][0]]))
            revdepth += 1 # the merge revision
        return revdepth

    # cache internal logic

    def clear(self, reset=False):
        """invalidate the cache content

        if 'reset' is passed, we detected a strip and the cache will have to be
        recomputed.

        Subclasses MUST overide this method to actually affect the cache data.
        """
        super(depthcache, self).clear()
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
            repo.ui.log(b'depthcache', b'could not write update %s\n' % forcebytestr(exc))
            repo.ui.debug(b'depthcache: could not write update %s\n' % forcebytestr(exc))
