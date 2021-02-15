"""
    The module contains the implementation of objects representing
    the functionality of caching with reference counting

    Author: Myshko E.V.
"""

import sys
from collections import UserDict
from threading import Lock


class RefCountCache(UserDict):
    """
        The class is a preemptive dictionary based on the number of references.
    """
    def __clear(self):
        """
            Clearing the internal dictionary of objects with missing external references.
            Doesn't handle circular references!
        """
        old_keys = [key for key in self if sys.getrefcount(super(RefCountCache, self).__getitem__(key)) < 3]
        for old_key in old_keys:
            del self[old_key]

    def __getitem__(self, key):
        """
            Get item
            Params:
                key - item key
            Return:
                item or KeyError
        """
        self.__clear()
        return super().__getitem__(key)


class SingletonRefCountCaheMeta(type):
    """
        A metaclass representing a thread-safe singleton with
        the ability to preempt objects in the absence of xrefs.
    """
    def __new__(cls, *args, **kwargs):
        """
            Create class instance
        """
        cls.__lock = Lock()
        cls.__instances = RefCountCache()
        return super().__new__(cls, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        """
            Create class object
        """
        key = f"{args}{kwargs}"
        with cls.__lock:
            instance = cls.__instances.get(key)
            if instance is None:
                instance = super().__call__(*args, **kwargs)
                cls.__instances[key] = instance
        return instance
