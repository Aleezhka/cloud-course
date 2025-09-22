from http import HTTPStatus
from flask import Blueprint, jsonify, request, make_response

from my_project.auth.controller import FlightController
from my_project.auth.domain import Flight

flight_bp = Blueprint('flights', __name__, url_prefix='/flights')
flight_controller = FlightController()

@flight_bp.route('', methods=['GET'])
def get_all_flights():
    return make_response(jsonify(flight_controller.get_all_flights()), HTTPStatus.OK)

@flight_bp.route('', methods=['POST'])
def create_flight():
    content = request.get_json()
    flight = Flight.create_from_dto(content)
    flight_controller.create(flight)
    return make_response(jsonify(flight.put_into_dto()), HTTPStatus.CREATED)

@flight_bp.route('/<int:flight_id>', methods=['GET'])
def get_flight(flight_id: int):
    flight = flight_controller.find_flight_by_id(flight_id)
    if flight:
        return make_response(jsonify(flight), HTTPStatus.OK)
    return make_response({"error": "Flight not found"}, HTTPStatus.NOT_FOUND)

@flight_bp.route('/<int:flight_id>', methods=['PUT'])
def update_flight(flight_id: int):
    content = request.get_json()
    flight = Flight.create_from_dto(content)
    flight_controller.update(flight_id, flight)
    return make_response("Flight updated", HTTPStatus.OK)

@flight_bp.route('/<int:flight_id>', methods=['DELETE'])
def delete_flight(flight_id: int):
    flight_controller.delete(flight_id)
    return make_response("Flight deleted", HTTPStatus.OK)

@flight_bp.route('/by-airline/<int:airline_id>', methods=['GET'])
def get_flights_by_airline(airline_id: int):
    return make_response(jsonify(flight_controller.get_flights_by_airline(airline_id)), HTTPStatus.OK)
