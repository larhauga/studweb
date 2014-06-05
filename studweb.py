#!/usr/bin/env python
#-*- coding: utf-8 -*-


from mechanize import Browser
import feide_login
import pushnotify
import shelve
import config
import parse
import mail
import re


def main():
    br = Browser()
    br.set_handle_robots(False)
    br.set_handle_refresh(False)
    br.addheaders = config.USER_AGENT

    d = shelve.open("results.cache")

    for school in config.SCHOOLS:
        points, courses = crawl(br, config.BASE_URL + school, school)
        if config.VERBOSE:
            printstdout(school, points, courses)

        # We have data stored from before
        # We will check if for new courses
        # Data format: shelve: school = {points: num, courses: []}
        if school in d:
            try:
                c = new_courses(courses, d[school]['courses'])
            except:
                c = None
            if c:
                # Update stored courses and points
                d[school] = {} # Cleaning to be able to update
                d[school]['courses'] = courses
                d[school]['points'] = points

                # Notify if new courses and notifications are turned on
                if config.NOTIFY:
                    notify(c)
            else:
                # No data from before. Storing it
                data = {}
                data['points'] = points
                data['courses'] = courses
                d[school] = data
        else:
            # No data from before. Storing it
            data = {}
            data['points'] = points
            data['courses'] = courses
            d[school] = data
    d.close()


def crawl(br, page, school):
    response = br.open(page)
    if config.FEIDE:
        response, br = feide_login.browser_login(br, school)
    else:
        br.select_form("fnrForm")
        br.form['fodselsnr'] = config.LOGINID
        br.form['pinkode'] = config.PIN
        response = br.submit()  # Submit form and logg in

    if school == "HiOA":
        menuexpand = config.MENUCOL + 'Innsyn'
        selectgrade = config.MENUEXP + 'Resultater'
        logout = config.MENUEXP + 'Logg ut'
    elif school == "UiO":
        menuexpand = config.MENUCOL + 'Se opplysninger om deg'
        selectgrade = config.MENUEXP + 'Resultater'
        logout = config.MENUEXP + 'Logg ut'

    response = br.follow_link(text=menuexpand)   # Press the button "Innsyn"
    response = br.follow_link(text=selectgrade)  # Press the button "Resultater"

    if config.HIDEFAILED:
        response = br.select_form(nr=0)
        br.form['rbVurdFilter'] = ["true"]
        response = br.submit()
    br.follow_link(text=logout)
    return parse.parsepage(response.get_data())  # Get the grades


def printstdout(school, points, courses):
    print "Courses for %s:" % school
    for course in courses:
        if config.LIMITCOURSE and not re.compile(config.COURSEREGEX).match(course['course']):
            pass
        elif course['name']:
            print "%s, Grade: %s, %s, %s" % (course['name'], course['grade'], course['points'], course['semester'])
        elif course['grade'] and course['points']:
            print "Unknown course: %s, %s" % (course['grade'], course['points'])

    print "Total points: %s" % points
    # Printing the average grades (and hacking it into lettergrade)
    grades = {'5':'A', '4':'B', '3':'C', '2':'D', '1':'E', '0':'F'}
    average = parse.average_grade(courses)
    print "Average grade: %0.2f == %s\n" % (average, grades[str(average)[0]])

def notify(new_results):
    print "Notifying new courses"
    if config.NOTIFY_SERVICE == 'email':
        client = mail.mail()
    elif config.NOTIFY_SERVICE in ['nma', 'prowl', 'pushover']:
        client = pushnotify.get_client(config.NOTIFY_SERVICE, application='StudWeb')
        client.add_key(config.NOTIFY_APIKEY)

    text = "New exam results: "
    for result in new_results:
        text = text + "Course: %s, grade: %s; " % \
                (result.get('name', 'Unknown'), result.get('grade', 'Unknown'))
        if config.VERBOSE:
            print "Notiying new course %s" % result['name']
    client.notify(text, "New exam results")
    print ""

def new_courses(courses, stored_courses):
    """
        Checks for coursecodes allready existing
        Tobeimplemeted: checking if valid
    """
    new = []
    for course in courses:
        if not any(c['course'] == course['course'] for c in stored_courses):
            new.append(course)

    return new

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Exited..."
