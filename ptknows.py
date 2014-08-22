# -*- coding: utf-8 -*-

import os
import trace
import cPickle
from pytest import skip
from pkg_resources import get_distribution, DistributionNotFound

try:
    _dist = get_distribution('ptknows')
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py'
else:
    __version__ = _dist.version


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


GLOBALS = AttributeDict()
_MTIME_TMP_CACHE = {}


def register_store(open_store, close_store):
    GLOBALS.open_store = open_store
    GLOBALS.close_store = close_store


def get_file_mtime(filename):
    if not os.path.exists(filename):
        return None

    if filename in _MTIME_TMP_CACHE:
        return _MTIME_TMP_CACHE[filename]

    mtime = os.stat(filename).st_mtime
    _MTIME_TMP_CACHE[filename] = mtime
    return mtime


def pytest_configure(config):
    GLOBALS.store = GLOBALS.open_store()


def pytest_unconfigure(config):
    GLOBALS.close_store()


def pytest_runtest_call(item):
    skip_test = True
    dep_info = GLOBALS.store.get(item.nodeid) or None
    if dep_info is None:
        skip_test = False
    else:
        for filename, mtime in cPickle.loads(dep_info).iteritems():
            if mtime != get_file_mtime(filename):
                skip_test = False
                break
    if skip_test:
        skip("ptknows")

    tracer = trace.Trace(ignoredirs=(), trace=0, count=1)
    tracer.runctx('item.runtest()', globals=globals(), locals=locals())
    deps = {filename: get_file_mtime(filename) for filename, _ in tracer.results().counts.keys()}
    GLOBALS.store[item.nodeid] = cPickle.dumps(deps)


def pytest_runtest_logreport(report):
    if report.failed and report.nodeid in GLOBALS.store:
        del GLOBALS.store[report.nodeid]
