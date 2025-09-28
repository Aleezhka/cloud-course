import os
from http import HTTPStatus
import secrets
from typing import Dict, Any

from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from my_project.db import db


DB_URI_KEY = "SQLALCHEMY_DATABASE_URI"
DB_USER_KEY = "MYSQL_ROOT_USER"
DB_PASS_KEY = "MYSQL_ROOT_PASSWORD"


def create_app(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> Flask:
    _process_input_config(app_config, additional_config)
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(16)
    app.config.update(app_config)

    _init_db(app)
    _init_swagger(app)

    return app


def _init_db(app: Flask) -> None:
    db.init_app(app)
    with app.app_context():
        db.create_all()


def _process_input_config(app_config: Dict[str, Any], additional_config: Dict[str, Any]) -> None:
    root_user = os.getenv(DB_USER_KEY, additional_config[DB_USER_KEY])
    root_password = os.getenv(DB_PASS_KEY, additional_config[DB_PASS_KEY])
    app_config[DB_URI_KEY] = app_config[DB_URI_KEY].format(root_user, root_password)


def _init_swagger(app: Flask) -> None:
    api = Api(app, title="Olezhka Cloud", description="Azure project")

    # --- Моделі для Swagger ---
    user_model = api.model('User', {
        'id': fields.Integer(readonly=True),
        'name': fields.String(required=True),
        'email': fields.String(required=True),
        'password': fields.String(required=True),
        'city': fields.String
    })

    flight_model = api.model('Flight', {
        'id': fields.Integer(readonly=True),
        'airline_id': fields.Integer(required=True),
        'departure_airport_id': fields.Integer(required=True),
        'arrival_airport_id': fields.Integer(required=True),
        'departure_time': fields.String(required=True, description="YYYY-MM-DD HH:MM:SS"),
        'arrival_time': fields.String(required=True, description="YYYY-MM-DD HH:MM:SS"),
        'ticket_price': fields.Float(required=True)
    })

    ticket_model = api.model('Ticket', {
        'id': fields.Integer(readonly=True),
        'flight_id': fields.Integer(required=True),
        'purchase_date': fields.String(required=True, description="YYYY-MM-DD HH:MM:SS")
    })

    ticket_history_model = api.model('TicketHistory', {
        'id': fields.Integer(readonly=True),
        'ticket_id': fields.Integer(required=True),
        'user_id': fields.Integer(required=True),
        'status': fields.String(required=True),
        'change_time': fields.String(required=True, description="YYYY-MM-DD HH:MM:SS")
    })

    connected_flight_model = api.model('ConnectedFlight', {
        'id': fields.Integer(readonly=True),
        'flight_id': fields.Integer(required=True),
        'connected_flight_id': fields.Integer(required=True)
    })

    # --- Users ---
    @api.route("/users/<int:user_id>")
    class UserResource(Resource):
        @api.marshal_with(user_model)
        def get(self, user_id):
            user = User.query.get(user_id)
            return user.put_into_dto() if user else ("User not found", HTTPStatus.NOT_FOUND)

        @api.expect(user_model)
        @api.marshal_with(user_model)
        def put(self, user_id):
            data = request.json
            user = User.query.get(user_id)
            if user:
                for key, value in data.items():
                    setattr(user, key, value)
                db.session.commit()
                return user.put_into_dto(), HTTPStatus.OK
            return ("User not found", HTTPStatus.NOT_FOUND)

        def delete(self, user_id):
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return ("Deleted", HTTPStatus.NO_CONTENT)
            return ("User not found", HTTPStatus.NOT_FOUND)

    @api.route("/users")
    class UserList(Resource):
        @api.marshal_list_with(user_model)
        def get(self):
            return [u.put_into_dto() for u in User.query.all()]

        @api.expect(user_model)
        @api.marshal_with(user_model)
        def post(self):
            data = request.json
            user = User.create_from_dto(data)
            db.session.add(user)
            db.session.commit()
            return user.put_into_dto(), HTTPStatus.CREATED

    # --- Flight ---
    @api.route("/flights/<int:flight_id>")
    class FlightResource(Resource):
        @api.marshal_with(flight_model)
        def get(self, flight_id):
            flight = Flight.query.get(flight_id)
            return flight.put_into_dto() if flight else ("Flight not found", HTTPStatus.NOT_FOUND)

        @api.expect(flight_model)
        @api.marshal_with(flight_model)
        def put(self, flight_id):
            data = request.json
            flight = Flight.query.get(flight_id)
            if flight:
                for key, value in data.items():
                    setattr(flight, key, value)
                db.session.commit()
                return flight.put_into_dto(), HTTPStatus.OK
            return ("Flight not found", HTTPStatus.NOT_FOUND)

        def delete(self, flight_id):
            flight = Flight.query.get(flight_id)
            if flight:
                db.session.delete(flight)
                db.session.commit()
                return ("Deleted", HTTPStatus.NO_CONTENT)
            return ("Flight not found", HTTPStatus.NOT_FOUND)

    @api.route("/flights")
    class FlightList(Resource):
        @api.marshal_list_with(flight_model)
        def get(self):
            return [f.put_into_dto() for f in Flight.query.all()]

        @api.expect(flight_model)
        @api.marshal_with(flight_model)
        def post(self):
            data = request.json
            flight = Flight.create_from_dto(data)
            db.session.add(flight)
            db.session.commit()
            return flight.put_into_dto(), HTTPStatus.CREATED

    # --- Ticket ---
    @api.route("/tickets/<int:ticket_id>")
    class TicketResource(Resource):
        @api.marshal_with(ticket_model)
        def get(self, ticket_id):
            ticket = Ticket.query.get(ticket_id)
            return ticket.put_into_dto() if ticket else ("Ticket not found", HTTPStatus.NOT_FOUND)

        @api.expect(ticket_model)
        @api.marshal_with(ticket_model)
        def put(self, ticket_id):
            data = request.json
            ticket = Ticket.query.get(ticket_id)
            if ticket:
                for key, value in data.items():
                    setattr(ticket, key, value)
                db.session.commit()
                return ticket.put_into_dto(), HTTPStatus.OK
            return ("Ticket not found", HTTPStatus.NOT_FOUND)

        def delete(self, ticket_id):
            ticket = Ticket.query.get(ticket_id)
            if ticket:
                db.session.delete(ticket)
                db.session.commit()
                return ("Deleted", HTTPStatus.NO_CONTENT)
            return ("Ticket not found", HTTPStatus.NOT_FOUND)

    @api.route("/tickets")
    class TicketList(Resource):
        @api.marshal_list_with(ticket_model)
        def get(self):
            return [t.put_into_dto() for t in Ticket.query.all()]

        @api.expect(ticket_model)
        @api.marshal_with(ticket_model)
        def post(self):
            data = request.json
            ticket = Ticket.create_from_dto(data)
            db.session.add(ticket)
            db.session.commit()
            return ticket.put_into_dto(), HTTPStatus.CREATED

    # --- TicketHistory ---
    @api.route("/ticket_histories/<int:id>")
    class TicketHistoryResource(Resource):
        @api.marshal_with(ticket_history_model)
        def get(self, id):
            th = TicketHistory.query.get(id)
            return th.put_into_dto() if th else ("Not found", HTTPStatus.NOT_FOUND)

        def delete(self, id):
            th = TicketHistory.query.get(id)
            if th:
                db.session.delete(th)
                db.session.commit()
                return ("Deleted", HTTPStatus.NO_CONTENT)
            return ("Not found", HTTPStatus.NOT_FOUND)

    @api.route("/ticket_histories")
    class TicketHistoryList(Resource):
        @api.marshal_list_with(ticket_history_model)
        def get(self):
            return [th.put_into_dto() for th in TicketHistory.query.all()]

        @api.expect(ticket_history_model)
        @api.marshal_with(ticket_history_model)
        def post(self):
            data = request.json
            th = TicketHistory.create_from_dto(data)
            db.session.add(th)
            db.session.commit()
            return th.put_into_dto(), HTTPStatus.CREATED

    # --- ConnectedFlight ---
    @api.route("/connected_flights/<int:id>")
    class ConnectedFlightResource(Resource):
        @api.marshal_with(connected_flight_model)
        def get(self, id):
            cf = ConnectedFlight.query.get(id)
            return cf.put_into_dto() if cf else ("Not found", HTTPStatus.NOT_FOUND)

        def delete(self, id):
            cf = ConnectedFlight.query.get(id)
            if cf:
                db.session.delete(cf)
                db.session.commit()
                return ("Deleted", HTTPStatus.NO_CONTENT)
            return ("Not found", HTTPStatus.NOT_FOUND)

    @api.route("/connected_flights")
    class ConnectedFlightList(Resource):
        @api.marshal_list_with(connected_flight_model)
        def get(self):
            return [cf.put_into_dto() for cf in ConnectedFlight.query.all()]

        @api.expect(connected_flight_model)
        @api.marshal_with(connected_flight_model)
        def post(self):
            data = request.json
            cf = ConnectedFlight.create_from_dto(data)
            db.session.add(cf)
            db.session.commit()
            return cf.put_into_dto(), HTTPStatus.CREATED


app_config = {
    "SQLALCHEMY_DATABASE_URI": (
        "mssql+pyodbc://{0}:{1}@cloud-course-db.database.windows.net:1433/cloud-course-db"
        "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"
    ),
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}

additional_config = {
    "MYSQL_ROOT_USER": "olezhka",
    "MYSQL_ROOT_PASSWORD": "Sqlroot365"
}

DEVELOPMENT_PORT = 5000
HOST = "0.0.0.0"

app = create_app(app_config, additional_config)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", DEVELOPMENT_PORT))
    app.run(host=HOST, port=port, debug=True)