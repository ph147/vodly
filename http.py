#!/usr/bin/python2

import requests
from lxml import html

BASE_URL = 'http://vodly.to'

CHROME_HEADER = {
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/28.0.1500.71 Chrome/28.0.1500.71 Safari/537.36',
    'Accept-Language': 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4',
}


def get(url, data=None):
    return requests.get(
        url=url, data=data, headers=CHROME_HEADER
    ).text


def post(url, data=None):
    return requests.post(
        url=url, data=data, headers=CHROME_HEADER
    ).text


def url_read(url):
    print 'Loading url "{}"...'.format(url)
    req = requests.get(url, headers=CHROME_HEADER)
    return req.text


def get_tree(url):
    data = url_read(url)
    return html.fromstring(data)


def get_url(link):
    response = requests.head('{}{}'.format(BASE_URL, link))
    return response.headers['location']
