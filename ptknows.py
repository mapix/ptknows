# -*- coding: utf-8 -*-

import os
import sys
import trace
import cPickle
from pytest import skip

# TODO: DBM related migrate to config
import shelve
def open_db():
    return shelve.open(os.path.join(os.curdir, '.ptknows'), writeback=True)

def close_db(db):
    db.sync()
    db.close()

DBM = None

def pytest_configure(config):
    global DBM
    DBM = open_db()

def pytest_unconfigure(config):
    global DBM
    close_db(DBM)

def pytest_runtest_call(item):
    global DBM
    skip_test = True
    dep_info = DBM.get(item.nodeid) or None
    if dep_info is None:
        skip_test = False
    else:
        for filename, mtime in cPickle.loads(dep_info).iteritems():
            if mtime != _get_file_mtime(filename):
                skip_test = False
                break
    if skip_test:
        skip("ptknows")
    tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix], trace=0, count=1)
    try:
        tracer.runctx('item.runtest()', globals=globals(), locals=locals())
    except:
        raise
    else:
        deps = {filename:_get_file_mtime(filename) for filename, _ in tracer.results().counts.keys()}
        DBM[item.nodeid] = cPickle.dumps(deps)


_MTIME_TMP_CACHE = {}

def _get_file_mtime(filename):
    if not os.path.exists(filename):
        return None

    if filename in _MTIME_TMP_CACHE:
        return _MTIME_TMP_CACHE[filename]

    mtime = os.stat(filename).st_mtime
    _MTIME_TMP_CACHE[filename] = mtime
    return mtime
