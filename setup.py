#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import platform
from setuptools import setup, find_packages

config_sample = '''
qy_access_key_id: 'QINGCLOUDACCESSKEYID'
qy_secret_access_key: 'QINGCLOUDSECRETACCESSKEYEXAMPLE'
zone: 'ZONEID'
'''

def is_windows():
    return platform.system().lower() == 'windows'

def prepare_config_file():
    config_file = os.path.expanduser('~/.qingcloud/config.yaml')
    if os.path.exists(config_file):
        return

    d = os.path.dirname(config_file)
    if not os.path.exists(d):
        os.makedirs(d)

    with open(config_file, 'w') as fd:
        fd.write(config_sample)


setup(
    name = 'qclient',
    version = '0.1',
    description = 'Command Line Interface for QingCloud.',
    long_description = open('README.rst', 'rb').read().decode('utf-8'),
    keywords = 'qingcloud iaas qingstor cli',
    scripts=["cmd/qclient"],
    packages = find_packages('.'),
    package_dir = {'qingcloud-cli': 'client'},
    namespace_packages = ['qclient'],
    include_package_data = True,
    install_requires = [
        'argparse>=1.1',
        'PyYAML>=3.1',
        'requests',
    ]
)

if len(sys.argv) >= 2 and sys.argv[1] == 'install':
    prepare_config_file()
