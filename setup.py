#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name = "qclient",
    version = "0.1",
    description = "qingcloud client",

    packages=['qclient'],

    install_requires = ["requests"],
    zip_safe=False
)

