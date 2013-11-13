#!/usr/bin/python2

import re
import sys
import subprocess
from collections import defaultdict
from os.path import basename

from process import process_url
from http import get_tree, get_url
from search import search
from season import select


CACHE = 512

BLOCKED_HOST = 'integral-marketing.com'

PREFERRED_HOSTS = (
    'gorillavid.in',
    'gorillavid.com',
    'putlocker.com',
    'sockshare.com',
    'putlocker.ws',
    'sockshare.ws',
)


def get_info(row):
    link = row.xpath('td/span[@class="movie_version_link"]/a')
    hoster = row.xpath('td/span[@class="version_host"]/script')
    if not link or not hoster:
        return None
    link = link[0].attrib['href']
    hoster = hoster[0].text.replace('document.writeln(\'', '')
    hoster = re.sub(r"'.;.*$", '', hoster)

    if BLOCKED_HOST in link:
        return None
    return (hoster, link)


def get_table(url):
    links = defaultdict(set)
    root = get_tree(url)

    for elem in root.xpath('//table'):
        rows = elem.xpath('tbody/tr')
        for row in rows:
            try:
                hoster, link = get_info(row)
                links[hoster].add(link)
            except TypeError:
                pass
    return links


def play(video_url):
    print 'Now playing:', video_url
    devnull = open('/dev/null', 'w')
    process = subprocess.Popen(
        ['mplayer', '-ontop', '-cache', str(CACHE), video_url],
        stdout=devnull,
        stderr=devnull,
    )
    _, _ = process.communicate()


def try_hosts(data):
    for host in PREFERRED_HOSTS:
        if not host in data:
            continue
        for link in data[host]:
            url = get_url(link)
            video_url = process_url(host, url)
            if not video_url:
                print 'Error: 404'
                continue
            play(video_url)
            return


def print_usage(app_name):
    print 'usage: {} <search terms>'.format(app_name)


def main():
    search_terms = sys.argv[1:]
    if not search_terms:
        print_usage(basename(sys.argv[0]))
        sys.exit(1)
    show_link = search(' '.join(search_terms))
    episode_link = select(get_tree(show_link))
    data = get_table(episode_link)
    try_hosts(data)


if __name__ == '__main__':
    main()
