"""Test the application using much monkeypatch bc don't want to deal with sqlite."""

import json

import pytest

import app
import app.routes as routes
from app import querying


@pytest.fixture
def client():
    """Application fixture."""
    application = app.create_app(config_file=None)

    with application.test_client() as cli:
        yield cli


def test_blank_page(client):
    """Test no results when there is no query."""
    rv = client.get("/")
    assert b"Proportion of lines" not in rv.data
    assert b"Friends Oh My God!" in rv.data


def test_search(client, monkeypatch):
    """Test page with mocked search results."""
    fake_results = dict(
        dict(
            overall=dict(fake_show=dict(n=10, k=1, p=1 / 10)),
            by_character=dict(
                fake_show=[dict(character_name="fake name", n=10, k=1, p=1 / 10)]
            ),
        )
    )
    monkeypatch.setattr(querying, "count_lines", lambda *x: fake_results)

    rv = client.get("/", query_string="q=something")
    assert b"Proportion of lines" in rv.data
    assert b"Fake_show" in rv.data
    assert b"Fake Name" in rv.data


def test_search_no_k(client, monkeypatch):
    """Test page with mocked search results."""
    fake_results = dict(
        dict(
            overall=dict(fake_show=dict(n=10, k=0, p=0)),
            by_character=dict(
                fake_show=[dict(character_name="fake name", n=10, k=0, p=0)]
            ),
        )
    )
    monkeypatch.setattr(querying, "count_lines", lambda *x: fake_results)

    rv = client.get("/", query_string="q=something")
    assert b"Proportion of lines" in rv.data
    assert b"Fake_show" in rv.data
    assert b"Fake Name" in rv.data
