from setuptools import setup


setup(
    name='bizu',
    version='0.1',
    py_modules=['main'],
    install_requires=[
        'click',
        'selenium',
    ],
    entry_points='''
        [console_scripts]
        bizu=main:cli
    ''',
)
