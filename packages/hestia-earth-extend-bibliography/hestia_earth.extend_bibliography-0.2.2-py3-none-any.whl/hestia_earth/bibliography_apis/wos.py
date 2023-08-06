import traceback

from .utils import has_key, MAXIMUM_DISTANCE, find_closest_result, remove_empty_values
import hestia_earth.bibliography_apis.wos_rest.client as wos_rest_client
import hestia_earth.bibliography_apis.wos_soap.client as wos_soap_client


def extend_wos(titles, **kwargs):
    try:
        wos_client = wos_rest_client if has_key('wos_api_key', **kwargs) else wos_soap_client
        queries = {}
        bibliographies = []
        actors = []

        with wos_client.get_client(**kwargs) as client:
            searcher = wos_client.exec_search(client)
            for title in list(filter(lambda x: len(x) > 0, titles)):
                [item, distance] = find_closest_result(queries, title, searcher)
                (biblio, authors) = wos_client.create_biblio(title, item if distance <= MAXIMUM_DISTANCE else None)
                bibliographies.extend([] if biblio is None else [biblio])
                actors.extend([] if authors is None else authors)
        return (remove_empty_values(actors), remove_empty_values(bibliographies))
    except Exception:
        print(traceback.format_exc())
        return ([], [])
