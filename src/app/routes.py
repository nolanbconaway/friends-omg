"""Routes for the app."""
from flask import Blueprint, jsonify, render_template, request

from . import querying
from .plotting import make_bar_chart

bp = Blueprint("routes", __name__)


@bp.route("/")
def search_form():
    """Present the search form for the user."""
    query = request.args.get("q", None)
    if query is None or not query:
        return render_template("search.html")

    result = querying.count_lines(query)
    chart = make_bar_chart(result["overall"])

    return render_template(
        "search.html", search_results=result, query=query, chart=chart,
    )
