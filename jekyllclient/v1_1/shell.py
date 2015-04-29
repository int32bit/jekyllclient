#!/usr/bin/python
#coding=utf-8
from __future__ import print_function
import sys
import time
import glob
import os

from jekyllclient import utils
from jekyllclient.post import Post
from jekyllclient.config import CONF

@utils.arg('--disable-comments',
        dest='comments',
        action='store_false',
        help='the layout of the new blog',
        )
@utils.arg('-t', '--title',
        dest='title',
        metavar='<title>',
        help='the title of the new blog',
        )
@utils.arg('-c','--category',
        dest='category',
        metavar='<category>',
        help='the category of the new blog',
        default='unclassified',
        )
@utils.arg('-T','--tags',
        dest='tags',
        metavar='<tags>',
        help='the tags of the new blog',
        default='None',
        )
@utils.arg('--layout',
        dest='layout',
        metavar='<layout>',
        help='the layout of the new blog',
        default='post',
        )
@utils.arg('--filetype',
        dest='filetype',
        metavar='<filetype>',
        help='the filetype of the new blog',
        default='markdown',
        )
def do_create(args):
    """Create a new post."""
    if not args.title:
        meta = _get_meta_interactive()
    else:
        meta = _get_meta_from_args(args)
    title = meta['title']
    ext = utils.getFileExt(args.filetype)
    date = "{0}-{1:0>2}-{2:0>2}".format(*(time.localtime()[:3]))
    target = "{0}-{1}.{2}".format(date, title, ext)
    path = "{0}/{1}/{2}".format(CONF.get("base"), CONF.get("posts"), target)
    meta['tags'] = meta['tags'].strip().split(',')
    with open(path, mode = "w") as f:
        f.writelines("---\n")
        for key in meta.keys():
            f.writelines("%s: %s\n" % (key, meta[key]))
        f.writelines("---\n")
    editor = os.getenv("EDITOR", "vim")
    return os.system("%s %s" % (editor, path))
def _get_meta_from_args(args):
    meta = {}
    meta['title'] = args.title
    meta['category'] = args.category
    meta['tags'] = args.tags.strip().split(",")
    meta['layout'] = args.layout
    meta['comments'] = str(args.comments).lower()
    meta['filetype'] = str(args.filetype).tolower()
    return meta
def _get_meta_interactive():
    meta = {}
    while not meta.get('title', None):
        meta['title'] = raw_input("title:").strip()
    meta['category'] = raw_input("category[default 'Unclassified'] : ").strip() or 'Unclassified'
    meta['tags'] = raw_input("comma-separated list of tags[default 'None']: ").strip() or 'None'
    meta['layout'] = raw_input("layout[default 'post']: ").strip() or 'post'
    meta['comments'] = raw_input("layout[default 'true']: ").strip() or 'true'
    return meta

@utils.arg('-d','--details',
        dest='details',
        help='get more detail of posts if this flags set',
        action='store_true',
        default=False,
        )
def do_list(args):
    """List all the posts."""
    if args.details:
        _do_list_details(args)
    else:
        _do_list_simple(args)
def _do_list_simple(args):
    base = CONF.get("base")
    posts_path = CONF.get("posts")
    posts = []
    for filename in os.listdir(base + "/" + posts_path):
        filename, ext = os.path.splitext(filename.strip())
        filetype = utils.getFiletype(ext)
        pos = utils.charAt(filename, '-', 3)
        title = filename[pos + 1:]
        date = filename[:pos]
        posts.append(Post(title, date, filetype = filetype))
    utils.print_list(posts, ["title", "filetype", "date"], sortby_index = 2, reversesort = True)
def _do_list_details(args):
    base = CONF.get("base")
    posts_path = CONF.get("posts")
    posts = []
    for filename in os.listdir(base + "/" + posts_path):
        meta = utils.getMetadata(base + "/" + posts_path + "/" + filename)
        title = meta['title']
        del meta['title']
        #tags = utils.parseList(meta.get('tags', ''))
        #meta['tags'] = tags
        meta['tags'] = meta['tags'].strip().strip('[]') # strip [ ]
        filename, ext = os.path.splitext(filename.strip())
        filetype = utils.getFiletype(ext)
        pos = utils.charAt(filename, '-', 3)
        date = filename[:pos]
        meta["filetype"] = filetype
        fields = ["title", "date"]
        fields.extend(meta.keys())
        posts.append(Post(title = title, date = date, **meta))
    utils.print_list(posts, fields = fields)
    utils.print_list(posts, fields = fields, sortby_index = fields.index('date'), reversesort = True)
@utils.arg('-d','--details',
        dest='details',
        help='get more detail of posts if this flags set',
        action='store_true',
        default=False,
        )
def do_ls(args):
    """Equivalent to list."""
    do_list(args)
def do_delete(args):
    """ Delete specified post."""
    pass
@utils.arg('-t', '--title',
        dest='title',
        metavar='<title>',
        help='the title of the post to show',
        required = True,
        )
@utils.arg('-s', '--style',
        metavar='<style>',
        help='the style to show, choice from \'cat, less, more\'',
        )
def do_show(args):
    """ Read a Post """
    base = CONF.get("base")
    posts_path = CONF.get("posts")
    path = base + "/" + posts_path + "/*%s*" % args.title
    begin = False
    end = False
    fileset = glob.glob(path)
    style = args.style
    if len(fileset) == 0:
        print("The file '%s' not found!" % args.title, file = sys.stderr)
        return 1
    for f in fileset:
        if style in ['cat', 'less', 'more']:
            _do_show_with_reader(style, f)
        else:
            _do_show_with_io(f)
def _do_show_with_reader(reader, path):
    os.system("%s %s" % (reader, path))
def _do_show_with_io(path):
    with open(path, "r") as f:
        for line in f:
            print(line.strip())
