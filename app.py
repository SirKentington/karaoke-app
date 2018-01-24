#!/usr/bin/env python


import sys
import songs
import fairqueue
import urllib

from flask import Flask, render_template, request, redirect, make_response
app = Flask(__name__, static_url_path='/static')

songlist = songs.SongList(sys.argv[1])
queue = fairqueue.FairQueue()

singer_cookie_name = 'kent_karaoke.singer_name'

# Add a series of random songs for testing the queue
singers = ['Kent', 'Lisa', 'Nels', 'Frosty']
for singer in singers:
    for i in range(5):
        queue.add(singer, songlist.random().sid)

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
        return ''
    return name

####################
# Displaying Songs #
####################
@app.route('/')
@app.route('/songs')
def root():
    name = singer_name()
    return search_box('', name=name)

@app.route('/songs/artist/')
@app.route('/songs/artist/<aid>')
def by_artist(aid=None):
    name = singer_name()
    if aid:
        results = songlist.all_by_artist(int(aid))
    else:
        results = songlist.by_artist
    return search_box('') + '<center>SONGS BY ARTIST</center><p>' + \
                    render_template('songs.html', songlist=results, name=name)

@app.route('/songs/title/')
def by_title():
    name = singer_name()
    return search_box('') + '<center>SONGS BY TITLE</center><p>' + \
                    render_template('songs.html', songlist=songlist.by_title, name=name)

@app.route('/songs/search')
def search():
    name = singer_name()
    searchtext = fmt(request.args.get('query'))
    print 'SEARCHED QUERY', searchtext
    results = songlist.search(searchtext.split())
    return search_box(searchtext) + render_template('songs.html', songlist=results, name=name)

####################
# Displaying Queue #
####################
@app.route('/queue/')
@app.route('/queue/display/')
@app.route('/queue/display/<singer>')
def queue_display(singer=None):
    name = singer_name()
    if singer:
        header = '%s\'s Queue' % singer
        namequeue = [(item.key, songlist[item.data]) for item in queue[singer]]
    else:
        header = 'All Singers Queue'
        namequeue = [(item.key, songlist[item.data]) for item in queue]
    return render_template('queue.html', queue=namequeue, name=name, header=header)

@app.route('/queue/add/<singer>/<sid>')
def queue_add(sid, singer=None):
    sid = int(sid)
    try:
        song = songlist[sid]
    except IndexError:
        pass
    if singer is None or sid >= len(songlist):
        return ''
    queue.add(singer, sid)
    return queue_display()

@app.route('/queue/remove/<singer>/<sid>')
def queue_remove(singer=None, sid=None):
    queue.remove(singer, int(sid))
    return queue_display(singer=None)

@app.route('/queue/moveup/<singer>/<sid>')
def queue_move_up(singer=None, sid=None):
    queue.moveup(singer, int(sid))
    return queue_display(singer=None)

@app.route('/queue/movedown/<singer>/<sid>')
def queue_move_down(singer=None, sid=None):
    queue.movedown(singer, int(sid))
    return queue_display(singer=None)

@app.route('/queue/setname')
def set_singer_name():
    singer = fmt(request.args.get('singer'))
    if not singer:
        return render_template('setname.html')
    resp = make_response(redirect('/songs'))
    resp.set_cookie(singer_cookie_name, singer)
    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

# vim: set expandtab sw=4 ts=4:
