# -*- coding: utf-8 -*-
import re
import requests
from spotify import get_link
from bs4 import BeautifulSoup
from telegraphapi import Telegraph


storag = {}


def genius(request):
    global g_url, g_artist, g_song, g_song_id
    search_url = "http://api.genius.com/search"
    headers = {'Authorization': 'Bearer 6fqXZIZFy-g1s2Zr1zJ1eyR0jcy_Ar8ElHUpu45N3Wu4jG9jB3cvyfj2WsQH0Yka'}
    data = {'q': request}
    response = requests.get(search_url, params=data, headers=headers)
    json = response.json()
    if len(json["response"]["hits"]) == 0:
        print(data)
        return 0
    for hit in json["response"]["hits"]:
        if hit["type"] == "song":
            g_artist = hit["result"]["primary_artist"]["name"]
            g_song = hit["result"]["title_with_featured"]
            g_url = hit["result"]["url"]
            g_song_id = hit["result"]["id"]
            link = check_storage(g_song_id)
            if link:
                return g_artist, g_song, g_song_id, link, True

            break
    page = requests.get(g_url)
    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    g_lyrics = html.find('div', class_='lyrics').get_text()
    return g_artist, g_song, g_song_id, g_lyrics, False


def check_storage(song_id):
    global storag
    if int(song_id) in storag:
        return storag[song_id]
    else:
        return None


def add_to_storage(song_id, link):
    global storag
    storag[song_id] = link
    with open("linkstorage.dat", 'a', 3, 'utf-8') as file:
        file.write(str(song_id) + '->' + link + '\n')


def telegraph(artist, song, lyrics):
    t = Telegraph()
    t.createAccount("PythonTelegraphAPI")
    spam = '\n<strong>lyrics from <a href="http://genius.com/" target="_blank">genius.com</a>\n' \
           'presented by <a href="http://t.me/ReallyLyricsBot" target="_blank">t.me/ReallyLyricsBot</a></strong>'
    title = song + ' by ' + artist
    try:
        page = t.createPage(title, html_content=lyrics + spam, author_name=artist)
        return 'http://telegra.ph/{}'.format(page['path'])
    except:
        print("Error adding to telegra.ph")


def load_storage():
    if not storag:
        with open("linkstorage.dat", 'r', 3, 'utf-8') as file:
            rows = [row.strip() for row in file]

        for row in rows:
            song_id, link = re.split(r"->", row)
            storag[int(song_id)] = link
        print("Storage loaded to cache")


'''''''''''''''''''''''''''''''''
               Main
'''''''''''''''''''''''''''''''''


def by_title(request):
    try:
        artist, song, song_id, lyrics, st = genius(request)
        if st:
            print(artist + ' - ' + song + " - Lyrics from Storage")
            return lyrics, get_link(artist, song)
        print(artist + ' - ' + song + " - Added to Storage")
    except:
        return "Sorry, text not found :c"

    try:
        link = telegraph(artist, song, lyrics)
        add_to_storage(song_id, link)
    except:
        print("Telegraph error")
    return link, get_link(artist, song)


load_storage()
