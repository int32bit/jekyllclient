#!/usr/bin/python
#coding=utf-8
import ConfigParser
import sys
class Configuration(object):
    def __init__(self, path = "conf/blog.conf"):
        self.config = None
        with open(path) as f:
            self.config = ConfigParser.ConfigParser()
            self.config.readfp(f, "rb")
    def get(self, key, section = "site"):
        return self.config.get(section, key)
CONF = Configuration(sys.path[0] + "/conf/blog.conf")
