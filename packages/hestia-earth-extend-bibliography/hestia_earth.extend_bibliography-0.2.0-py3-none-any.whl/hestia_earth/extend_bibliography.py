from functools import reduce
from hestia_earth.schema import NodeType, Bibliography

from .bibliography_apis.utils import unique_values
from .bibliography_apis.crossref import extend_crossref
from .bibliography_apis.mendeley import extend_mendeley
from .bibliography_apis.wos import extend_wos


def is_node_of(node_type: NodeType):
    def check_type(node: dict):
        return 'type' in node.keys() and node['type'] == node_type.value
    return check_type


def update_source(source: dict, bibliographies: list):
    def update_key(key: str):
        value = source.get(key)
        biblio = next((x for x in bibliographies if value and value.get('title') == x['originalTitle']), None)
        if biblio and biblio.get('name'):
            source['name'] = biblio.get('name') if key == 'bibliography' else source.get('name')
            source[key] = {**source[key], **biblio}
            del source[key]['originalTitle']

    update_key('bibliography')
    update_key('metaAnalysisBibliography')
    return source


def need_update_source(node: dict):
    def has_title(key: str): return key in node and 'title' in node.get(key)

    return is_node_of(NodeType.SOURCE)(node) and (has_title('bibliography') or has_title('metaAnalysisBibliography'))


def update_node(bibliographies: list):
    def update_single_node(node):
        if isinstance(node, list):
            return list(reduce(lambda p, x: p + [update_single_node(x)], node, []))
        elif isinstance(node, dict):
            node = update_source(node, bibliographies) if need_update_source(node) else node
            list(map(update_single_node, node.values()))
        return node
    return update_single_node


def get_node_citation(node: dict):
    required = Bibliography().required
    required_values = list(filter(lambda x: node.get(x) is not None, required))
    return None if len(required_values) == len(required) else node.get('title')


def get_titles_from_node(node: dict):
    title = get_node_citation(node)
    return list(reduce(lambda x, y: x + get_citations(y), node.values(), [] if title is None else [title]))


def get_citations(nodes):
    if isinstance(nodes, list):
        return list(reduce(lambda p, x: p + get_citations(x), nodes, []))
    elif isinstance(nodes, dict):
        return get_titles_from_node(nodes)
    else:
        return []


def has_key(key: str, **kwargs): return key in kwargs and kwargs.get(key) is not None


def is_enabled(key: str, **kwargs): return key in kwargs and kwargs.get(key) is True


def extend(content, **kwargs):
    nodes = content.get('nodes') if 'nodes' in content else []

    actors = []
    bibliographies = []

    if has_key('mendeley_username', **kwargs):
        (actors, bibliographies) = extend_mendeley(get_citations(nodes), **kwargs)
        actors.extend([] if actors is None else actors)
        bibliographies.extend([] if bibliographies is None else bibliographies)

    if has_key('wos_api_key', **kwargs) or (has_key('wos_api_user', **kwargs) and has_key('wos_api_pwd', **kwargs)):
        (actors, bibliographies) = extend_wos(get_citations(nodes), **kwargs)
        actors.extend([] if actors is None else actors)
        bibliographies.extend([] if bibliographies is None else bibliographies)

    if is_enabled('enable_crossref', **kwargs):
        (actors, bibliographies) = extend_crossref(get_citations(nodes), **kwargs)
        actors.extend([] if actors is None else actors)
        bibliographies.extend([] if bibliographies is None else bibliographies)

    nodes = unique_values(actors) + list(map(update_node(bibliographies), nodes))
    return {'nodes': nodes}
