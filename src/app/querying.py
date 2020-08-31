"""Utilities to interact with the database."""
import sqlite3
import typing
from collections import OrderedDict

from flask import current_app

CHARACTER_QUERY_TEMPLATE = """
with t as (
    select  
        character_name, 
        count(case when lower(line_text) like lower(?) then 1 end) as k,
        count(*) as n

    from {show}
    group by character_name
    having n > 100
)

select character_name, k, n, (k + 0.0) / n as p
from t
order by p desc, n desc
limit 10
"""

SHOW_QUERY_TEMPLATE = """
with t as (
    select 
        count(case when lower(line_text) like lower(?) then 1 end) as k,
        count(*) as n

    from {show}
)

select k, n, (k + 0.0) / n as p
from t
"""


def dict_factory(cursor, row):
    """For the sqlite connection."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def count_character_lines(query: str) -> dict:
    results = OrderedDict()
    with sqlite3.connect(current_app.config["DB_PATH"]) as con:
        con.row_factory = dict_factory

        for show in current_app.config["SHOWS"]:
            key = current_app.config["SHOW_RENAMES"].get(show, show)
            results[key] = con.execute(
                CHARACTER_QUERY_TEMPLATE.format(show=show), ("%" + query + "%",)
            ).fetchall()
    return results


def count_show_lines(query: str) -> dict:
    results = OrderedDict()
    with sqlite3.connect(current_app.config["DB_PATH"]) as con:
        con.row_factory = dict_factory

        for show in current_app.config["SHOWS"]:
            key = current_app.config["SHOW_RENAMES"].get(show, show)
            results[key] = con.execute(
                SHOW_QUERY_TEMPLATE.format(show=show), ("%" + query + "%",)
            ).fetchone()

    return results


def count_lines(query: str) -> dict:
    """Call count show lines and count character lines to get a full result set."""
    character_counts = count_character_lines(query)
    show_counts = count_show_lines(query)
    return dict(overall=show_counts, by_character=character_counts)
