from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import TicketController
from my_project.auth.domain import Ticket
from my_project.auth.domain import User


ticket_bp = Blueprint('tickets', __name__, url_prefix='/tickets')
ticket_controller = TicketController()

@ticket_bp.route('', methods=['GET'])
def get_all_tickets() -> Response:
    return make_response(jsonify(ticket_controller.find_all()), HTTPStatus.OK)

@ticket_bp.route('', methods=['POST'])
def create_ticket() -> Response:
        content = request.get_json()
        ticket = Ticket.create_from_dto(content)
        ticket_controller.create(ticket)
        return make_response(jsonify(ticket.put_into_dto()), HTTPStatus.CREATED)

@ticket_bp.route('/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id: int) -> Response:
        return make_response(jsonify(ticket_controller.find_by_id(ticket_id)), HTTPStatus.OK)

@ticket_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id: int) -> Response:
        content = request.get_json()
        ticket = Ticket.create_from_dto(content)
        ticket_controller.update(ticket_id, ticket)
        return make_response("Ticket updated", HTTPStatus.OK)

@ticket_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id: int) -> Response:
        ticket_controller.delete(ticket_id)
        return make_response("Ticket deleted", HTTPStatus.OK)

@ticket_bp.route('/flight/<int:flight_id>', methods=['GET'])
def get_tickets_by_flight(flight_id: int) -> Response:
        return make_response(jsonify(ticket_controller.get_tickets_by_flight_id(flight_id)), HTTPStatus.OK)

@ticket_bp.route('/user/<int:user_id>/tickets', methods=['GET'])
def get_tickets_by_user(user_id: int) -> Response:
    user = User.query.get(user_id)
    if user:
        tickets = user.tickets
        return make_response(jsonify([ticket.put_into_dto() for ticket in tickets]), HTTPStatus.OK)
    return make_response("User not found", HTTPStatus.NOT_FOUND)

@ticket_bp.route('/ticket/<int:ticket_id>/users', methods=['GET'])
def get_users_by_ticket(ticket_id: int) -> Response:
    ticket = Ticket.query.get(ticket_id)
    if ticket:
        users = ticket.users
        return make_response(jsonify([user.put_into_dto() for user in users]), HTTPStatus.OK)
    return make_response("Ticket not found", HTTPStatus.NOT_FOUND)
