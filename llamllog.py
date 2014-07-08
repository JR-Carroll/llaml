#!/usr/bin/env python
#coding:utf-8
#llamllog.py

'''
  Author:   Justin Carroll--<jrc.csus@gmail.com>
  Purpose:  Logging Support for LLaML.
  Created: 7/4/2014
'''

import logging

_infoLevel =  {"LOW": logging.ERROR,
               "NORMAL": logging.INFO,
               "HIGH": logging.DEBUG
               }

LOGLEVEL = _infoLevel.get("HIGH")

# Setup logging facilities
logging.basicConfig(filename=".llamlLOG", filemode='a', level=LOGLEVEL,
                    format="%(asctime)s :: %(levelname)-8s %(module)-14s:: %(message)s")

logging.info("Logging module has formally started")