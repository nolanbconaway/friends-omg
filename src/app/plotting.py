"""Utilities to produce plots using eplots."""
from math import sqrt


def normal_approximation_interval(k: int, n: int, z: float = 1.96) -> float:
    """Compute the normal approximation for the interval around a binomial P."""
    if min(k, n) <= 0:
        return None
    p = k / n
    return z * sqrt((p * (1 - p)) / n)


def make_bar_chart(data: dict) -> dict:
    """Prep a plotly bar chart payload."""
    names = [i.title() for i in data.keys()]
    ps = [v["p"] for k, v in data.items()]
    ci = [normal_approximation_interval(v["k"], v["n"]) for k, v in data.items()]

    return dict(
        data=[
            dict(
                x=names,
                y=ps,
                error_y=dict(type="data", array=ci, visible=True),
                type="bar",
            )
        ],
        layout={
            "showlegend": False,
            "margin": dict(t=0, b=70, r=60, l=60),
            "yaxis": {"tickformat": ",.3%", "range": [0, None]},
        },
        config={"displayModeBar": False, "responsive": True},
    )
