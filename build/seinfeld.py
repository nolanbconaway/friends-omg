"""Copy the pre-cleaned seinfeld data into the database.

Thanks again to @colinpollock for providing the data from he repo:

https://github.com/colinpollock/seinfeld-scripts
"""
import sqlite3
from argparse import ArgumentParser
from pathlib import Path

from . import utils

TABLE = "seinfeld"
SOURCE_DB_PATH = utils.RAW_DATA / "seinfeld.db"

# to process the db data
SQL = """
with joined as (
    select
        case
            when episode.season_number < 10 then '0' else ''
        end || episode.season_number || case
            when episode.episode_number < 10 then '0' else ''
        end || episode.episode_number as episode_id,
        utterance.utterance_number as episode_line_number,
        lower(utterance.speaker) as character_name,
        sentence.text as sentence_text

    from utterance
    inner join sentence on utterance.id = sentence.utterance_id
    inner join episode on episode.id = utterance.episode_id

    order by
        episode.season_number,
        episode.episode_number,
        utterance.utterance_number,
        sentence.sentence_number
)

select
    episode_id,
    episode_line_number,
    max(character_name) as character_name,
    group_concat(sentence_text, ' ') as sentence_text


from joined
group by 1, 2
"""


def make_parser():
    parser = ArgumentParser()
    parser.add_argument("--db", type=Path, default=utils.DEFAULT_DB)

    return parser


def main(db_path: Path) -> None:
    print("BUILDING SEINFELD DATA...")

    with sqlite3.connect(db_path) as con:
        con.execute(f"drop table if exists {TABLE}")
        con.executescript(utils.get_ddl(TABLE))

    print("    Querying source db...")
    with sqlite3.connect(SOURCE_DB_PATH) as con:
        records = con.execute(SQL).fetchall()

    print("    Loading results into target db...")
    with sqlite3.connect(db_path) as con:
        con.executemany(
            f"""
            insert into {TABLE} (
                episode_id,
                episode_line_number,
                character_name,
                line_text
            ) 
            values (?, ?, ?, ?)
            """,
            records,
        )


if __name__ == "__main__":
    args = make_parser().parse_args()
    main(args.db)
