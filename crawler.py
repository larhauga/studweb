#!/usr/bin/env python
#-*- coding: utf-8 -*-


from mechanize import Browser
import pushnotify
import shelve
import config
import parse


def main():
    br = Browser()
    br.set_handle_robots(False)
    br.set_handle_refresh(False)
    br.addheaders = config.USER_AGENT

    client = pushnotify.get_client(config.NOTIFY_SERVICE,
                                   application='StudWeb')
    client.add_key(config.NOTIFY_APIKEY)
    d = shelve.open("results.cache")

    for school in config.SCHOOLS:
        points, courses = crawl(br, config.BASE_URL + school, school)
        if config.VERBOSE:
            printstdout(points, courses)
            print "Total points: %s" % points
        # We have points stored before
        # so lets see if they are different from what we got now.
        if school in d:
            if d[school] != points:
                d[school] = points
                if config.NOTIFY:
                    client.notify("Exam results are in, latest course: %s, grade: %s" % (courses[0].get('name', "Unknown"), courses[0].get('grade', 'Unknown')), "New exam results")
        # No points stored before, so let's just store them.
        else:
            d[school] = points
    d.close()


def crawl(br, page, school):
    response = br.open(page)
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
    br.follow_link(text=logout)
    return parse.parsepage(response.get_data())  # Get the grades


def printstdout(points, courses):
    for course in courses:
        if course['name']:
            print "%s, Grade:\t %s, %s, %s" % (course['name'], course['grade'], course['points'], course['semester'])
        elif course['grade'] and course['points']:
            print "Unknown course: %s, %s" % (course['grade'], course['points'])

    print "Average grade: %f" % (parse.average_grade(courses))

if __name__ == '__main__':
    main()
