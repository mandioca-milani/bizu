import click


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
        print('Verify user auth')

@auth.command()
@click.option('-e', '--email', prompt=True)
@click.option('-p', '--password', prompt=True, hide_input=True)
def login(email, password):
    """Login user."""
    print('Login user {}'.format(email))

@auth.command()
def logout():
    """Logout user."""
    print('Logout user')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# index commands
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@cli.group(invoke_without_command=True)
@click.pass_context
def index(ctx):
    """List courses to index."""
    if ctx.invoked_subcommand is None:
        print('List courses to index')

@index.command('course')
@click.argument('course')
def index_course(course):
    """Index selected course."""
    print('index {}'.format(course))

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
