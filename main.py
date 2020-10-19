import click

from bizu import *


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# command line interface
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@click.group()
def cli():
    """Bizu is a software to download promilitares.com.br courses."""
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# auth commands
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@cli.group(invoke_without_command=True)
@click.pass_context
def auth(ctx):
    """Verify user auth."""
    if ctx.invoked_subcommand is None:
        verify_auth()

@auth.command()
@click.option('-e', '--email', prompt=True)
@click.option('-p', '--password', prompt=True, hide_input=True)
def login(email, password):
    """Login user."""
    auth_login(email, password)

@auth.command()
def logout():
    """Logout user."""
    auth_logout()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# index commands
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@cli.group(invoke_without_command=True)
@click.pass_context
def index(ctx):
    """List courses to index."""
    if ctx.invoked_subcommand is None:
        idx_courses()

@index.command('course')
@click.argument('course')
def index_course(course):
    """Index selected course."""
    idx_course(course)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# download methods
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@cli.group(invoke_without_command=True)
@click.pass_context
def download(ctx):
    """List courses to download."""
    if ctx.invoked_subcommand is None:
        print('List courses to download')

@download.command('course')
@click.argument('course')
def download_course(course):
    print('Download {}'.format(course))
