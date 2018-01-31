from __future__ import print_function
from collections import defaultdict
from collections import namedtuple

import pickle

#Data = namedtuple('Data', 'key data')

backup_file = 'queue.backup'

class Data(object):
    def __init__(self, key, data):
        self.key = key
        self.data = data

def backup_filename(name):
    return name + '.queue.backup'

def create_queue(name):
    filename = backup_filename(name)
    try:
        with open(backup_file, 'r') as f:
            return pickle.load(f)
    except:
        pass
    return FairQueue(name)

def save_after(func):
    def do_save(self, *args, **kwargs):
        func(self, *args, **kwargs)
        with open(self.backup_file, 'w') as f:
            pickle.dump(self, f)
    return do_save

class FairQueue(object):

    '''
    Fair queue details:
        For a given key/value pair inserted into the queue
    '''
    def __init__(self, name):
        self.queue = []
        self.name = name
        self.backup_file = backup_filename(name)

    def _last_key_pos(self, key):
        # Find the last occurrence of key
        for n, item in reversed(list(enumerate(self.queue))):
            if item.key == key:
                return n
        raise ValueError

    @save_after
    def add(self, key, data):
        if data is None:
            raise ValueError

        if (key, data) in self:
            return

        try:
            pos = self._last_key_pos(key)
        except ValueError:
            pos = 0

        seen = set()
        for n, elem in enumerate(self.queue[pos:]):
            if elem.key in seen:
                self.queue.insert(pos + n, Data(key, data))
                return
            else:
                seen.add(elem.key)
        self.queue.append(Data(key, data))

    @save_after
    def reorder(self):
        oldq = self.queue
        self.queue = []
        for item in oldq:
            self.add(item.key, item.data)

    @save_after
    def remove(self, key, data):
        for n, elem in enumerate(self.queue[:]):
            if elem.key == key and elem.data == data:
                self.queue.remove(elem)
                self.reorder()
                return

    @save_after
    def moveup(self, key, data):
        last = None
        for item in self.queue:
            if item.key == key:
                if item.data == data:
                    if last is None:
                        return
                    item.data = last.data
                    last.data = data
                else:
                    last = item

    @save_after
    def movedown(self, key, data):
        last = None
        for item in self.queue:
            if item.key == key and item.data == data:
                last = item
            elif item.key == key and last is not None:
                last.data = item.data
                item.data = data
                return

    @save_after
    def addlist(self, key, datalist):
        for data in datalist:
            self.add(key, data)

    def pop(self):
        while True:
            elem = self.queue.pop()
            if elem.data is not None:
                return elem

    def keypop(self, key):
        newqueue = []
        keyqueue = []
        try:
            while True:
                item = self.queue.pop(0)
                if item.key == key and item.data is not None:
                    keyqueue.append(item.data)
                newqueue.append(item)
        except IndexError:
            pass
        self.queue = newqueue
        return keyqueue

    def keys(self):
        return list(set([item.key for item in self.queue]))

    def __getitem__(self, key):
        return [item for item in self.queue if item.key == key and item.data is not None]

    def __iter__(self):
        for item in self.queue:
            if item.data is None:
                continue
            yield item

    def __contains__(self, keytuple):
        for item in self.queue:
            if item.key == keytuple[0] and item.data == keytuple[1]:
                return True
        return False

    def __repr__(self):
        return repr(self.queue)

# vim: set expandtab sw=4 ts=4:
