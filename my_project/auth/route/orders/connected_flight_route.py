from http import HTTPStatus
from flask import Blueprint, jsonify, request, make_response

from my_project.auth.controller import ConnectedFlightController
from my_project.auth.domain import ConnectedFlight

connected_flight_bp = Blueprint('connected_flights', __name__, url_prefix='/connected_flights')
connected_flight_controller = ConnectedFlightController()

@connected_flight_bp.route('', methods=['GET'])
def get_all_connected_flights():
    return make_response(jsonify(connected_flight_controller.get_all_connected_flights()), HTTPStatus.OK)

@connected_flight_bp.route('', methods=['POST'])
def create_connected_flight():
    content = request.get_json()
    connected_flight = ConnectedFlight.create_from_dto(content)
    connected_flight_controller.create(connected_flight)
    return make_response(jsonify(connected_flight.put_into_dto()), HTTPStatus.CREATED)

@connected_flight_bp.route('/<int:connected_flight_id>', methods=['GET'])
def get_connected_flight(connected_flight_id: int):
    connected_flight = connected_flight_controller.find_connected_flight_by_id(connected_flight_id)
    if connected_flight:
        return make_response(jsonify(connected_flight), HTTPStatus.OK)
    return make_response({"error": "Connected flight not found"}, HTTPStatus.NOT_FOUND)

@connected_flight_bp.route('/<int:connected_flight_id>', methods=['PUT'])
def update_connected_flight(connected_flight_id: int):
    content = request.get_json()
    connected_flight = ConnectedFlight.create_from_dto(content)
    connected_flight_controller.update(connected_flight_id, connected_flight)
    return make_response("Connected flight updated", HTTPStatus.OK)

@connected_flight_bp.route('/<int:connected_flight_id>', methods=['DELETE'])
def delete_connected_flight(connected_flight_id: int):
    connected_flight_controller.delete(connected_flight_id)
    return make_response("Connected flight deleted", HTTPStatus.OK)

@connected_flight_bp.route('/for-flight/<int:flight_id>', methods=['GET'])
def get_connected_flights_for_flight(flight_id: int):
    return make_response(jsonify(connected_flight_controller.get_connected_flights_for_flight(flight_id)), HTTPStatus.OK)
