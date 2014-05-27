# -*- coding: utf-8 -*-

import os
import shelve
import ptknows

store = shelve.open(os.path.join(os.curdir, 'ptknows.dbm'), writeback=True)


def open_store():
    return store


def close_store():
    store.sync()
    store.close()


ptknows.register_store(open_store, close_store)

pytest_plugins = ["ptknows", ]
