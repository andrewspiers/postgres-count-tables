#!/usr/bin/env python2


#postgres_count_tables.py

"""
notes
-----
Configuration must be supplied entirely as
arguments.

Necessary database arguments:
 dbname, user, host, password

"""

import argparse
import os
import sys

import psycopg2



def connectionfromargs(args):
    """
    given an argparse parser namespace, return a db connection.
    """
    conn = psycopg2.connect(database=args.dbname,
                            user=args.username,
                            password=args.password,
                            host=args.host
                            )
    return conn


def counttables(conn, minimum=0, maximum=0):
    """
    given a connection to a database (conn), return the number of tables in
    that database. if provided with a minimum or maximum number of tables,
    sys.exit with code 40 or 41.

    Excludes tables in the information_schema and pg_catalog schemas.
    """
    assert isinstance(minimum,int)
    assert isinstance(maximum,int)
    query = "SELECT COUNT(table_name) FROM information_schema.tables "
    query += "WHERE table_schema != 'pg_catalog' AND table_schema != "
    query += "'information_schema';"
    cur = conn.cursor()
    cur.execute(query)
    tablecount = int(cur.fetchone()[0])
    cur.close()
    assert isinstance(tablecount,int)
    #print "tablecount = ", tablecount
    #print "minimum = ", minimum
    #print "maximum = ", maximum
    #if minimum == 0 and maximum == 0:
    #    return tablecount
    if tablecount < minimum and minimum !=0:
        sys.stderr.write(
            'Database contains less than ' + str(minimum) + ' tables\n')
        sys.exit(40)
    if tablecount > maximum and maximum !=0:
        sys.stderr.write(
            'Database contains more than ' + str(maximum) + ' tables\n')
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
                40. Defaults to zero, which means no minimum number of \
                tables.',
        'maximum': 'The maximum number of tables. If the database has \
                more tables than thiis, the script will exit with status \
                41. Defaults to zero, which means no maximum number of \
                tables.', }

    parser = argparse.ArgumentParser(
        description="Count the number of tables in a given database, raise \
                exit code if maximum and/or minimum table counts are not met.")
    parser.add_argument('--dbname', '-d', help=help['dbname'],
                        default=os.getlogin())
    parser.add_argument(
        '--username', '-U', help=help['username'], default=os.getlogin())
    parser.add_argument('--host', '-H', help=help['host'], default='localhost')
    parser.add_argument('--password', '-q', help=help['password'], default='')
    parser.add_argument(
        '--minimum', '-m', help=help['minimum'],default=0, type=int)
    parser.add_argument('--maximum', '-M', help=help['maximum'],default=0,
            type=int)
    args = parser.parse_args()
    print type(args)
    c = connectionfromargs(args)
    print(str(counttables(c,args.minimum,args.maximum)) + " tables counted.")
