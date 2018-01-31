from __future__ import print_function

import fairqueue
import songs

class KaraokeParty(object):
    def __init__(self, name):
        self.name = name
        self.queue = fairqueue.create_queue(name)
        self.songs = songs.songlist()
