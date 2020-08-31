from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address, default_limits=["2 per second", "86400 per day"]
)


@limiter.request_filter
def ip_whitelist():
    """Add some exemptions to the limiter."""
    from flask import request

    return request.remote_addr in ("127.0.0.1", "localhost")


def create_app(config_file: str = "config.py"):
    """App factory."""
    app = Flask(__name__)

    if config_file:
        app.config.from_pyfile(config_file)

    from . import routes

    limiter.init_app(app)
    app.register_blueprint(routes.bp)

    return app
