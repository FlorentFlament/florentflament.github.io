#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Florent Flament'
SITENAME = u"Florent Flament's Tech Blog"
SITEURL = 'http://www.florentflament.com/blog'

STATIC_PATHS = ['images', 'static']

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (
    ("Adam Young's Web Log", "http://adam.younglogic.com/"),
    ("Chmouel's Blog", "http://blog.chmouel.com/"),
    ("Cloudwatt's Tech Blog", "http://dev.cloudwatt.com/en/blog/"),
    ("Jamie Lennox's Blog", "http://www.jamielennox.net/"),
    ("Loïc Dachary's Blog", "http://dachary.org/"),
)

# Social widget
SOCIAL = None # (('Social links to come', '#'),)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = "theme/"
