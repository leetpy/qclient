#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import yaml


def check_key(conf_obj, keys=None):
    if not keys:
        keys = [
                "qy_access_key_id",
                "qy_secret_access_key",
                "zone",
        ]

    for key in keys:
        if key not in conf_obj.keys():
            raise Exception("%s should in config file" % key)


def parse_config(cfg_path):
    if not os.path.isfile(cfg_path):
        raise Exception("config file %s does not exists" % cfg_path)
    with open(cfg_path, 'r') as fd:
        try:
            conf = yaml.load(fd, Loader=yaml.Loader)
        except Exception as e:
            print(e)
            conf = None

    if not conf:
        raise Exception("config file %s format error" % cfg_path)

    # make suer all necessary keys have been set
    check_key(conf)
    return conf



