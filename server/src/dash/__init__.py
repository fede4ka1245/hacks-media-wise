from os import getenv

from dash import Dash

from src.flask import flask_server

dash_app = Dash(__name__, server=flask_server, use_pages=True, serve_locally=(getenv("SERVE_LOCALLY") == "TRUE"),
                url_base_pathname="/api/")

dash_app.css.config.serve_locally = True
dash_app.scripts.config.serve_locally = True