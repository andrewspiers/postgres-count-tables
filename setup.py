from distutils.core import setup

setup(
        author='Andrew Spiers',
        author_email='andrew@andrewspiers.net',
        name = 'python-postgres-count-tables',
        url=
        'https://bitbucket.org/andrewspiers/python-postgres-count-tables',
        version='0.1.0dev',
        packages=['python-postgres-count-tables',],
        license='Apache 2.0',
        long_description=open('README.txt').read(),
        install_requires=["psycopg2 >= 2.4.5",],
    )


