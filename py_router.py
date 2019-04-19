def create(*rules):
    routes, handlers = create_routes_and_handlers(*rules)
    scope = {}
    exec(compile(create_dispatch_src(routes), '<string>', 'exec'), scope)

    return lambda url: scope['dispatch'](url.strip('/').split('/'), handlers)


def create_routes_and_handlers(*rules):
    routes = {}

    for i, uri_and_value in enumerate(rules):
        uri, value = uri_and_value
        parts = uri.strip('/').split('/')
        routes.setdefault(len(parts), [])
        routes[len(parts)].append((parts, i))

    return routes, tuple(r[1] for r in rules)


def create_dispatch_src(routes):
    tab = '    '
    src = ['def dispatch(path, handlers):', tab + 'length = len(path)']

    for length, optimised_routes in routes.items():
        src.append(tab + f'if length == {length}:')
        for parts, value in optimised_routes:
            if_start = 2 * tab + 'if '
            conditions = [f'path[{i}] == \'{part}\''
                          for i, part in enumerate(parts) if not part.startswith(':')]
            src.append(if_start + ' and '.join(conditions) + ':')

            dict_args = [f'\'{part[1:]}\': path[{i}]'
                         for i, part in enumerate(parts) if part.startswith(':')]
            returned_dict = '{' + ', '.join(dict_args) + '}'
            src.append(3 * tab + f'return handlers[{value}], {returned_dict}')

    src.append(tab + 'return None, {}')
    return '\n'.join(src)
