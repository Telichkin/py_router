from py_router import create_routes_and_handlers, create_dispatch_src, create


def test_routes_and_handlers_creation():
    routes, handlers = create_routes_and_handlers(
        ('foo', 'handler 1'),
        ('/bar', 'handler 2'),
        ('/foo/bar/', 'handler 3'),
        ('/foo/:name/bar/baz', 'handler 4'))

    assert routes == {
        1: [(['foo'], 0), (['bar'], 1)],
        2: [(['foo', 'bar'], 2)],
        4: [(['foo', ':name', 'bar', 'baz'], 3)]}

    assert handlers == ('handler 1', 'handler 2', 'handler 3', 'handler 4')


def test_dispatch_src_creation():
    src = create_dispatch_src({
        1: [(['foo'], 0), (['bar'], 1)],
        2: [(['foo', 'bar'], 2)],
        4: [(['foo', ':name', ':id', 'baz'], 3)]})

    expected = '''
def dispatch(path, handlers):
    length = len(path)
    if length == 1:
        if path[0] == 'foo':
            return handlers[0], {}
        if path[0] == 'bar':
            return handlers[1], {}
    if length == 2:
        if path[0] == 'foo' and path[1] == 'bar':
            return handlers[2], {}
    if length == 4:
        if path[0] == 'foo' and path[3] == 'baz':
            return handlers[3], {'name': path[1], 'id': path[2]}
    return None, {}
'''.strip('\n')

    assert src == expected


def test_router_creation():
    r = create(
        ('foo', 'handler 1'),
        ('/foo/:name/bar', 'handler 2'))

    assert r('/foo/') == ('handler 1', {})
    assert r('/foo/example/bar') == ('handler 2', {'name': 'example'})
    assert r('not/exists/len/uri') == (None, {})
