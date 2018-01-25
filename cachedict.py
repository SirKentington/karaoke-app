
class CacheDict(object):
    def __init__(self, size=512):
        self._dict = {}
        self._lru_list = []
        self._max_cache = size

    def __contains__(self, key):
        return key in self._dict

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, val):
        self._dict[key] = val
        self._lru_list.append(key)
        if len(self._lru_list) >= self._max_cache:
            oldkey = self._lru_list.pop(0)
            del self._dict[oldkey]

