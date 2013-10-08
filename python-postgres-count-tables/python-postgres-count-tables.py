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

def findconfig():
    """return a ConfigParser object containing the configuration if one is
    found, else return None."""
    config = ConfigParser.ConfigParser()
    locations = []
    locations.append(os.getenv('PPCT_CONFIG'))
    locations.append(os.path.join(os.getcwd(),'ppct_config'))
    if os.getenv('XDG_CONFIG_HOME'):
        locations.append(os.path.join(os.getenv('XDG_CONFIG_HOME'), 'ppct_config'))
    else:
        locations.append(os.path.join(os.getenv('HOME'),'.config/ppct_config'))
    locations.append('/etc/ppct_config')
    locations = [ item for item in locations if item ]  #strip out any None
    l = config.read(locations)
    #print (locations)
    #print ("configuration file found at " + " ".join(l))
    return l
    
def defaultconfig():
    """return a ConfigParser containing some defaults."""
    wconfig = ConfigParser.ConfigParser()
    wconfig.add_section('Main')
    #dbname,user,password,host
    #default dbname : username
    wconfig.set('Main','dbname',os.getlogin())
    #default user   : username
    wconfig.set('Main','username',os.getlogin())
    #default password : empty string
    wconfig.set('Main','password','')
    #default host     : localhost
    wconfig.set('Main','host','localhost')
    return wconfig

def stringconfig(config):
    """
    return a given ConfigParser as a string
    """
    flo = StringIO.StringIO()  #file like object
    config.write(flo)
    flo.flush()
    flo.seek(0)
    return flo.read()


findconfig()
default = defaultconfig()
printabledefault = stringconfig(default)
print (printabledefault)
