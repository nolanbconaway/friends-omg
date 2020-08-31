"""Postprocess the FRIENDS html data into the database."""
import html
import re
import sqlite3
from argparse import ArgumentParser
from pathlib import Path

from bs4 import BeautifulSoup

from . import utils

TABLE = "friends"
EXCLUDE_FILES = {"07outtakes.html", "0423uncut.html"}
HTML_DIR = utils.RAW_DATA / "friends" / "season"


def make_parser():
    parser = ArgumentParser()
    parser.add_argument("--db", type=Path, default=utils.DEFAULT_DB)

    return parser


def remove_blocking(s: str) -> str:
    return re.sub(r"\[[^)]*\]", "", re.sub(r"\([^)]*\)", "", s))


def get_lines(filepath: Path):
    script = html.unescape(
        BeautifulSoup(filepath.read_text("latin1"), "lxml").get_text()
    )
    pattern = re.compile(r"\s(?=\w+(?=:))")
    result = re.split(pattern, script)

    episode_id = filepath.name.split(".html")[0]
    lines = []
    line_no = 0
    for item in filter(lambda x: ": " in x, result):
        split_line = item.split(": ")
        character = split_line[0].lower()
        speech = " ".join(remove_blocking(": ".join(split_line[1:])).split())

        lines.append((episode_id, line_no, character, speech))
        line_no += 1

    if len(lines) < 10:
        raise RuntimeError(f"{filepath.name}: {len(lines):03d} lines")

    return lines


def clean_lines(lines: list) -> list:
    character_replace = {
        "chan": "chandler",
        "chandler": "chandler",
        "chandlers": "chandler",
        "joey": "joey",
        "mnca": "monica",
        "monica": "monica",
        "phoe": "phoebe",
        "phoebe": "phoebe",
        "pheebs": "phoebe",
        "rache": "rachel",
        "rachel": "rachel",
        "rach": "rachel",
        "ross": "ross",
    }
    # remove invalid characters
    result = [i for i in lines if i[2] not in ("by, ")]

    # replace character names
    result = [(*i[:2], character_replace.get(i[2], i[2]), i[3]) for i in result]
    return result


def main(db_path: Path) -> None:
    print("BUILDING FRIENDS DATA...")
    with sqlite3.connect(db_path) as con:
        con.execute(f"drop table if exists {TABLE}")
        con.executescript(utils.get_ddl(TABLE))

    print("    Processing HTML data...")
    files = sorted(i for i in HTML_DIR.glob("*.html") if i.name not in EXCLUDE_FILES)
    records = []
    for filepath in files:
        records += get_lines(filepath)

    print("    Cleaning and appending to db...")
    records = clean_lines(records)

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
