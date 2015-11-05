# -*- coding: utf-8 -*-

# Scrapy settings for funtv project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'funtv'

SPIDER_MODULES = ['funtv.spiders']
NEWSPIDER_MODULE = 'funtv.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'funtv (+http://www.yourdomain.com)'


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'spiders'))