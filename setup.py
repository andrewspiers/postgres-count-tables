from distutils.core import setup

setup(
        author='Andrew Spiers',
        author_email='andrew@andrewspiers.net',
        name = 'python_postgres_count_tables',
        url=
        'https://bitbucket.org/andrewspiers/python-postgres-count-tables',
        version='0.1.0dev',
        packages=['python_postgres_count_tables',],
        license='Apache 2.0',
        long_description=open('README.txt').read(),
        install_requires=["psycopg2 >= 2.4.5",],
        scripts=['bin/python_postgres_count_tables.py'],
    )


