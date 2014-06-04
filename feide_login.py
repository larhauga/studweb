#!/usr/bin/env python
#-*- coding: utf-8 -*-

from mechanize import Browser
import csv

def get_users():
    try:
        credentials = {}
        with open('feide.conf', 'rb') as f:
            reader = csv.reader(f, delimiter=',', skipinitialspace=True)
            for row in reader:
                if row[0].startswith('#'):
                    continue
                credentials[row[0]] = row[1:]
            return credentials
    except IOError as e:
        print "No login information available. Config file is missing: %s" % e
        return None

def browser_login(browser):
    raise NotImplementedError

if __name__ == '__main__':
    print get_users()
