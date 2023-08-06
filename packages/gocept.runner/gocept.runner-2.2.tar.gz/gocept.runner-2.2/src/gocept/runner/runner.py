# Copyright (c) 2008-2015 gocept gmbh & co. kg
# See also LICENSE.txt
"""Infrastructure for running."""

from __future__ import absolute_import
import contextlib
import ZODB.POSException
import logging
import signal
import time
import transaction
import zope.app.appsetup.product
import zope.component.hooks
import zope.app.wsgi
import zope.authentication.interfaces
import zope.publisher.base
import zope.security.management


log = logging.getLogger(__name__)


Exit = object()


class RunnerRequest(zope.publisher.base.BaseRequest):
    """A custom publisher request for the runner."""

    def __init__(self, *args):
        super(RunnerRequest, self).__init__(None, {}, positional=args)


class MainLoop(object):

    def __init__(self, app, ticks, worker, principal=None, once=False):
        self._is_running = False
        self.app = app
        self.ticks = ticks
        self.worker = worker
        self.once = once
        if principal is None:
            self.interaction = False
        else:
            self.interaction = True
            self.principal_id = principal

    def stopMainLoop(self, signum, frame):
        log.info("Received signal %s, terminating." % signum)
        self._is_running = False

    def __call__(self):
        old_site = zope.component.hooks.getSite()
        zope.component.hooks.setSite(self.app)

        self._is_running = True

        while self._is_running:
            ticks = None
            self.begin()
            try:
                ticks = self.worker()
            except (KeyboardInterrupt, SystemExit):
                self.abort()
                break
            except Exception as e:
                log.error("Error in worker: %s", repr(e), exc_info=True)
                self.abort()
            else:
                try:
                    self.commit()
                except ZODB.POSException.ConflictError:
                    # Ignore silently, the next run will be a retry anyway.
                    log.warning("Conflict error", exc_info=True)
                    self.abort()

            if self.once or ticks is Exit:
                self._is_running = False
            else:
                if ticks is None:
                    ticks = self.ticks
                log.debug("Sleeping %s seconds" % ticks)
                time.sleep(ticks)

        zope.component.hooks.setSite(old_site)

    def begin(self):
        transaction.begin()
        if self.interaction:
            request = RunnerRequest()
            request.setPrincipal(self.principal)
            zope.security.management.newInteraction(request)

    def abort(self):
        transaction.abort()
        if self.interaction:
            zope.security.management.endInteraction()

    def commit(self):
        transaction.commit()
        if self.interaction:
            zope.security.management.endInteraction()

    @property
    def principal(self):
        auth = zope.component.getUtility(
            zope.authentication.interfaces.IAuthentication)
        return auth.getPrincipal(self.principal_id)


class appmain(object):
    """Decorator to simplify the actual entry point functions for main loops.
    """

    def __init__(self, ticks=1, principal=None):
        self.ticks = ticks
        self.principal = principal
        self.once = False

    def get_principal(self):
        if callable(self.principal):
            return self.principal()
        # BBB: depcreated:
        return self.principal

    def __call__(self, worker_method):
        def configure(appname, configfile):
            with init(appname, configfile) as app:
                mloop = MainLoop(app, self.ticks, worker_method,
                                 principal=self.get_principal(),
                                 once=self.once)
                # XXX do we want more signal handlers?
                signal.signal(signal.SIGHUP, mloop.stopMainLoop)
                signal.signal(signal.SIGTERM, mloop.stopMainLoop)
                mloop()
        # Just to make doctests look nice.
        configure.__name__ = worker_method.__name__
        return configure


class once(appmain):

    def __init__(self, principal=None):
        super(once, self).__init__(principal=principal)
        self.once = True


@contextlib.contextmanager
def init(appname, configfile):
    """Initialise the Zope environment (without network servers) and return a
    specific root-level object.
    """
    db = zope.app.wsgi.config(configfile)
    root = db.open().root()
    # Not really worth using zope.app.publication.ZopePublication.root_name
    try:
        app = root['Application']
        if appname is not None:
            app = app[appname]
        yield app
    finally:
        db.close()


def from_config(section, variable):
    """Return a callable that returns a value from product config."""
    def get_config():
        config = zope.app.appsetup.product.getProductConfiguration(section)
        if config is None:
            raise KeyError('No such section %s' % section)
        return config[variable]
    return get_config
