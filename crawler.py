#!/usr/bin/env python
#-*- coding: utf-8 -*-


from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import re
import config, parse

def main():
    br = Browser()
    br.set_handle_robots(False)
    br.set_handle_refresh(False)
    br.addheaders = config.USER_AGENT

    for school in config.SCHOOLS:
        points, courses = crawl(br, config.BASE_URL + school, school)
        printstdout(points, courses)

        # Based upon 'studiepoeng' we can find out if there are any new grades.
        # New grade - old grades => print the new grades (assuming they are on top)

def crawl(br, page, school):
    response = br.open(page)
    br.select_form("fnrForm")
    br.form['fodselsnr'] = config.LOGINID
    br.form['pinkode']  = config.PIN
    response = br.submit()  # Submit form and logg in

    if school == "HiOA":
        menuexpand  = config.MENUCOL + 'Innsyn'
        selectgrade = config.MENUEXP + 'Resultater'
        logout = config.MENUEXP + 'Logg ut'
    elif school == "UiO":
        menuexpand  = config.MENUCOL + 'Se opplysninger om deg'
        selectgrade = config.MENUEXP + 'Resultater'
        logout = config.MENUEXP + 'Logg ut'

    response = br.follow_link(text=menuexpand)  # Press the button "Innsyn"
    response = br.follow_link(text=selectgrade) # Press the button "Resultater"
    br.follow_link(text=logout)
    return parse.parsepage(response.get_data()) # Get the grades

def printstdout(points, courses):
    # "https://www.studweb.no/as/WebObjects/studentweb2?inst=HiOA"
    #response = br.open(config.BASE_URL + "UiO") #config.SCHOOLS[0])

    print points
    #print courses
    for course in courses:
        if course['name']:
            print "%s, Grade:\t %s, %s, %s" % (course['name'], course['grade'], course['points'], course['semester'])
        elif course['grade'] and course['points']:
            print "Unknown course: %s, %s" % (course['grade'], course['points'])

    print "Average grade: %f" % (parse.average_grade(courses))

if __name__ == '__main__':
    main()
