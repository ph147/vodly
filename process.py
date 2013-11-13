#!/usr/bin/python2

import re
from lxml import html

from http import get_tree, post


def process_gorillavid_in(hoster, url):
    root = get_tree(url)
    try:
        ident = root.xpath('//form/input[@name="id"]')[0].attrib['value']
    except IndexError:
        return None
    payload = {
        'op': 'download1',
        'usr_login': '',
        'channel': '',
        'method_free': 'Kostenloser Download',
        'id': ident,
    }
    data = post(url=url, data=payload)
    for line in data.split('\n'):
        if 'file: "' in line:
            line = re.sub(r'^.*file: "', '', line)
            return re.sub(r'",.*$', '', line)
    return None


def process_sockshare_ws(hoster, url):
    root = get_tree(url)
    try:
        filehash = root.xpath('//input[@name="hash"]')[0].attrib['value']
    except IndexError:
        return None
    payload = {
        'hash': filehash,
        'agreeButton': 'Continue as Free User',
    }
    data = post(url=url, data=payload)
    root = html.fromstring(data)
    return root.xpath('//a[@id="player"]')[0].attrib['href']


def process_putlocker_com(hoster, url):
    root = get_tree(url)
    try:
        filehash = root.xpath('//input[@name="hash"]')[0].attrib['value']
    except IndexError:
        return None
    payload = {
        'hash': filehash,
        'confirm': 'Continue as Free User',
    }
    data = post(url=url, data=payload)
    root = html.fromstring(data)
    remote_file = root.xpath(
        '//a[@class="download_file_link"]'
    )[0].attrib['href']
    return 'http://www.{}{}'.format(hoster, remote_file)


def process_putlocker_ws(hoster, url):
    payload = {
        'freeuser': 'yes',
        'confirm': 'Continue as Free User',
    }
    data = post(url=url, data=payload)
    for line in data.split('\n'):
        if 'url: \'' in line:
            line = re.sub(r'^.*url: \'', '', line)
            return re.sub(r'\',.*$', '', line)
    return None


def process_url(hoster, url):
    print 'Getting video from {}...'.format(hoster)
    video_url = HOSTER_PROCESSORS[hoster](hoster, url)
    return video_url


HOSTER_PROCESSORS = {
    'gorillavid.in': process_gorillavid_in,
    'gorillavid.com': process_gorillavid_in,
    'putlocker.ws': process_putlocker_ws,
    'putlocker.com': process_putlocker_com,
    'sockshare.com': process_putlocker_com,
    'sockshare.ws': process_sockshare_ws,
}
