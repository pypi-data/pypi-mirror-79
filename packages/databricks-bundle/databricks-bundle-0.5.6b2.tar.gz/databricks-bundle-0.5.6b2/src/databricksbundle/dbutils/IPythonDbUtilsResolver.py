def resolveDbUtils():
    g = globals()

    if 'dbutils' not in g:
        raise Exception('dbutils cannot be resolved')

    return g['dbutils']
