#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *


# Publishing specifics

SITEURL = 'http://www.florentflament.com/blog'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

# This removes the previously generated content
DELETE_OUTPUT_DIRECTORY = True

DISQUS_SITENAME = "florentflament"
GOOGLE_ANALYTICS = "UA-23791515-4"
