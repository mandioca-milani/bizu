import importlib
import re
import sys
import time
from pathlib import Path

import click
import requests
from bs4 import BeautifulSoup
from tinydb import TinyDB, where

from bizu import verify_auth

db = TinyDB('data/db.json')
base_url = 'https://promilitares.com.br'

pfx_done = '[{}]'.format(click.style('✓', fg='green'))
pfx_fail = '[{}]'.format(click.style('✗', fg='red'))
pfx_info = '[{}]'.format(click.style('i'))


def download_course(course: str):
    if not db.table('courses').search(where('title') == course):
        print(pfx_fail, 'Course {} not found!'.format(course))
        return

    course = db.table('courses').search(where('title') == course)[0]
    lessons = db.table('lessons').search(where('course') == course['title'])

    if not lessons:
        print(pfx_fail, 'Course {} have no lessons!'.format(course['title']))
        return

    season = dict(title='')
    module = dict(title='')

    for lesson in lessons:
        if module['title'] != lesson['module']:
            module = db.table('modules').search(
                where('title') == lesson['module'])[0]

            print('\n' + pfx_info, 'Module {}.'.format(module['title']))
            time.sleep(.1)

        if season['title'] != lesson['season']:
            season = db.table('seasons').search(
                where('title') == lesson['season'])[0]

            print('\n' + pfx_info, 'Season {}.'.format(season['title']))
            time.sleep(.1)

        video = dict(href='', path='')
        video['path'] = '.' + season['href']
        video['file'] = '.' + lesson['href']

        if Path(video['file'] + '.mp4').is_file():
            print(pfx_done, 'Lesson {} downloaded.'.format(lesson['title']))
            time.sleep(.1)
            continue

        print(pfx_info, 'Lesson {} downloading.'.format(lesson['title']))

        if not 'driver' in locals():
            driver = importlib.import_module('bizu.webdriver').driver

            if not verify_auth():
                return

        driver.get(base_url + lesson['href'])

        soup = BeautifulSoup(driver.page_source, 'html.parser').find(
            'iframe', {
                'class': 'video-player'
            }
        )

        if not soup:
            print(pfx_fail, 'Lesson {} download failure!'.format(
                lesson['title']))
            time.sleep(.1)
            continue

        video['href'] = 'https:' + \
            soup.attrs['src'].replace('player', 'download')

        Path(video['path']).mkdir(parents=True, exist_ok=True)

        with Path(video['file'] + '.bzdl').open('wb') as f:
            r = requests.get(video['href'], stream=True)

            iterable = r.iter_content(1000)
            length = int(r.headers['Content-Length']) / 1000

            with click.progressbar(iterable, length) as bar:
                for chunk in bar:
                    f.write(chunk)

            Path(video['file'] + '.bzdl').rename(video['file'] + '.mp4')

            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')
            sys.stdout.write('\033[F')
            sys.stdout.write('\033[K')

            print(pfx_done, 'Lesson {} downloaded.'.format(lesson['title']))
