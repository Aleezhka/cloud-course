import os
from http import HTTPStatus
import secrets
from typing import Dict, Any

from flask import Flask
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database

from my_project.auth.route import register_routes

import pymysql
pymysql.install_as_MySQLdb()  


DB_URI_KEY = "SQLALCHEMY_DATABASE_URI"
DB_USER_KEY = "MYSQL_ROOT_USER"
DB_PASS_KEY = "MYSQL_ROOT_PASSWORD"

# Database
db = SQLAlchemy()
todos = {}


def create_app(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> Flask:
    """
    Creates Flask application
    """
    _process_input_config(app_config, additional_config)
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(16)
    app.config.update(app_config)

    _init_db(app)
    register_routes(app)
    _init_swagger(app)

    return app


def _init_swagger(app: Flask) -> None:
    # Swagger
    restx_api = Api(app, title="Olezhka Cloud",
                    description="Azure project")

    @restx_api.route("/users/<string:user_id>")
    class TodoSimple(Resource):
        @staticmethod
        def get(user_id):
            return todos, HTTPStatus.ACCEPTED



def _init_db(app: Flask) -> None:
    """Initializes DB with SQLAlchemy"""
    db.init_app(app)

    if not database_exists(app.config[DB_URI_KEY]):
        create_database(app.config[DB_URI_KEY])

    import my_project.auth.domain
    with app.app_context():
        db.create_all()


def _process_input_config(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> None:
    """Processes input configuration"""
    root_user = os.getenv(DB_USER_KEY, additional_config[DB_USER_KEY])
    root_password = os.getenv(DB_PASS_KEY, additional_config[DB_PASS_KEY])

    app_config[DB_URI_KEY] = app_config[DB_URI_KEY].format(root_user, root_password)
