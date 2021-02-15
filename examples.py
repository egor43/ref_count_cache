"""
    Examples of the "ref_count_cache" module

    Author: Myshko E.V.
"""

from datetime import datetime
import time
import threading
import ref_count_cahce


class Test(metaclass=ref_count_cahce.SingletonRefCountCaheMeta):
    """
        Class using caching "SingletonRefCountCaheMeta"
    """
    def __init__(self, name):
        self.name = name
        self.creating = datetime.now()


def foo(name, sleep_seconds=None):
    """
        Test function to demonstrate how the cache works
    """
    obj = Test(name)
    print(obj.creating, obj.name)
    if sleep_seconds:
        time.sleep(sleep_seconds)

"""
    Fast creation of objects of the Test class. 
    Objects are created and deleted quickly. 
    Thus, when creating a new object, there are no references to the previous one.

    Pay attention to the creation time of the object. It is different. 
    This means that the objects were re-constructed each time.
"""
print("\nFast creation of objects of the Test class:")
for _ in range(3):
    thread = threading.Thread(target=foo, args=("Alice",))
    thread.start()


"""
    Slow creation of objects of class Test.
    Objects are created quickly, but removed with a delay.
    Thus, when creating a new object, the link to the previous one remains active.
    Therefore, a new object is not created, but transferred from the cache.

    Pay attention to the creation time of the object. They are identical.
    This means that the objects were not rebuilt.
"""
print("\nSlow creation of objects of class Test:")
for _ in range(3):
    thread = threading.Thread(target=foo, args=("Bob", 5))
    thread.start()
