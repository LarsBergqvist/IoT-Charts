#!/usr/bin/env python

import logging
import logging.handlers
import argparse
import sys

LOG_FILENAME = "/tmp/charts_server.log"
LOG_LEVEL = logging.DEBUG

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter(u'%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class STDLogger(object):
        def __init__(self, logger, level):
                self.logger = logger
                self.level = level

        def write(self, message):
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())
        def flush(self):
            pass
					

sys.stdout = STDLogger(logger, logging.INFO)
sys.stderr = STDLogger(logger, logging.INFO)