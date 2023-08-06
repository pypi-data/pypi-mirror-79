from .utils import MAXIMUM_DISTANCE, find_closest_result, remove_empty_values
import hestia_earth.bibliography_apis.wos_rest.client as wos_rest_client
import hestia_earth.bibliography_apis.wos_soap.client as wos_soap_client


def extend_wos(titles, **kwargs):
    api_key = kwargs.get('wos_api_key')
    api_user = kwargs.get('wos_api_user')
    api_password = kwargs.get('wos_api_pwd')
    wos_client = wos_rest_client if api_key else wos_soap_client
    searcher = wos_client.exec_search(api_key) if api_key else wos_client.exec_search(api_user, api_password)

    queries = {}
    bibliographies = []
    actors = []

    for title in titles:
        if len(title) > 0:
            [item, distance] = find_closest_result(queries, title, searcher)
            (biblio, authors) = wos_client.create_biblio(title, item if distance <= MAXIMUM_DISTANCE else None)
            bibliographies.extend([] if biblio is None else [biblio])
            actors.extend([] if authors is None else authors)

    return (remove_empty_values(actors), remove_empty_values(bibliographies))
