import importlib
import re
import time

import click
from bs4 import BeautifulSoup
from tinydb import TinyDB, where

db = TinyDB('data/db.json')
base_url = 'https://promilitares.com.br'


def index_courses():
    if not db.table('courses').all():
        driver = importlib.import_module('bizu.webdriver').driver

        if not driver.current_url == base_url + '/cursos':
            driver.get(base_url + '/cursos')

        courses = [
            'afa-en-efomm',
            'aprendiz',
            'cn-epcar',
            'colegio-naval',
            'eear',
            'epcar',
            'esa',
            'espcex',
            'fuzileiros',
            'ita-ime',
            'oficial-cbmg',
            'oficialato',
            'pm-barro-branco',
            'pmsp',
            'sargento-militar',
            'soldado-cbmg'
        ]

        soup = BeautifulSoup(driver.page_source, 'html.parser').find_all(
            'a', {
                'class': 'btn',
                'href': re.compile('/({})/[0-9]{}'.format('|'.join(courses), '{4}'))
            }
        )

        if not soup:
            click.secho('An error ocurred on indexing courses!', fg='red')
            return

        for index in range(len(soup)):
            db.table('courses').insert({
                'title': soup[index].attrs['href'].split('/')[1],
                'href': soup[index].attrs['href']
            })

    for course in db.table('courses').all():
        click.secho('→ {}'.format(course['title']), fg='green')


def index_course(course: str):
    if not db.table('courses').search(where('title') == course):
        click.secho('Course not found!', fg='red')
        return

    course = db.table('courses').search(where('title') == course)[0]
    modules = db.table('modules').search(where('course') == course['title'])

    if not modules:
        click.echo('Indexing {} modules.'.format(click.style(course['title'], fg='green')))

        driver = importlib.import_module('bizu.webdriver').driver

        if not driver.current_url == base_url + course['href']:
            driver.get(base_url + course['href'])

        soup = BeautifulSoup(driver.page_source, 'html.parser').find_all(
            'a', {
                'href': re.compile(course['href'] + '/')
            }
        )

        if not soup:
            click.secho('An error ocurred on indexing modules!', fg='red')
            return

        for index in range(len(soup)):
            db.table('modules').insert({
                'title': soup[index].attrs['href'].split('/')[-1],
                'course': course['title'],
                'href': soup[index].attrs['href']
            })

        modules = db.table('modules').search(where('course') == course['title'])

    click.echo('Indexed {} modules.'.format(click.style(course['title'], fg='green')))
    time.sleep(0.3)

    # {
    #     "title": "nivelamento-matematica",
    #     "course": "ita-ime",
    #     "href": "/ita-ime/2019/nivelamento-matematica"
    # }
    for module in modules:
        seasons = db.table('seasons').search(
            (where('course') == course['title']) &
            (where('module') == module['title'])
        )

        if not seasons:  # index seasons
            if not 'driver' in locals():
                driver = importlib.import_module('bizu.webdriver').driver

            # "https://promilitares.com.br/ita-ime/2019/nivelamento-matematica"
            driver.get(base_url + module['href'])

            soup = BeautifulSoup(driver.page_source, 'html.parser').find_all(
                'a', {
                    'href': re.compile(
                        # "/ita-ime/nivelamento-matematica/[0-9]{4}"
                        '/' + '/'.join([
                            module['course'],
                            module['title'],
                            '[0-9]{4}'
                        ])
                    )
                }
            )

            if not soup:
                click.secho('An error ocurred on indexing seasons!', fg='red')
                continue

            for index in range(len(soup)):
                # {
                #     "title": "nocoes-de-logica-matematica-e-conjuntos",
                #     "course": "ita-ime",
                #     "module": "nivelamento-matematica",
                #     "href": "/ita-ime/nivelamento-matematica/2019/nocoes-de-logica-matematica-e-conjuntos"
                # }
                db.table('seasons').insert({
                    'title': soup[index].attrs['href'].split('/')[-1],
                    'course': course['title'],
                    'module': module['title'],
                    'href': soup[index].attrs['href']
                })

            seasons = db.table('seasons').search(
                (where('course') == course['title']) &
                (where('module') == module['title'])
            )

        click.echo('Indexed {} seasons.'.format(click.style(module['title'], fg='blue')))
        time.sleep(0.3)

        for season in seasons:
            lessons = db.table('lessons').search(
                (where('course') == course['title']) &
                (where('module') == module['title']) &
                (where('season') == season['title'])
            )

            if not lessons:
                click.echo('Indexing {} lessons.'.format(click.style(season['title'], fg='cyan')))

                driver = importlib.import_module('bizu.webdriver').driver

                if not driver.current_url == base_url + season['href']:
                    driver.get(base_url + season['href'])

                soup = BeautifulSoup(driver.page_source, 'html.parser').find_all(
                    'a', {
                        'href': re.compile(season['href'] + '/[\s\S]+')
                    }
                )

                if not soup:
                    click.secho('An error ocurred on indexing lessons!', fg='red')
                    continue

                for index in range(len(soup)):
                    db.table('lessons').insert({
                        'title': soup[index].attrs['href'].split('/')[-1],
                        'course': course['title'],
                        'module': module['title'],
                        'season': season['title'],
                        'href': soup[index].attrs['href']
                    })

            click.echo('Indexed {} lessons.'.format(click.style(season['title'], fg='cyan')))
            time.sleep(0.1)
