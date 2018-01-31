#!/usr/bin/env python
from __future__ import print_function
import sys
import songs
import fairqueue
import urllib

from flask import Flask, render_template, request, redirect, make_response
app = Flask(__name__, static_url_path='/static')

songlist = songs.SongList(sys.argv[1])
queue = fairqueue.create_queue('derp')

singer_cookie_name = 'kent_karaoke.singer_name'

# Add a series of random songs for testing the queue
singers = ['Kent', 'Lisa', 'Nels', 'Frosty']
singers = []
for singer in singers:
    for i in range(5):
        queue.add(singer, songlist.random().sid)

lettercache = {}

#####################
# Generic functions #
#####################
def fmt(string):
    if string is None:
        return None
    return urllib.unquote(string.decode('utf-8').strip())

def search_box(text='', name=''):
    name = singer_name()
    return render_template('searchbox.html', searchtext=text, name=name)

@app.route('/batman')
def header_image():
    app.send_static_file('batman.jpg')

@app.route('/favicon.ico')
def icon():
    return ''

def singer_name():
    name = request.cookies.get(singer_cookie_name)
    if not name:
        return None
    return name

####################
# Displaying Songs #
####################
@app.route('/')
@app.route('/artists/')
def artists():
    name = singer_name()
    if not name:
        return render_template('setname.html')
    return search_box('') + render_template('artists.html', name=name)

@app.route('/artists/letter/<letter>')
def artist_by_letter(letter=None):
    if letter is None:
        return
    letter = letter.upper()
    if letter in lettercache:
        return search_box('') + render_template('artistslist.html', artistlist=lettercache[letter])
    artistlist = []
    for artist in songlist.artists:
        if artist.artist.upper().startswith(letter):
            artistlist.append(artist)
    lettercache[letter.upper()] = artistlist
    return search_box('') + render_template('artistsletter.html', artistlist=artistlist)

@app.route('/artists/<start>/<end>')
def artists_list(start=0, end=1):
    name = singer_name()
    if not name:
        return render_template('setname.html')
    artistlist = songlist.artists[int(start): int(end)]
    return render_template('artistslist.html', artistlist=artistlist, name=name)

@app.route('/songs')
@app.route('/songs/artist/')
def root():
    name = singer_name()
    if not name:
        return render_template('setname.html')
    return search_box('') + render_template('artistsendless.html', songlist=songlist.by_artist, name=name)

@app.route('/songs/artist/<aid>')
def by_artist(aid=None):
    name = singer_name()
    if not name:
        return render_template('setname.html')
    if aid:
        results = songlist.all_by_artist(int(aid))
    else:
        results = songlist.by_artist
    return search_box('') + render_template('songs.html', songlist=results, name=name)

@app.route('/songs/title/')
def by_title():
    name = singer_name()
    if not name:
        return render_template('setname.html')
    return search_box('') + '<center>SONGS BY TITLE</center><p>' + \
                    render_template('songsendless.html', name=name)

@app.route('/songs/title/<start>/<end>/')
def title_start_end(start=0, end=1):
    name = singer_name()
    if not name:
        return render_template('setname.html')
    slist = songlist.songs[int(start):int(end)]
    print(len(slist))
    return render_template('songtable.html', songlist=slist, name=name)

@app.route('/songs/artist/<start>/<end>/')
def artist_start_end(start=0, end=1):
    name = singer_name()
    if not name:
        return render_template('setname.html')
    slist = songlist.by_artist[int(start):int(end)]
    print(len(slist))
    return render_template('songtable.html', songlist=slist, name=name)

@app.route('/songs/search')
def search():
    name = singer_name()
    if not name:
        return render_template('setname.html')
    searchtext = fmt(request.args.get('query'))
    print('SEARCHED QUERY', searchtext)
    results = songlist.search(searchtext)
    return search_box(searchtext) + render_template('songs.html', songlist=results, name=name)

####################
# Displaying Queue #
####################
@app.route('/queue/')
@app.route('/queue/display/')
@app.route('/queue/display/<singer>')
def queue_display(singer=None):
    name = singer_name()
    if not name:
        return render_template('setname.html')
    if singer:
        header = '%s\'s Queue' % singer
        namequeue = [(item.key, songlist[item.data]) for item in queue[singer]]
    else:
        header = 'All Singers Queue'
        namequeue = [(item.key, songlist[item.data]) for item in queue]
    return search_box('') + render_template('queue.html', queue=namequeue, name=name, header=header)

@app.route('/queue/api/add/<singer>/<sid>', methods=['PUT'])
def queue_add(sid, singer=None):
    response = make_response()
    name = singer_name()
    if not name:
        return '', 403
    sid = int(sid)
    try:
        song = songlist[sid]
    except IndexError:
        return '', 404
        pass
    if singer is None or singer == 'None' or sid >= len(songlist):
        return '', 403
    queue.add(singer, sid)
    return '', 200

@app.route('/queue/remove/<singer>/<sid>')
def queue_remove(singer=None, sid=None):
    queue.remove(singer, int(sid))
    return ''

@app.route('/queue/moveup/<singer>/<sid>')
def queue_move_up(singer=None, sid=None):
    queue.moveup(singer, int(sid))
    return queue_display(singer=None)

@app.route('/queue/movedown/<singer>/<sid>')
def queue_move_down(singer=None, sid=None):
    queue.movedown(singer, int(sid))
    return queue_display(singer=None)

@app.route('/queue/setname')
def set_name():
    singer = fmt(request.args.get('singer'))
    if singer is None:
        return render_template('setname.html')
    resp = make_response(render_template('redirect.html'))
    resp.set_cookie(singer_cookie_name, singer)
    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)

# vim: set expandtab sw=4 ts=4:
