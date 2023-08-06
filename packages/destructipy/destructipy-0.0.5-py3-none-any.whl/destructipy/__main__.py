from json import dump
from os import listdir
from os.path import isdir, islink, relpath
from . import get_tokens, get_line, get_keys


def listdir_recursive(path):
    files = []
    for item in listdir(path):
        item = '%s/%s' % (path, item)
        if islink(item):
            continue
        if isdir(item):
            files.extend(listdir_recursive(item))
        else:
            files.append(relpath(item))
    return files


def gen_cache(file):
    with open(file) as file:
        source = file.read().splitlines()

    tokens = get_tokens(source)
    if not tokens: return

    cache = {}
    for lineidx, line in enumerate(source):
        line = get_line(lineidx, line, source)
        if tokens[0] in line or tokens[1] in line:
            cache[lineidx + 1] = get_keys(line, tokens)
    return cache


cache = {}
for file in listdir_recursive('.'):
    if file.endswith('.py'):
        _cache = gen_cache(file)
        if _cache:
            cache[file] = _cache

with open('.destructipy', 'w') as file:
    dump(cache, file)
