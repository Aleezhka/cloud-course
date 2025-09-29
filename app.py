import os
import yaml
from waitress import serve
from my_project import create_app

DEVELOPMENT_PORT = 5000
PRODUCTION_PORT = 8080
HOST = "0.0.0.0"
DEVELOPMENT = "development"
PRODUCTION = "production"
FLASK_ENV = "FLASK_ENV"
ADDITIONAL_CONFIG = "ADDITIONAL_CONFIG"


def _create_application_instance():
    try:
        flask_env = os.environ.get(FLASK_ENV, DEVELOPMENT).lower()
        return create_app()
    except Exception as e:
        print(f"Помилка при створенні додатку: {e}")
        return create_app()



app = _create_application_instance()


if __name__ == '__main__':
    flask_env = os.environ.get(FLASK_ENV, DEVELOPMENT).lower()

    if flask_env == DEVELOPMENT:
        app.run(host=HOST, port=DEVELOPMENT_PORT, debug=True)

    elif flask_env == PRODUCTION:
        serve(app, host=HOST, port=PRODUCTION_PORT)
