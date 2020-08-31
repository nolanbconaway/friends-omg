"""Build the full database from scratch."""

from argparse import ArgumentParser
from pathlib import Path

from . import friends, satc, seinfeld, utils


def make_parser():
    parser = ArgumentParser()
    parser.add_argument("--db", type=Path, default=utils.DEFAULT_DB)

    return parser


def main(db_path: Path) -> None:
    if db_path.exists():
        db_path.unlink()

    for show in satc, seinfeld, friends:
        show.main(db_path)


if __name__ == "__main__":
    args = make_parser().parse_args()
    main(args.db)
