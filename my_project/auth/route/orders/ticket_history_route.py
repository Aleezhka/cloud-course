from flask import Blueprint, request, jsonify, make_response
from my_project.auth.controller.orders.ticket_history_controller import TicketHistoryController

ticket_history_bp = Blueprint('ticket_history_bp', __name__)

ticket_history_controller = TicketHistoryController()

@ticket_history_bp.route('/ticket/history/all', methods=['GET'])
def get_all_ticket_history():
    history = ticket_history_controller.get_all_ticket_history()
    return make_response(jsonify(history), 200)

@ticket_history_bp.route('/ticket/<int:ticket_id>/history', methods=['GET'])
def get_ticket_history(ticket_id):
    history = ticket_history_controller.get_ticket_history_by_ticket(ticket_id)
    return make_response(jsonify(history), 200)

@ticket_history_bp.route('/ticket/history', methods=['POST'])
def create_ticket_history():
    data = request.json
    history = ticket_history_controller.create_ticket_history(data)
    return make_response(jsonify(history), 201)

@ticket_history_bp.route('/ticket/history/<int:ticket_history_id>', methods=['DELETE'])
def delete_ticket_history(ticket_history_id):
    result = ticket_history_controller.delete_ticket_history(ticket_history_id)
    return make_response(jsonify(result), 200 if 'message' in result else 404)