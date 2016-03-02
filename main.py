import urllib.request
import os
import feedparser
import sys

RSS_LINK = 'http://musicforprogramming.net/rss.php'


def get_song_links(items):
    links = []
    for item in items:
        link = {'title': item['title'], 'url': item['links'][1]['href']}
        links.append(link)
    return links


def get_items(url):
    feed = feedparser.parse(url)
    items = feed['items']
    return items


def download_song(title, url, download_dir):
    if ".mp3" in url:
        u = urllib.request.urlopen(url)
        meta = u.info()
        file_size = int(meta["Content-Length"])
        file_name = title + '.mp3'
        file_path = os.path.join(download_dir, file_name)

        if os.path.isfile(file_path) and \
                os.stat(file_path).st_size == file_size:
            print(file_name + ' is already downloaded! Skipping!')
            return

        try:
            f = open(file_path, 'wb')
        except Exception as e:
            print(str(e))
            print('Do you want to create directory? (yes, no):',)
            answer = input()
            if answer == 'yes':
                os.mkdir(download_dir)
                f = open(file_path, 'wb')
            elif answer == 'no':
                return
            else:
                print('Please answer "yes" or "no".')

        print('Downloading: ' + file_name + ' Bytes: ' + str(file_size))

        file_size_dl = 0
        block_sz = 8192

        while True:
            buff = u.read(block_sz)
            if not buff:
                break

            file_size_dl += len(buff)
            f.write(buff)
            status = r"%10d [%3.2f%%]" % \
                (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            sys.stdout.write(status)
            sys.stdout.flush()
        f.close()
    else:
        print('LOLWUT?')


def main():
    try:
        download_dir = sys.argv[1]
    except:
        download_dir = './downloads'
    print('Hi!')
    print('Let\'s download beautiful songs!')
    print('Songs will be downloaded in %s directory.' % download_dir)
    items = get_items(RSS_LINK)

    links = get_song_links(items)

    for link in links:
        title = link['title']
        url = link['url']
        download_song(title, url, download_dir)


if __name__ == '__main__':
    main()
