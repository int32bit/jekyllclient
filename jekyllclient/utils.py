#!/usr/bin/python
#coding=utf-8
import prettytable
def arg(*args, **kwargs):
    """Decorator for CLI args.

    Example:

    >>> @arg("name", help="Name of the new entity")
    ... def entity_create(args):
    ...     pass
    """
    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func
    return _decorator
def add_arg(func, *args, **kwargs):
    """ Bind CLI arguments to a shell.py `do_foo` function."""
    if not hasattr(func, 'arguments'):
        func.arguments = []
    if (args, kwargs) not in func.arguments:
        func.arguments.insert(0, (args, kwargs))
def charAt(s, c, nth = 1):
    """ Find the nth index of char 'c' in the string 's' """
    for i in range(len(s)):
        if s[i] == c:
            count = count - 1
            if count == 0:
                return i
def print_list(objs, fields, formatters={}, sortby_index=None, reversesort = False, sort_key = None):
    print(fields)
    if sortby_index is None:
        sortby = None
    else:
        sortby = fields[sortby_index]
    pt = prettytable.PrettyTable([f for f in fields], caching=False)
    pt.align = 'l'
    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            else:
                field_name = field.lower().replace(' ', '_')
                data = getattr(o, field_name, '')
                if data is None:
                    data = '-'
                row.append(data)
        pt.add_row(row)
    if sortby is not None:
        if sort_key is not None:
            result = pt.get_string(sortby = sortby, reversesort = reversesort, sort_key = sort_key)
        else:
            result = pt.get_string(sortby = sortby, reversesort = reversesort)
    else:
        result = pt.get_string()
    print(result)
def getFiletype(ext):
    if ext is None or len(ext) == 0:
        return "undefine"
    if ext == '.md' or ext == '.markdown':
        return 'markdown'
    if ext == '.html':
        return 'html'
def getFileExt(filetype):
    if not filetype:
        return "md"
    if filetype == 'html':
        return 'html'
    return 'md'
def getMetadata(post):
    data = {}
    begin = False
    end = False
    with open(post) as f:
        for line in f:
            line = line.strip()
            if line == '---':
                if not begin:
                    begin = True
                else:
                    end = True
                continue
            if end:
                break
            else:
                split = line.split(":")
                key = split[0].strip()
                value = split[1].strip()
                data[key] = value
    return data
def parseList(strList):
    strList = strList.strip()
    if not strList:
        return list()
    strList = strList[1:-1]
    if strList:
        return strList.split(',')
    else:
        return list()
