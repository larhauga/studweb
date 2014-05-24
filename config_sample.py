#!/usr/bin/env python

# Username
LOGINID = '<changeme>'
# Pincode
PIN = '<changeme>'
# Regex of the different course codes which you want to include
COURSEREGEX = 'MS\d{3}A|INF\d{4}NSA' # Change me to your courses. Normal regex
# The schools which should be scraped.
SCHOOLS = ['HiOA', 'UiO'] # Case sensitive

# The url to studweb
BASE_URL = "https://www.studweb.no/as/WebObjects/studentweb2?inst="
# Custom user agent
USER_AGENT = [('User-agent', 'Mozilla/5.0 (Windows NT 6.0; rv:27.0) Gecko/20100101 Firefox/27.0')]
# To limit to the courses specified in the regex or not
LIMITCOURSE = False
# Menu collapsed (its a plus)
MENUCOL="[+][IMG]\xa0"
# Menu expanded
MENUEXP="[ ][IMG]\xa0"
# Send notification when points are updated
NOTIFY = True
# Service to notify your phone with. Valid types are 'nma' 'prowl', and 'pushover'
# for Notify My Android, Prowl, and Pushover clients, respectively.
NOTIFY_SERVICE = "nma"
# API key for that service
NOTIFY_APIKEY = "<key>"
# Print to stdout
VERBOSE = True
