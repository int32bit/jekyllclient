#!/usr/bin/python
#coding=utf-8
import ConfigParser
import sys
import os
class Configuration(object):
    def __init__(self, path = "conf/blog.conf"):
        self.config = None
        with open(path) as f:
            self.config = ConfigParser.ConfigParser()
            self.config.readfp(f, "rb")
    def get(self, key, section = "site"):
        return self.config.get(section, key)
jekyll_conf = os.getenv("JEKYLL_CONF", sys.path[0] + "/conf/blog.conf")
CONF = Configuration(jekyll_conf)
