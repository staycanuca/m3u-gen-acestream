﻿#!/usr/bin/python3
# -*- coding: UTF-8 -*-


# Address used to check internet connection:
CONN_CHECK_ADDR = 'http://google.com'

# Delay between requests to the internet connection check address (in seconds):
CONN_CHECK_REQ_DELAY = 30

# Delay between processing each data set (in seconds):
DATA_SET_DELAY = 5

# Delay between playlist updates (in seconds):
UPDATE_DELAY = 60 * 60

# Delay between requests to the JSON source host if it is currently down (in seconds):
JSON_SRC_REQ_DELAY = 60 * 10

# Amount of requests to the JSON source host before throw an exception if it is currently down:
JSON_SRC_MAX_ATTEMPTS = 10

# Time to wait before consider that destination is unreachable (in seconds):
CONN_TIMEOUT = 10

# Send email on program crash or not:
MAIL_ON_CRASH = False

# Send email from:
# Note: To use this feature with gmail, enable 'less secure apps' on the sender account.
# See: https://myaccount.google.com/lesssecureapps
MAIL_FROM = 'from.email.address@domain.com'

# Send email to:
MAIL_TO = 'to.email.address@domain.com'

# SMTP server address:
SMTP_ADDR = 'smtp.gmail.com:587'

# SMTP server login:
SMTP_LOGIN = 'my.email.login'

# SMTP server password:
SMTP_PWD = 'my.email.password'

# Ask to press <Enter> on program crash to exit or not:
PAUSE_ON_CRASH = True

# noinspection SpellCheckingInspection
# Data sets used to generate m3u files:
DATA_SETS = (
    # TTV, all:
    {
        # Source JSON file URL:
        # Response example:
        # {
        #   "channels": [
        #     {
        #       "name": "2x2 (+2)",
        #       "url": "55025502b66f3a1d637fe22ed1ca54cfa2b255c3",
        #       "cat": "Развлекательные"
        #     },
        #     {
        #       "name": "AMC",
        #       "url": "adee14686e77e169b3622d10cc0e66ac84f09e1d",
        #       "cat": "Фильмы"
        #     },
        #
        #     ...
        #
        #     {
        #       "name": "Super Tennis HD",
        #       "url": "4468f2698f66674f30044903fc8cadc80ebe181f",
        #       "cat": "Спорт"
        #     }
        #   ]
        # }
        'JSON_URL': 'http://91.92.66.82/trash/ttv-list/ttv.json',

        # JSON response encoding:
        'RESP_ENCODING': 'UTF-8-SIG',

        # Output file name:
        'OUT_FILE_NAME': './acestream-ttv-all.m3u',

        # Output file encoding:
        'OUT_FILE_ENCODING': 'UTF-8',

        # Output file first line:
        'OUT_FILE_FIRST_LINE': '#EXTM3U url-tvg="http://1ttvapi.top/ttv.xmltv.xml.gz" tvg-shift=0 deinterlace=1 '
                               'm3uautoload=1 cache=3000\r\n',

        # Output file format:
        'OUT_FILE_FORMAT': '#EXTINF:-1 group-title="{CATEGORY}",{NAME}\r\n'
                           'http://127.0.0.1:6878/ace/getstream?id={CONTENT_ID}\r\n',

        # Categories that needs to be changed (channel names uses regex):
        # Format: 'CHANNEL_NAME': 'CATEGORY_TO_SET':
        'REPLACE_CATS': {
        },

        # Categories blacklist (uses regex):
        'EXCLUDE_CATS': (
        ),

        # Channel names blacklist (uses regex):
        'EXCLUDE_NAMES': (
        ),
    },
)