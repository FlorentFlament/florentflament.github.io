#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Florent Flament'
SITENAME = u"Florent Flament 2 cents"
SITEURL = '' # Empty site for development purpose

PATH = 'content'
STATIC_PATHS = ['images', 'static']

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True


# Using m.css pelican theme
# see: https://mcss.mosra.cz/themes/pelican/

THEME = 'm.css/pelican-theme'
THEME_STATIC_DIR = 'static'
DIRECT_TEMPLATES = ['index']

M_CSS_FILES = ['https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600',
               '/static/m-dark.css']
M_THEME_COLOR = '#22272e'
M_HIDE_ARTICLE_SUMMARY = True

PLUGIN_PATHS = ['m.css/plugins']
PLUGINS = ['m.htmlsanity']
