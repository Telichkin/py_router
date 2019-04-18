def create_router(*rules):
    routes, handlers = create_routes_and_handlers(*rules)
    scope = {}
    exec(compile(create_dispatch_src(routes), '<string>', 'exec'), scope)

    def dispatch_fn(url):
        return scope['dispatch'](url.strip('/').split('/'), handlers)

    return dispatch_fn


def create_routes_and_handlers(*rules):
    routes = {}

    for i, uri_and_value in enumerate(rules):
        uri, value = uri_and_value
        parts = uri.strip('/').split('/')
        dynamic_parts = {}

        for part in parts:
            part_is_dynamic = part.startswith('<') and part.endswith('>')
            if part_is_dynamic:
                dynamic_parts[part] = part[1:-1]

        routes.setdefault(len(parts), [])
        routes[len(parts)].append((parts, dynamic_parts, i))

    return routes, tuple(r[1] for r in rules)


def create_dispatch_src(routes):
    tab = '    '

    nest_level = 1
    src = ['', 'def dispatch(path, handlers):', tab + 'length = len(path)']

    for length, r_list in routes.items():
        src.append(f'{nest_level * tab}if length == {length}:')
        nest_level += 1
        for parts, dynamic_parts, value in r_list:
            if_start = f'{nest_level * tab}if '
            conditions = [f'path[{i}] == \'{part}\''
                          for i, part in enumerate(parts) if part not in dynamic_parts]
            dict_args = [f'\'{dynamic_parts[part]}\': path[{i}]'
                         for i, part in enumerate(parts) if part in dynamic_parts]
            returned_dict = '{' + ', '.join(dict_args) + '}'
            src.append(if_start + ' and '.join(conditions) + ':')

            nest_level += 1
            src.append(f'{nest_level * tab}return handlers[{value}], {returned_dict}')

            nest_level -= 1

        nest_level -= 1

    src.append(tab + 'return None, {}\n')
    return '\n'.join(src)
