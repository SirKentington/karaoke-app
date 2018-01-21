#!/usr/bin/env python

from collections import namedtuple
import random
import re
import urllib

Song = namedtuple('Song', 'artist title artist_url title_url')

class SongList(object):

    def __init__(self, filename):
        print 'Reading in songlist'
        artist = ''
        title = ''
        artisturl = ''
        titleurl = ''
        songs = set()
        artists = set()
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
                songs.add(Song(artist, title, artist_url, title_url))
        songs = sorted(list(songs))
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
        return self.songs[random.randint(0, len(self.songs))]

# vim: set expandtab sw=4 ts=4:
