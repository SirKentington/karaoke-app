#!/usr/bin/env python


import sys
import songs
import fairqueue
import urllib
from collections import namedtuple

from flask import Flask, render_template, request
app = Flask(__name__, static_url_path='/static')

urlinfo = namedtuple('urlinfo', 'artist title artisturl titleurl')

songlist = songs.SongList(sys.argv[1])
queue = fairqueue.FairQueue()

for singer in ['Kent', 'Lisa', 'Nels', 'Frosty']:
    for i in xrange(5):
        queue.add(singer, ' '.join(songlist.random()))

# GENERIC STUFF
def fmt(string):
    if string is None:
        return None
    return urllib.unquote(string.decode('utf-8').strip())

def to_url(string):
    return urllib.quote(string.decode('utf-8'))

def search_box(text=''):
    return render_template('searchbox.html', searchtext=text)

@app.route('/batman')
def header_image():
    app.send_static_file('batman.jpg')

@app.route('/favicon.ico')
def icon():
    return ''

# SONGS PART
@app.route('/')
@app.route('/songs')
def root():
    return search_box('')

@app.route('/songs/artist')
def by_artist():
    return search_box('') + '<center>SONGS BY ARTIST</center><p>' + \
                    render_template('songs.html', songlist=songlist.by_artist)

@app.route('/songs/title')
def by_title():
    return search_box('') + '<center>SONGS BY TITLE</center><p>' + \
                    render_template('songs.html', songlist=songlist.by_title)

@app.route('/songs/search')
def search():
    searchtext = ''
    artist = fmt(request.args.get('artist'))
    if artist is not None:
        results = songlist.all_by_artist(artist)
        searchtext = artist
    else:
        query = fmt(request.args.get('query')).split()
        print 'SEARCHED WITH QUERY', query
        results = songlist.search(query)
        searchtext = artist
    return search_box(searchtext) + render_template('songs.html', songlist=results)

# QUEUE PART
@app.route('/queue/display')
def queue_display(all_singers=False):
    display_q = queue
    singer = None
    if not all_singers:
        singer = fmt(request.args.get('singer'))
    if singer is not None:
        display_q = queue[singer]
    return render_template('queue.html', queue=display_q)

@app.route('/queue/display/<singer>')
def queue_singer(singer):
    return render_template('singerqueue.html', queue=queue[singer])

@app.route('/queue/add')
def queue_add():
    singer = fmt(request.args.get('singer'))
    song   = fmt(request.args.get('song'))
    queue.add(singer, song)
    return queue_display()

@app.route('/queue/remove')
def queue_remove():
    singer = fmt(request.args.get('singer'))
    song   = fmt(request.args.get('song'))
    queue.remove(singer, song)
    return queue_display(True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

# vim: set expandtab sw=4 ts=4:
