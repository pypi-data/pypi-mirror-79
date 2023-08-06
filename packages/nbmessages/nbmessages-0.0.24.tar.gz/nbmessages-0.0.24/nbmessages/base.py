"""Shared methods or any shared objects/funcs"""

from abc import ABCMeta, abstractproperty
import os, functools

from . import APPLICATION_DATA_DIR, DATA_DIR_IGNORE_DIRS

def get_directories():
    """list of all nbmessages directories"""
    items = os.listdir(APPLICATION_DATA_DIR)

    # ignore certain user defined directories
    for directory_to_ignore in DATA_DIR_IGNORE_DIRS:
        if directory_to_ignore in items:
            ind = items.index(directory_to_ignore)
            items.pop(ind)
    
    return items

def check_xsrf(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        _ = self.xsrf_token
        return f(self, *args, **kwargs)
    return wrapper