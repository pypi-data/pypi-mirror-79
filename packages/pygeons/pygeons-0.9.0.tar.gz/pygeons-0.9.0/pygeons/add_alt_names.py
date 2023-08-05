"""Add alternative names using some ad hoc business logic."""

import collections
import logging
import os.path as P
import re

from typing import (
    Dict,
    List,
)

import yaml

import pygeons.db


def _load(name):
    """Load the data file with the specified name."""
    curr = P.dirname(P.abspath(__file__))
    with open(P.join(curr, "data", "%s.yml" % name)) as fin:
        return yaml.full_load(fin)


def _get_existing_names(
    feature_code: str,
    country_code: str,
) -> Dict[str, List[str]]:
    c = pygeons.db.CONN.cursor()

    existing = collections.defaultdict(set)
    command = (
        'SELECT G.geonameid, A.alternate_name '
        'FROM geoname G JOIN alternatename A on G.geonameid = A.geonameid '
        'WHERE feature_code = ? AND country_code = ?'
    )
    params = (feature_code, country_code)
    for geonameid, name in c.execute(command, params):
        existing[geonameid].add(name.lower())
    
    return dict(existing.items())


def add_gb_county_names() -> None:
    c = pygeons.db.CONN.cursor()
    data = _load('gb-counties')
    existing = _get_existing_names('ADM2', 'GB')
    command = (
        'SELECT geonameid, name FROM geoname '
        'WHERE feature_code = "ADM2" AND country_code = "GB"'
    )
    def g():
        for geonameid, name in c.execute(command):
            try:
                new_names = data[name]
            except KeyError:
                continue

            for name in new_names:
                if name.lower() not in existing[geonameid]:
                    yield geonameid, name

    insert = (
        'INSERT INTO alternatename(geonameid, alternate_name, isolanguage, isShortName) '
        'VALUES (?, ?, ?, ?)'
    )

    params = [(geonameid, name, 'en', True) for (geonameid, name) in g()]
    c.executemany(insert, params)
    pygeons.db.CONN.commit()


def add_ie_county_names() -> None:
    c = pygeons.db.CONN.cursor()

    existing = _get_existing_names('ADM2', 'IE')

    command = (
        'SELECT geonameid, name FROM geoname '
        'WHERE feature_code = "ADM2" AND country_code = "IE"'
    )
    def g():
        for geonameid, name in c.execute(command):
            new_names = set()
            if name.startswith('County ') or name.endswith(' County'):
                stripped = name.replace('County', '').strip()
                new_names.add('Co ' + stripped)
                new_names.add(stripped)

            for name in new_names:
                if name.lower() not in existing[geonameid]:
                    yield geonameid, name

    insert = (
        'INSERT INTO alternatename(geonameid, alternate_name, isolanguage, isShortName) '
        'VALUES (?, ?, ?, ?)'
    )

    params = [(geonameid, name, 'en', True) for (geonameid, name) in g()]
    c.executemany(insert, params)
    pygeons.db.CONN.commit()


def _strip_ken_suffix(name):
    """
    >>> _strip_ken_suffix('Akita ken')
    'Akita'
    >>> _strip_ken_suffix('Akita-ken')
    'Akita'
    >>> _strip_ken_suffix('Akita Prefecture')
    'Akita'
    """
    return re.sub(r'[- ](ken|prefecture)', '', name, flags=re.IGNORECASE)


def add_jp_prefecture_names():
    existing = _get_existing_names('ADM1', 'JP')

    command = (
        'SELECT geonameid, name FROM geoname '
        'WHERE feature_code = "ADM1" AND country_code = "JP"'
    )
    def g():
        new_names = set()
        for geonameid, name in c.execute(command):
            barename = _strip_ken_suffix(name)
            if barename == 'Hokkaido':
                pass
            elif barename in ('Ōsaka', 'Tokyo'):
                new_names |= {barename, barename + ' prefecture'}
            else:
                new_names |= {barename, barename + '-ken', barename + ' prefecture'}

        for name in new_names:
            if name.lower() not in existing:
                yield name

    insert = (
        'INSERT INTO alternatename(geonameid, alternate_name, isolanguage) '
        'VALUES (?, ?, ?)'
    )
    params = [(geonameid, name, 'en') for (geonameid, name) in g()]
    c.executemany(insert, params)
    pygeons.db.CONN.commit()



if __name__ == '__main__':
    pygeons.db.connect()
    add_gb_county_names()
    add_ie_county_names()
