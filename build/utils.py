from pathlib import Path

BUILD = Path(__file__).parent.absolute()
OMG = BUILD.parent
DEFAULT_DB = OMG / "data.db"
RAW_DATA = OMG / "raw-data"


def get_ddl(table: str) -> str:
    return (BUILD / "ddl.sql").read_text().format(table_name=table)
