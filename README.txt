Count the number of tables in a postgres database.
Needs libpq-dev (debian) or postgresql-devel installed otherwise psycopg2 will
not install. May also need libpython2.7-dev or similar, to avoid this error::

    ./psycopg/psycopg.h:30:20: fatal error: Python.h: No such file or directory


To build a debian package from this using fpm::

  fpm -s python -t deb -a all $DIRECTORY/setup.py
