from dash import Dash

from src.flask import flask_server

dash_app = Dash(__name__, server=flask_server, use_pages=True)