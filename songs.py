#!/usr/bin/env python
from __future__ import print_function
from collections import namedtuple
from collections import defaultdict
from collections import OrderedDict
import random
import re
import urllib

Song = namedtuple('Song', 'artist title aid sid')
Artist = namedtuple('Artist', 'artist aid')

class CacheDict(object):
    def __init__(self, size=0):
        self._dict = OrderedDict()
        self._max_cache = size

    def __contains__(self, key):
        return key in self._dict

    def __getitem__(self, key):
        val = self._dict[key]
        del self._dict[key]
        self._dict[key] = val
        return val

    def __setitem__(self, key, val):
        self._dict[key] = val
        if len(self._dict) >= self._max_cache:
            self._dict.popitem()

class Incrementor(object):
    def __init__(self):
        self.n = 0

    def inc(self):
        self.n += 1
        return self.n

class SongList(object):

    def __init__(self, filename):
        print('Reading in songlist')
        tmp_songlist = []
        aid = 0
        aid_inc = Incrementor()
        artist = ''
        title = ''
        songs = []
        sid_dict = {}
        aid_dict = defaultdict(list)
        artist_to_aid = {}
        # Read in every artist/title pair
        with open(filename, 'r') as f:
            for line in f.readlines():
                if line.isspace():
                    continue
                try:
                    (artist, title) = [x.decode('utf-8').strip() for x in re.split(r'###', line, 1)]
                except ValueError:
                    print('Line not formatted correctly:', line)
                    continue
                artist = artist[:30]
                tmp_songlist.append((artist, title))
        # Filter out dups and sort by title
        tmp_songlist = sorted(list(set(tmp_songlist)), key=lambda x: x[1])
        for sid, (artist, title) in enumerate(tmp_songlist):
            if artist not in artist_to_aid:
                artist_to_aid[artist] = aid_inc.inc()
            aid = artist_to_aid[artist]
            song = Song(artist, title, aid, sid)
            songs.append(song)
            aid_dict[aid].append(song)
            sid_dict[sid] = song
        self.artist_to_aid = artist_to_aid
        self._aid_dict = aid_dict
        self._sid_dict = sid_dict
        self.artists = sorted([Artist(key, val) for key, val in self.artist_to_aid.items()], key=lambda x:x.artist.upper())
        self.songs = songs
        self.by_title = songs
        self.by_artist = sorted(self.songs)
        self.search_cache = CacheDict()
        print('Finished reading in songlist')

    def search(self, query):
        if len(query) == 0:
            return []
        if query in self.search_cache:
            print('Cache hit on', query)
            return self.search_cache[query]
        print('Cache miss on', query)
        results_list = []
        queries = query.split()
        for song in self.songs:
            if all(re.search(q, song.artist + ' ' + song.title, re.IGNORECASE) for q in queries):
                results_list.append(song);
        results_list.sort()
        self.search_cache[query] = results_list
        return results_list

    def all_by_artist(self, aid=None):
        if aid:
            return sorted(self._aid_dict[aid])
        return self.by_artist

    def aid_to_artist(self, artist_id):
        return self._aid_dict[artist_id][0].artist

    def random(self):
        return self[random.randint(0, len(self))]

    def __getitem__(self, key):
        return self._sid_dict[key]

    def __len__(self):
        return len(self.songs)

# vim: set expandtab sw=4 ts=4:
