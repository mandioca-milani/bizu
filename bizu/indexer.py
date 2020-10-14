import re
import importlib

from bs4 import BeautifulSoup
from tinydb import TinyDB, where


db = TinyDB('data/db.json')
base_url = 'https://promilitares.com.br/cursos'

def index_courses():
    if not db.table('courses').all():
        driver = importlib.import_module('bizu.webdriver').driver

        if not driver.current_url == base_url:
            driver.get(base_url)

        courses = [
            'afa-en-efomm',
            'aprendiz',
            'carreira-militar',
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

        for index in range(len(soup)):
            db.table('courses').insert({
                'title': soup[index].attrs['href'].split('/')[1],
                'href': soup[index].attrs['href']
            })

    for course in db.table('courses').all():
         print('→ {}'.format(course['title']))

def index_course(course: str):
    if not db.table('courses').search(where('title') == course):
        print('Course not found!')
        return
    
    print(course)
