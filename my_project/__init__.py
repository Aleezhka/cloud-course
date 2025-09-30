import os
from http import HTTPStatus
import secrets
from typing import Dict, Any
from datetime import timedelta

from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from my_project.db import db
from dotenv import load_dotenv


load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(16)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_SECRET_KEY"] = secrets.token_hex(32)

    jwt = JWTManager(app)

    db_user = os.environ.get("MYSQL_ROOT_USER")
    db_pass = os.environ.get("MYSQL_ROOT_PASSWORD")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mssql+pyodbc://{db_user}:{db_pass}@cloud-course-db.database.windows.net:1433/cloud-course-db"
        "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"
    )


    _init_db(app)
    _init_swagger(app)

    return app


def _init_db(app: Flask) -> None:
    db.init_app(app)
    with app.app_context():
        db.create_all()
        


def _init_swagger(app: Flask) -> None:
    from my_project.auth.domain import User, Flight, Ticket, TicketHistory, ConnectedFlight
    authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Введи JWT токен у форматі: **Bearer &lt;your_token&gt;**'
    }
}
    api = Api(
    app,
    title="Olezhka Cloud",
    description="Azure project",
    authorizations=authorizations,
    security='Bearer Auth'
)

    # --- MODELS ---
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
        'departure_time': fields.String(required=True),
        'arrival_time': fields.String(required=True),
        'ticket_price': fields.Float(required=True)
    })

    ticket_model = api.model('Ticket', {
        'id': fields.Integer(readonly=True),
        'flight_id': fields.Integer(required=True),
        'purchase_date': fields.String(required=True)
    })

    ticket_history_model = api.model('TicketHistory', {
        'id': fields.Integer(readonly=True),
        'ticket_id': fields.Integer(required=True),
        'user_id': fields.Integer(required=True),
        'status': fields.String(required=True),
        'change_time': fields.String(required=True)
    })

    connected_flight_model = api.model('ConnectedFlight', {
        'id': fields.Integer(readonly=True),
        'flight_id': fields.Integer(required=True),
        'connected_flight_id': fields.Integer(required=True)
    })


    # --- NAMESPACES ---
    user_ns = api.namespace("users", description="User operations")
    flight_ns = api.namespace("flights", description="Flight operations")
    ticket_ns = api.namespace("tickets", description="Ticket operations")
    th_ns = api.namespace("ticket_histories", description="Ticket history operations")
    cf_ns = api.namespace("connected_flights", description="Connected flight operations")

    login_model = user_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
    })


    @user_ns.route("/login")
    class UserLogin(Resource):
        @user_ns.expect(login_model)
        def post(self):
            data = request.json
            email = data.get("email")
            password = data.get("password")

            user = User.query.filter_by(email=email).first()
            if user and user.password == password:
                access_token = create_access_token(identity=str(user.id))
                return {'token': access_token}, HTTPStatus.OK

            return {"message": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED
        

    # --- USERS ---
    @user_ns.route("/")
    class UserList(Resource):
        @user_ns.marshal_list_with(user_model)
        def get(self):
            return [u.put_into_dto() for u in User.query.all()]

        @jwt_required()
        @user_ns.expect(user_model)
        @user_ns.marshal_with(user_model, code=201)
        def post(self):
            data = request.json
            user = User.create_from_dto(data)
            db.session.add(user)
            db.session.commit()
            return user.put_into_dto(), HTTPStatus.CREATED

    @user_ns.route("/<int:user_id>")
    class UserItem(Resource):
        @user_ns.marshal_with(user_model)
        def get(self, user_id):
            user = User.query.get(user_id)
            return user.put_into_dto() if user else ("User not found", HTTPStatus.NOT_FOUND)

        @jwt_required()
        @user_ns.expect(user_model)
        @user_ns.marshal_with(user_model)
        def put(self, user_id):
            data = request.json
            user = User.query.get(user_id)
            if user:
                for k, v in data.items():
                    setattr(user, k, v)
                db.session.commit()
                return user.put_into_dto(), HTTPStatus.OK
            return ("User not found", HTTPStatus.NOT_FOUND)

        @jwt_required()
        def delete(self, user_id):
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return ("Deleted", HTTPStatus.NO_CONTENT)
            return ("User not found", HTTPStatus.NOT_FOUND)

    # --- FLIGHTS ---
    @flight_ns.route("/")
    class FlightList(Resource):
        @flight_ns.marshal_list_with(flight_model)
        def get(self):
            return [f.put_into_dto() for f in Flight.query.all()]

        @jwt_required()
        @flight_ns.expect(flight_model)
        @flight_ns.marshal_with(flight_model, code=201)
        def post(self):
            data = request.json
            flight = Flight.create_from_dto(data)
            db.session.add(flight)
            db.session.commit()
            return flight.put_into_dto(), HTTPStatus.CREATED

    @flight_ns.route("/<int:flight_id>")
    class FlightItem(Resource):
        @flight_ns.marshal_with(flight_model)
        def get(self, flight_id):
            flight = Flight.query.get(flight_id)
            return flight.put_into_dto() if flight else ("Flight not found", HTTPStatus.NOT_FOUND)

        @jwt_required()
        @flight_ns.expect(flight_model)
        @flight_ns.marshal_with(flight_model)
        def put(self, flight_id):
            data = request.json
            flight = Flight.query.get(flight_id)
            if flight:
                for k, v in data.items():
                    setattr(flight, k, v)
                db.session.commit()
                return flight.put_into_dto(), HTTPStatus.OK
            return ("Flight not found", HTTPStatus.NOT_FOUND)

        @jwt_required()
        def delete(self, flight_id):
            flight = Flight.query.get(flight_id)
            if flight:
                db.session.delete(flight)
                db.session.commit()
                return ("Deleted", HTTPStatus.NO_CONTENT)
            return ("Flight not found", HTTPStatus.NOT_FOUND)

    # --- TICKETS ---
    @ticket_ns.route("/")
    class TicketList(Resource):
        @ticket_ns.marshal_list_with(ticket_model)
        def get(self):
            return [t.put_into_dto() for t in Ticket.query.all()]

        @jwt_required()
        @ticket_ns.expect(ticket_model)
        @ticket_ns.marshal_with(ticket_model, code=201)
        def post(self):
            data = request.json
            ticket = Ticket.create_from_dto(data)
            db.session.add(ticket)
            db.session.commit()
            return ticket.put_into_dto(), HTTPStatus.CREATED

    @ticket_ns.route("/<int:ticket_id>")
    class TicketItem(Resource):
        @ticket_ns.marshal_with(ticket_model)
        def get(self, ticket_id):
            ticket = Ticket.query.get(ticket_id)
            return ticket.put_into_dto() if ticket else ("Ticket not found", HTTPStatus.NOT_FOUND)

        @jwt_required()
        @ticket_ns.expect(ticket_model)
        @ticket_ns.marshal_with(ticket_model)
        def put(self, ticket_id):
            data = request.json
            ticket = Ticket.query.get(ticket_id)
            if ticket:
                for k, v in data.items():
                    setattr(ticket, k, v)
                db.session.commit()
                return ticket.put_into_dto(), HTTPStatus.OK
            return ("Ticket not found", HTTPStatus.NOT_FOUND)

        @jwt_required()
        def delete(self, ticket_id):
            ticket = Ticket.query.get(ticket_id)
            if ticket:
                db.session.delete(ticket)
                db.session.commit()
                return ("Deleted", HTTPStatus.NO_CONTENT)
            return ("Ticket not found", HTTPStatus.NOT_FOUND)

    # --- TICKET HISTORY ---
    @th_ns.route("/")
    class TicketHistoryList(Resource):
        @th_ns.marshal_list_with(ticket_history_model)
        def get(self):
            return [th.put_into_dto() for th in TicketHistory.query.all()]

        @jwt_required()
        @th_ns.expect(ticket_history_model)
        @th_ns.marshal_with(ticket_history_model, code=201)
        def post(self):
            data = request.json
            th = TicketHistory.create_from_dto(data)
            db.session.add(th)
            db.session.commit()
            return th.put_into_dto(), HTTPStatus.CREATED

    @th_ns.route("/<int:id>")
    class TicketHistoryItem(Resource):
        @th_ns.marshal_with(ticket_history_model)
        def get(self, id):
            th = TicketHistory.query.get(id)
            return th.put_into_dto() if th else ("Not found", HTTPStatus.NOT_FOUND)

        @jwt_required()
        def delete(self, id):
            th = TicketHistory.query.get(id)
            if th:
                db.session.delete(th)
                db.session.commit()
                return ("Deleted", HTTPStatus.NO_CONTENT)
            return ("Not found", HTTPStatus.NOT_FOUND)

    # --- CONNECTED FLIGHTS ---
    @cf_ns.route("/")
    class ConnectedFlightList(Resource):
        @cf_ns.marshal_list_with(connected_flight_model)
        def get(self):
            return [cf.put_into_dto() for cf in ConnectedFlight.query.all()]

        @jwt_required()
        @cf_ns.expect(connected_flight_model)
        @cf_ns.marshal_with(connected_flight_model, code=201)
        def post(self):
            data = request.json
            cf = ConnectedFlight.create_from_dto(data)
            db.session.add(cf)
            db.session.commit()
            return cf.put_into_dto(), HTTPStatus.CREATED

    @cf_ns.route("/<int:id>")
    class ConnectedFlightItem(Resource):
        @cf_ns.marshal_with(connected_flight_model)
        def get(self, id):
            cf = ConnectedFlight.query.get(id)
            return cf.put_into_dto() if cf else ("Not found", HTTPStatus.NOT_FOUND)

        @jwt_required()
        def delete(self, id):
            cf = ConnectedFlight.query.get(id)
            if cf:
                db.session.delete(cf)
                db.session.commit()
                return ("Deleted", HTTPStatus.NO_CONTENT)
            return ("Not found", HTTPStatus.NOT_FOUND)



DEVELOPMENT_PORT = 5000
HOST = "0.0.0.0"

app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", DEVELOPMENT_PORT))
    app.run(host=HOST, port=port, debug=True)