#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import hmac
import requests
import time
import urllib
from hashlib import sha256


def get_ts(ts=None):
    ISO8601 = '%Y-%m-%dT%H:%M:%SZ'
    if not ts:
        ts = time.gmtime()
    return time.strftime(ISO8601, ts)


def get_utf8_value(value):
    if isinstance(value, unicode):
        return value.encode('utf-8')
    if not isinstance(value, str):
        return str(value)
    return value


def get_signature(string_to_sign):
    h = hmac.new(secret_access_key, digestmod=sha256)
    h.update(string_to_sign)
    sign = base64.b64encode(h.digest()).strip()
    signature = urllib.quote_plus(sign)
    return signature


def send_http(url):
    r = requests.get(url)
    return r.text