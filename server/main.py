from os import getenv

from src.dash import dash_app

if __name__ == '__main__':
    dash_app.run(debug=(getenv("DEBUG") == "TRUE"), port=int(getenv("PORT")), host="0.0.0.0")
