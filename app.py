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

# Add a series of random songs for testing the queue
singers = ['Kent', 'Lisa', 'Nels', 'Frosty']
for singer in singers:
    for i in range(5):
        song = songlist.random()
        print 'Adding singer/song', singer, song.sid, song.title
        queue.add(singer, song.sid)

for item in queue[singer]:
    print item.key, item.data

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

####################
# Displaying Songs #
####################
@app.route('/')
@app.route('/songs')
def root():
    return search_box('')

@app.route('/songs/artist/<aid>')
def by_artist(aid=None):
    if aid:
        results = songlist.all_by_artist(int(aid))
    else:
        results = songlist.by_artist
    return search_box('') + '<center>SONGS BY ARTIST</center><p>' + \
                    render_template('songs.html', songlist=results)

@app.route('/songs/title')
def by_title():
    return search_box('') + '<center>SONGS BY TITLE</center><p>' + \
                    render_template('songs.html', songlist=songlist.by_title)

@app.route('/songs/search')
def search():
    searchtext = fmt(request.args.get('query'))
    print 'SEARCHED QUERY', searchtext
    results = songlist.search(searchtext.split())
    return search_box(searchtext) + render_template('songs.html', songlist=results)

####################
# Displaying Queue #
####################
@app.route('/queue')
@app.route('/queue/display')
@app.route('/queue/display/<singer>')
def queue_display(singer=None):
    if singer:
        print 'SINGER', singer
        for item in queue[singer]:
            print item.key, item.data
        namequeue = [(item.key, songlist[item.data]) for item in queue[singer]]
        print namequeue
    else:
        print 'NOSINGER', singer
        for item in queue:
            print item.key, item.data
        namequeue = [(item.key, songlist[item.data]) for item in queue]
    for thing in namequeue:
        print thing[0], thing[1].title, thing[1].sid
    if singer is not None:
        return render_template('singerqueue.html', queue=namequeue)
    return render_template('queue.html', queue=namequeue)

def recreate_url(base, args):
    if len(args) == 0:
        return base
    return base + '?' + '&'.join(['%s=%s' % (v, args[v]) for v in args])

@app.route('/queue/add/<sid>/<singer>')
def queue_add(sid, singer=None):
    try:
        song = songlist[sid]
    except IndexError:
        pass
    if singer is None or song is None:
        return ''
    queue.add(singer, sid)
    return queue_display()

@app.route('/queue/remove/<sid>/<singer>')
def queue_remove(singer=None, sid=None):
    queue.remove(singer, int(sid))
    return queue_display(singer=None)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

# vim: set expandtab sw=4 ts=4:
