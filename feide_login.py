#!/usr/bin/env python
#-*- coding: utf-8 -*-

from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import sys
import csv
import re

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

def browser_login(br, school):
    # Getting the username and password
    schoollink = school.lower() + '.no'
    user = get_users()
    if user:
        try:
            user = user[school]
        except KeyError:
            print "No login information for school %s" % school
            return None, None
    else:
        print "No users specified"
        return None, None

    # Starting the logon prosedure: still at studweb
    br.select_form('feideForm')
    response = br.submit()
    # Now at feide logon site
    br.select_form(nr=0)
    # Finding the dropdown menu, and choosing the right school
    control = br.form.find_control('org')
    for item in control.items:
        if item.name == schoollink:
            item.selected = True
    response = br.submit()

    # On next page where username and password should be entered
    br.select_form(nr=0)
    br.form['feidename'] = user[0]
    br.form['password'] = user[1]
    response = br.submit()
    br.select_form(nr=0)
    response = br.submit()

    # Testing if we are logged in
    if '<div id="errorframe"><p>Pålogging feilet. Dette kan skyldes feil brukernavn eller passord' in response.get_data():
        print "Login with feide failed. This can be the result of bad username/password, or that your account has expired."
        print "Please check the configuration feide.conf to ensure that correct creditentials are presented"
        return None, None

    if 'For å fullføre innloggingen må du godta at opplysningene' in response.get_data():
        print "You need to logon in a browser first, to accept that personal information is shared with studweb."
        return None, None
    if '<b>Jeg får ikke logget inn</b>' in response.get_data():
        print "Login was not successfull. Yo may need to login with a browser first."
        return None, None

    # Here we assume that we get a successfull login, and that evrything is in order
    return response, br

if __name__ == '__main__':
    print get_users()
