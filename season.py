#!/usr/bin/python

import re
import sys
from collections import namedtuple, defaultdict


def get_season_from_link(link):
    match = re.search(r'/season-([0-9]+)-episode', link)
    return int(match.group(1))


def get_episode_from_link(link):
    match = re.search(r'/season-[0-9]+-episode-([0-9]+)', link)
    return int(match.group(1))


def get_episodes(root):
    result = defaultdict(dict)

    episode_pair = namedtuple('episode_pair', 'title link')
    tv_containers = root.xpath('//div[@class="tv_container"]')
    for elem in tv_containers:
        for episode in elem.xpath('div[@class="tv_episode_item"]'):
            try:
                anchor = episode.xpath('a')[0]
                link = anchor.attrib['href']
                title = anchor.xpath('span')[0].text
                title = re.sub(r'^ *- ', '', title)
                season_number = get_season_from_link(link)
                episode_number = get_episode_from_link(link)
            except IndexError:
                continue
            result[season_number][episode_number] = episode_pair(title, link)
    return result


def choose(iterable):
    try:
        response = int(raw_input('? '))
    except ValueError:
        sys.exit(1)
    if response < 1 or response > len(iterable):
        sys.exit(1)
    return response


def choose_season(seasons):
    for season in sorted(seasons):
        print 'Season {}'.format(season)
    response = choose(seasons)
    return seasons[response]


def choose_episode(season):
    for episode in sorted(season):
        print episode, season[episode].title
    response = choose(season)
    return season[response]


def get_episode_link(root, season, episode):
    seasons = get_episodes(root)
    return seasons[season][episode].link


def select(root):
    seasons = get_episodes(root)
    season = choose_season(seasons)
    episode_link = choose_episode(season).link
    return episode_link


def main():
    pass


if __name__ == '__main__':
    main()
