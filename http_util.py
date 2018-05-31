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


def get_signature(string_to_sign, conf):
    secret_access_key = conf.get('qy_secret_access_key')
    h = hmac.new(secret_access_key, digestmod=sha256)
    h.update(string_to_sign)
    sign = base64.b64encode(h.digest()).strip()
    signature = urllib.quote_plus(sign)
    return signature

def update_params(params, conf):
    params['zone'] = conf['zone']
    params['access_key_id'] = conf['qy_access_key_id']
    params['time_stamp'] = get_ts()
    params['signature_method'] = "HmacSHA256"
    params['signature_version'] = 1


def send_http(url, params, conf, method='GET'):
    update_params(params, conf)
    string_to_sign = "%s\n/%s/\n" % (method, 'iaas')
    keys = sorted(params.keys())
    pairs = []
    for key in keys:
        val = get_utf8_value(params[key])
        pairs.append(urllib.quote(key, safe='') + '=' +
                     urllib.quote(val, safe='-_~'))
    query_string = '&'.join(pairs)
    string_to_sign += query_string
    signature = get_signature(string_to_sign, conf)
    request_url = '{}?{}&signature={}'.format(url, query_string, signature)
    r = requests.get(request_url)
    print r.text
