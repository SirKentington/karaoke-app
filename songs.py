#!/usr/bin/env python

from collections import namedtuple
import random
import re
import urllib

Song = namedtuple('Song', 'artist title artist_url title_url sid')

class SongList(object):

    def __init__(self, filename):
        print 'Reading in songlist'
        sid = 0
        artist = ''
        title = ''
        artisturl = ''
        titleurl = ''
        songs = set()
        artists = set()
        id_dict = {}
        with open(filename, 'r') as f:
            for line in f.readlines():
                if line.isspace():
                    continue
                (artist, title) = line.split('#', 1)
                artist_url = urllib.quote(artist)
                title_url = urllib.quote(title)
                artist = artist.decode('utf-8').strip()
                title = title.decode('utf-8').strip()
                #print 'Derp', artist, title, artist_url, title_url
                song = Song(artist, title, artist_url, title_url, sid)
                songs.add(song)
                id_dict[sid] = song
                sid += 1
        songs = sorted(list(songs))
        self._id_dict = id_dict
        self.artists = sorted(list(artists))
        self.songs = songs
        self.by_artist = self.songs
        self.by_title = sorted(self.songs, key=lambda x: x[1])
        print 'Finished reading in songlist'

    def search(self, queries):
        if len(queries) == 0:
            return []
        results_list = []
        for song in self.songs:
            if all(re.search(query, song.artist + ' ' + song.title, re.IGNORECASE) for query in queries):
                results_list.append(song);
        results_list.sort()
        return results_list

    def all_by_artist(self, artist):
        return [song for song in self.songs if song.artist == artist]

    def artists(self):
        return self.artists

    def random(self):
        return self[random.randint(0, len(self))]

    def __getitem__(self, key):
        return self._id_dict[key]

    def __len__(self):
        return len(self.songs)

# vim: set expandtab sw=4 ts=4:
