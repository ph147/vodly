#!/usr/bin/python2

import re
import sys
from collections import namedtuple

from http import get_tree


SEARCH_BASE = 'http://vodly.to/index.php?search_section=1&search_keywords='


def get_list(root):
    result = []
    show = namedtuple('show', 'name link')
    for elem in root.xpath('//div[@class="index_item index_item_ie"]'):
        anchor = elem.xpath('a')[0]
        link = anchor.attrib['href']
        name = re.sub('^Watch ', '', anchor.attrib['title'])
        result.append(show(name, link))
    return result


def choose(show_list):
    for num, (name, _) in enumerate(show_list):
        print '{}\t{}'.format(num+1, name)
    try:
        response = int(raw_input('? '))
    except ValueError:
        sys.exit(1)
    if response < 1 or response > len(show_list):
        sys.exit(1)
    return show_list[response-1].link


def search(name):
    name = name.replace(' ', '+')
    root = get_tree('{}{}'.format(SEARCH_BASE, name))
    show_list = get_list(root)

    if not show_list:
        print 'No search results.'
        sys.exit(1)
    elif len(show_list) == 1:
        return show_list[0].link
    else:
        return choose(show_list)


def main():
    response = search('how mother')
    print 'retrieved url: ', response


if __name__ == '__main__':
    main()
