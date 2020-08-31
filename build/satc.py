"""Parse the SATC CSV file into the database."""
import sqlite3
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

from . import utils

TABLE = "satc"
SOURCE_CSV_PATH = utils.RAW_DATA / "satc.csv"


def make_parser():
    parser = ArgumentParser()
    parser.add_argument("--db", type=Path, default=utils.DEFAULT_DB)

    return parser


def main(db_path: Path) -> None:
    print("BUILDING SATC DATA...")

    with sqlite3.connect(db_path) as con:
        con.execute(f"drop table if exists {TABLE}")
        con.executescript(utils.get_ddl(TABLE))

    print("    Processing the csv...")

    records = (
        pd.read_csv(SOURCE_CSV_PATH)
        .assign(
            episode_id=lambda x: x.Season.astype(int).astype(str).str.zfill(2)
            + x.Episode.astype(int).astype(str).str.zfill(2),
            episode_line_number=lambda x: x.groupby("episode_id").cumcount(),
            Speaker=lambda x: x.Speaker.str.lower().fillna("<unknown>"),
        )[["episode_id", "episode_line_number", "Speaker", "Line",]]
        .to_records(index=False)
        .tolist()
    )

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
