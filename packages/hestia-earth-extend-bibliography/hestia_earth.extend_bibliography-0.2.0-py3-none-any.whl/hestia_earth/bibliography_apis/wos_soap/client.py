from wos import WosClient
import wos.utils
import xmltodict
from hestia_earth.schema import Bibliography

from hestia_earth.bibliography_apis.utils import extend_bibliography


def int_value(x): return int(x) if int(x) > 0 else None


def author_to_actor(author: str):
    [last, first] = author.split(', ')
    return {
        'firstName': first,
        'lastName': last
    }


def item_to_bibliography(item: dict):
    values = item['source'] + item['other']

    def label_value(label: str, default=None):
        return next((x['value'] for x in values if x['label'] == label), default)

    return {
        'title': item['title']['value'],
        'year': int_value(label_value('Published.BiblioYear', 0)),
        'documentDOI': label_value('Identifier.Doi'),
        'volume': int_value(label_value('Volume')),
        'issue': int_value(label_value('Issue')),
        'pages': label_value('Pages'),
        'outlet': label_value('SourceTitle')
    }


def create_biblio(title: str, item: dict):
    biblio = Bibliography()
    # save title here since closest item might differ
    biblio.fields['originalTitle'] = title
    biblio.fields['title'] = title
    authors = list(map(author_to_actor, item.get('authors')['value'] if item else []))
    bibliography = item_to_bibliography(item) if item else {}
    (extended_biblio, actors) = extend_bibliography(authors, bibliography['year']) if item else ({}, [])
    return (
        {**biblio.to_dict(), **bibliography, **extended_biblio},
        actors
    ) if item else (biblio.to_dict(), [])


def exec_search(user: str, password: str):
    def search(title: str):
        try:
            with WosClient(user=user, password=password, lite=True) as client:
                result = xmltodict.parse(wos.utils.query(client, f"TI=({title})"))['return']
                items = result['records'] if 'records' in result else []
                items = [items] if isinstance(items, dict) else items
                return list(map(lambda x: {'title': x['title']['value'], 'item': x}, items))
        except Exception:
            return []
    return search
