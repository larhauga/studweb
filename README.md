# Studweb web scraper
This is a web scraper that use the Python implementation of Mechanize to
crawl the Norwegian student webpage for higher education. This will
scrape the grades from the courses that have been taken, and can be used
to notify the student when new grades are out.

This script supports multiple school, and can filter out the courses.
If you are taking multiple bachelor's or a bachelor and a masters,
you can filter the results as to only count the current courses.

This script supports notification through push services like
*NotifyMyAndroid* (NMA), *Prowl*, and *pushover*.

## Getting started
To get started. Copy the *config_sample.py* to *config.py*
and edit it to your preferences.

Using virtualenv's load in the requirements.txt.
`pip install -r requirements.txt`
