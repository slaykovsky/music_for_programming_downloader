__author__ = 'Alexey Slaykovsky'
__email__ = 'alexey@slaykovsky.com'
__music_for_programming__ = 'http://musicforprogramming.net/rss.php'


import urllib.request
import os
import feedparser
from sys import stdout


def main():
    print('Hi!')
    print('Let\'s download beautiful songs!')
    items = get_items(__music_for_programming__)
    links = get_song_links(items)
    for link in links:
        download_song(link['title'], link['url'])


def get_items(url):
    feed = feedparser.parse(url)
    items = feed['items']
    return items


def get_song_links(items):
    links = []
    for item in items:
        link = {'title': item['title'], 'url': item['links'][1]['href']}
        links.append(link)
    return links


def download_song(name, song_link):
    if ".mp3" in song_link:
        u = urllib.request.urlopen(song_link)
        meta = u.info()
        file_size = int(meta["Content-Length"])
        file_name = name + '.mp3'

        if os.path.isfile(file_name) and \
                os.stat(file_name).st_size == file_size:
            print(file_name + ' is already downloaded! Skipping!')
            return

        f = open(file_name, 'wb')
        print('Downloading: ' + file_name
              + ' Bytes: ' + str(file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d [%3.2f%%]" % \
                (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            stdout.write(status)
            stdout.flush()

        f.close()
    else:
        print('LOLWUT?')


if __name__ == '__main__':
    main()
