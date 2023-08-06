from json import load
from os import getcwd
from sys import _getframe
from os.path import isabs, abspath, relpath
from operator import attrgetter, itemgetter
from linecache import getline, cache as source_cache

cwd = getcwd()
funcs_cache = {}
keys_cache = {}


def get_tokens(source):
    token = 'fromdestructipyimport_as'
    for line in source:
        line = line.replace(' ', '')
        if token in line:
            token = line.split(token)[1].split(';')[0].strip()
            return '=%s(' % token, '=%s.' % token


def get_line(lineidx, line, source):
    while 1:
        _line = source[lineidx - 1].strip()
        if not _line.endswith('\\'): break
        _line = _line.replace('\\', '')
        line = '%s%s' % (_line, line)
        lineidx -= 1
    return line.replace(' ', '')


def get_keys(line, tokens):
    return line.split(tokens[tokens[1] in line])[0].split(';')[-1].split(',')


def get_funcs(frame):
    lineno = frame.f_lineno
    funcs = funcs_cache.get((frame, lineno))
    if not funcs:
        filename = frame.f_code.co_filename
        if not isabs(filename):
            filename = abspath('%s/%s' % (cwd, filename))
        line = getline(filename, lineno)
        if line:
            source = source_cache[filename][2]
            tokens = get_tokens(source)
            line = get_line(lineno - 1, line, source)
            keys = get_keys(line, tokens)
        else:
            if not keys_cache:
                with open('%s/.destructipy' % cwd) as file:
                    keys_cache.update(load(file))
            keys = keys_cache[relpath(filename, cwd)][str(lineno)]
        funcs_cache[frame, lineno] = funcs = attrgetter(*keys), itemgetter(*keys)
    return funcs


_ = lambda _: get_funcs(_getframe(1))[hasattr(_, '__getitem__')](_)
_.attr = _.a = lambda a: get_funcs(_getframe(1))[0](a)
_.item = _.i = lambda i: get_funcs(_getframe(1))[1](i)
