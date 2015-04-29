#!/usr/bin/python
#coding=utf-8
class Post(object):
    def __init__(self, title = None, date = None, filetype = None, comments=True, layout='post',category = 'unclassified', tags = ['None']):
        self.title = title
        self.date = date
        self.comments = comments
        self.layout = layout
        self.category = category
        self.tags = tags
        self.filetype = filetype
