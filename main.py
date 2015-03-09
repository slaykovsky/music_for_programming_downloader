__author__ = 'Alexey Slaykovsky'
__email__ = 'alexey@slaykovsky.com'
__music_for_programming__ = 'http://musicforprogramming.net'

import urllib.request
import os
from bs4 import BeautifulSoup
from sys import stdout


def main():
    print('Hi there!')
    print('I\'ll download some cool music')
    html = get_html(__music_for_programming__)
    menu_links = get_menu_links(html)
    # song_link = get_song_link(html)['href']
    # download_song(song_link)
    for menu_link in menu_links:
        link = menu_link['href']
        song_page = get_html(__music_for_programming__ + link)
        song_link = get_song_link(song_page)['href']
        download_song(menu_link.get_text(), song_link)


def get_html(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    return html


def get_menu_links(html):
    soup = BeautifulSoup(html)
    menu = soup.find('div', {'class': 'menu'})
    links = menu.findAll(href=True)
    return links


def get_song_link(html):
    soup = BeautifulSoup(html)
    content = soup.find('div', {'class': 'content'})
    link = content.find(href=True)
    return link


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
