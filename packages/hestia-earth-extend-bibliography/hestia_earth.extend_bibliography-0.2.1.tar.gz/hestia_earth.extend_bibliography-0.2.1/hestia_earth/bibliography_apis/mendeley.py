from hestia_earth.schema import Bibliography
from mendeley import Mendeley

from .utils import MAXIMUM_DISTANCE, find_closest_result, remove_empty_values, extend_bibliography


def author_to_actor(author):
    return {
        'firstName': author.first_name,
        'lastName': author.last_name,
        'scopusID': author.scopus_author_id
    }


def citation_to_bibliography(citation):
    has_identifiers = citation and citation.identifiers is not None
    doi = citation.identifiers['doi'] if has_identifiers and 'doi' in citation.identifiers else None
    scopus = citation.identifiers['scopus'] if has_identifiers and 'scopus' in citation.identifiers else None
    return {
        'title': citation.title,
        'year': citation.year,
        'documentType': citation.type,
        'outlet': citation.source,
        'mendeleyID': citation.id,
        'abstract': citation.abstract,
        'documentDOI': doi,
        'scopus': scopus
    }


def create_biblio(title, citation):
    biblio = Bibliography()
    # save title here since closest citation might differ
    biblio.fields['originalTitle'] = title
    biblio.fields['title'] = title
    authors = list(map(author_to_actor, citation.authors if citation else []))
    bibliography = citation_to_bibliography(citation) if citation else {}
    (extended_biblio, actors) = extend_bibliography(authors, citation.year) if citation else ({}, [])
    return (
        {**biblio.to_dict(), **bibliography, **extended_biblio},
        actors
    ) if citation else (biblio.to_dict(), [])


def exec_search(session):
    def search(title: str):
        items = session.catalog.search(title, view='all').list(20).items
        return list(map(lambda x: {'title': x.title, 'item': x}, items))
    return search


def search(queries, session, title):
    [citation, distance] = find_closest_result(queries, title, exec_search(session))
    return create_biblio(title, citation if distance <= MAXIMUM_DISTANCE else None)


def extend_mendeley(titles, **kwargs):
    mendel = Mendeley(client_id=int(kwargs.get('mendeley_username')), client_secret=kwargs.get('mendeley_password'))
    auth = mendel.start_client_credentials_flow()
    session = auth.authenticate()

    queries = {}
    bibliographies = []
    actors = []

    for title in titles:
        if len(title) > 0:
            (biblio, authors) = search(queries, session, title)
            bibliographies.extend([] if biblio is None else [biblio])
            actors.extend([] if authors is None else authors)

    return (remove_empty_values(actors), remove_empty_values(bibliographies))
