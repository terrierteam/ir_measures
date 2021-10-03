# These libraries can add a bunch of overhead when imported -- which is bad for command line
# utilities. This file loads them lazily if they are needed.
_cache = {}

def pandas():
    if 'pandas' not in _cache:
        import pandas
        _cache['pandas'] = pandas
    return _cache['pandas']
