import sys
import json
import click
import importlib
from pathlib import Path
from selenium.webdriver.common.action_chains import ActionChains


base_url = 'https://promilitares.com.br'


def verify_auth():
    click.echo('Checking auth...')

    driver = importlib.import_module('bizu.webdriver').driver
    
    if not driver.current_url == base_url + '/cursos':
        driver.get(base_url + '/cursos')
    
    if Path('data/cookies.json').is_file():
        driver.delete_all_cookies()
        
        with Path('data/cookies.json').open('r') as f:
            for cookie in json.load(f):
                driver.add_cookie(cookie)

        driver.refresh()

    try:
        if driver.find_element_by_class_name('saudacao'):
            click.secho('Someone is logged in!', fg='green')
            return True
    except:
        with Path('data/cookies.json').open('w') as f:
            json.dump([], f)

        driver.delete_all_cookies()
        driver.refresh()

        click.secho('Nobody is logged in!', fg='red')
        return False


def auth_login(email, password):
    click.echo('Logging in...')

    if verify_auth():
        return True

    driver = importlib.import_module('bizu.webdriver').driver

    try:
        driver.find_element_by_name('_username').send_keys(email)
        driver.find_element_by_name('_password').send_keys(password)
        driver.find_element_by_class_name('btn-enviar').click()
    except:
        click.secho('An error ocurred on logging in!', fg='red')
        return False

    try:
        if driver.find_element_by_class_name('saudacao'):
            with Path('data/cookies.json').open('w') as f:
                json.dump(driver.get_cookies(), f)

            click.secho('You are logged in!', fg='green')
            return True
    except:
        click.secho('Invalid credentials!', fg='red')
        return False


def auth_logout():
    click.echo('Logging out...')
    
    if not verify_auth():
        return True

    driver = importlib.import_module('bizu.webdriver').driver

    try:
        action = ActionChains(driver)

        action.move_to_element(
            driver.find_element_by_class_name('item-logado')
        ).perform()

        action.click(
            driver.find_element_by_xpath('//a[@href="/logout"]')
        ).perform()

        click.secho('Softly logged out.', fg='green')
    except:
        click.secho('Hardly logged out.', fg='yellow')

    with Path('data/cookies.json').open('w') as f:
        json.dump([], f)

