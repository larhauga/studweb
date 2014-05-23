#!/usr/bin/env python
#-*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from collections import defaultdict
import re
import config

def parsepage(data):
    soup    = BeautifulSoup(data)
    points  =  soup.findAll(attrs={'class': 'sum-r'})[0].text.split(',')[0]
    courses = []

    for tr in soup.findAll(attrs={'class': re.compile(r"pysj\d{1}")}):
        courses.append([ x.text.strip() if x is not None else '' for x in tr.findAll('td')]) # Parses the table

    return points, courses

def course_to_dict(courses):
    course = []
    for item in courses:
        if config.LIMITCOURSE and re.compile(config.COURSEREGEX).match(item[1]):
            course.append(create_item_dict(item))
        elif not config.LIMITCOURSE:
            course.append(create_item_dict(item))

    return course

def create_item_dict(item):
    c = defaultdict(str)
    c['semester']       = item[0]
    c['course']         = item[1]
    c['name']           = item[2]
    c['studyway']       = item[3]
    c['assessment']     = item[4]
    c['exam_date']      = item[5]
    c['candidatenr']    = item[6]
    c['grade']          = item[7]
    c['points']         = item[8].split(',')[0]
    return c

def average_grade(courses, from_year=None, to_year=None):
    grades = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1 }
    # <study points> * <grade> + (..repeat..) / <total studypoints>
    gpp = 0
    points = 0
    for course in courses:
        if not re.compile(config.COURSEREGEX).match(course['course']):
            pass
        elif course['points']:
            gpp += float(grades[course['grade']]) * float(course['points'])
            points += float(course['points'])

    return float(gpp / points)
