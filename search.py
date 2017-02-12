#!/usr/bin/env python

from flask import Flask
app = Flask(__name__, static_url_path='/static')

import re
import sys
import socket

hostname = 'http://zergling.americas.cray.com:5000'
hostname = 'http://localhost'
hostname = socket.gethostname()

class SongList(object):

    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.lines = f.readlines()
        self.songs = []
        for line in self.lines:
            (artist, title) = line.split('#', 1)
            self.songs.append((artist, title))
        self.songs = list(set(self.songs))
        self.songs.sort()
        self.by_artist = self.as_table(self.songs)
        self.songs.sort(key=lambda x: x[1])
        self.by_title = self.as_table(self.songs)

    def as_table(self, songs):

        if len(songs) == 0:
            return '<center>No Results</center>'

        table = '''
        <style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
            padding-right: 5px;
            padding-left: 5px;
        }
        </style>
        '''
        table += '<center><table>\n<tr>\n<th> Artist </th>\n<th> Title </th>\n'
        for artist, title in songs:
            table += '<tr><td> %s </td><td> %s </td></tr>\n' % (artist, title)
        table += '</table></center>'
        return table

    def search(self, queries):
        if len(queries) == 0:
            return self.as_table([])
        results_list = []
        for artist, title in self.songs:
            if all(re.search(query, artist + title, re.IGNORECASE) for query in queries):
                results_list.append((artist, title))
        results_list.sort()
        return self.as_table(results_list)

slist = SongList(sys.argv[1])

def search_box(text=''):
    string = '''
<center>
<img src=/static/batman.jpg style="width:600px"><p>
<a style="text-align:center" href=/songs/artist>All Songs by Artist</a><p>
<a style="text-align:center" href=/songs/title>All Songs by Title</a><p>
</center>
<div id="tfheader" style="text-align:center">
    <form id="tfnewsearch" method="get">
        <input type="text" class="tftextinput" id="tftextinput" name="q" size="21" maxlength="120" value="{1}">
        <input type="submit" value="Search" class="tfbutton">
    </form>
<div class="tfclear"></div>
</div>

<script>
    var a = document.getElementById('tfnewsearch');
    a.addEventListener('submit',function(e) {{
        e.preventDefault();
        var b = document.getElementById('tftextinput').value;
        window.location.href = '/songs/search/'+b;

    }});

</script>
'''
    return string.format(hostname, text)

@app.route('/')
@app.route('/songs')
def root():
    return search_box('')

@app.route('/songs/artist')
def by_artist():
    return search_box('') + '<center>SONGS BY ARTIST</center><p>' + slist.by_artist

@app.route('/songs/title')
def by_title():
    return search_box('') + '<center>SONGS BY TITLE</center><p>' + slist.by_title

@app.route('/songs/search/')
@app.route('/songs/search/<path>')
def search(path=''):
    path = path.replace('%20', ' ')
    return search_box(path) + slist.search(path.split())

@app.route('/batman')
def header_image():
    app.send_static_file('batman.jpg')

@app.route('/favicon.ico')
def icon():
    return ''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)

# vim: set expandtab sw=4 ts=4:
