#!/usr/bin/env/python2


#python-postgres-count-tables.py

"""
notes
-----
Configuration can be in a configuration file, or supplied entirely as
arguments.

Search order for the config file:
* os.getenv('PPCT_CONFIG'),
* os.getcwd(),
* os.getenv(XDG_CONFIG_HOME)/python-postgres-count-tables, where
  XDG_CONFIG_HOME defaults to $HOME/.config (XDG base spec)
* /etc/python-postgres-count-tables

Necessary database arguments:
 dbname, user, host, password

"""

import argparse
import ConfigParser
import os
import StringIO

import psycopg2


def findconfig():
    """return a ConfigParser object containing the configuration if one is
    found, else return None."""
    config = ConfigParser.ConfigParser()
    locations = []
    locations.append(os.getenv('PPCT_CONFIG'))
    locations.append(os.path.join(os.getcwd(),  'ppct_config'))
    if os.getenv('XDG_CONFIG_HOME'):
        locations.append(os.path.join(os.getenv('XDG_CONFIG_HOME'),
                                      'ppct_config'))
    else:
        locations.append(os.path.join(os.getenv('HOME'),
                         '.config/ppct_config'))
    locations.append('/etc/ppct_config')
    locations = [item for item in locations if item]  # strip out any None
    l = config.read(locations)
    return l


def createconfig(
        dbname=os.getlogin(),
        username=os.getlogin(),
        password="",
        host="localhost",
        minimum=0,
        maximum=0):
    """return a ConfigParser containing some defaults."""
    wconfig = ConfigParser.ConfigParser()
    wconfig.add_section('Main')
    wconfig.set('Main', 'dbname', dbname)
    wconfig.set('Main', 'username', username)
    wconfig.set('Main', 'password', password)
    wconfig.set('Main', 'host', host)
    wconfig.set('Main', 'minimum', minimum)
    wconfig.set('Main', 'maximum', maximum)
    return wconfig


def stringconfig(config):
    """
    return a given ConfigParser as a string
    """
    flo = StringIO.StringIO()  # file like object
    config.write(flo)
    flo.flush()
    flo.seek(0)
    return flo.read()


def makeconnection(config):
    """
    given a config, return a connection.
    """
    conn = psycopg2.connect(database=config.get('Main', 'dbname'),
                            user=config.get('Main', 'username'),
                            password=config.get('Main', 'password'),
                            host=config.get('Main', 'host'),
                            )
    return conn


def counttables(conn, minimum=0, maximum=0):
    """
    given a connection to a database (conn), return the number of tables in
    that database. if provided with a minimum or maximum number of tables,
    sys.exit with code 40 or 41.

    Excludes tables in the information_schema and pg_catalog schemas.
    """
    query = "SELECT COUNT(table_name) FROM information_schema.tables "
    query += "WHERE table_schema != 'pg_catalog' AND table_schema != "
    query += "'information_schema';"
    print(query)
    cur = conn.cursor()
    cur.execute(query)
    tablecount = cur.fetchone()[0]
    cur.close()
    if minimum == 0 or maximum == 0:
        return tablecount
    if tablecount < minimum:
        sys.stderror.write('Database contains less than ' + minimum + 'tables')
        sys.exit(40)
    if tablecount > maximum:
        sys.stderror.write('Database contains more than ' + maximum + 'tables')
        sys.exit(41)
    return tablecount


if __name__ == "__main__":
    help = {
        'dbname': 'The database to connect to. Defaults to your username.',
        'username': 'The username to user to connect. Defaults to \
                your username.',
        'host': 'The database server host. Defaults to localhost.',
        'password': 'Defaults to empty string.',
        'minimum': 'The minimum number of tables. If the database has fewer \
                tables than this, The script will exit with status \
                40.',
        'maximum': 'The maximum number of tables. If the database has \
                more tables than thiis, the script will exit with status \
                41.', }

    parser = argparse.ArgumentParser(
        description="Count the number of tables in a given database")
    parser.add_argument('--dbname', '-d', help=help['dbname'],
                        default=os.getlogin())
    parser.add_argument(
        '--username', '-U', help=help['username'], default=os.getlogin())
    parser.add_argument('--host', '-H', help=help['host'], default='localhost')
    parser.add_argument('--password', '-q', help=help['password'], default='')
    parser.add_argument('--minimum', '-m', help=help['minimum'])
    parser.add_argument('--maximum', '-M', help=help['maximum'])
    args = parser.parse_args()
    conf = createconfig(
        dbname=args.dbname, username=args.username, password=args.password,
        host=args.host, maximum=args.maximum, minimum=args.minimum)
    print stringconfig(conf)
    c = makeconnection(conf)
    print(counttables(c))
