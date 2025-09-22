from http import HTTPStatus
from flask import Blueprint, jsonify, request, make_response

from my_project.auth.controller import UserController
from my_project.auth.domain import User
from my_project.auth.service.general_service import GeneralService


user_bp = Blueprint('users', __name__, url_prefix='/users')
user_controller = UserController()
user_service = GeneralService()

@user_bp.route('', methods=['GET'])
def get_all_users():
    return make_response(jsonify(user_controller.find_all()), HTTPStatus.OK)

@user_bp.route('', methods=['POST'])
def create_user():
    content = request.get_json()
    user = User.create_from_dto(content)
    user_controller.create(user)
    return make_response(jsonify(user.put_into_dto()), HTTPStatus.CREATED)

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    return make_response(jsonify(user_controller.find_by_id(user_id)), HTTPStatus.OK)

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id: int):
    content = request.get_json()
    user = User.create_from_dto(content)
    user_controller.update(user_id, user)
    return make_response("User updated", HTTPStatus.OK)

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    user_controller.delete(user_id)
    return make_response("User deleted", HTTPStatus.OK)

@user_bp.route('/by-email/<string:email>', methods=['GET'])
def get_user_by_email(email: str):
    return make_response(jsonify(user_controller.get_user_by_email(email)), HTTPStatus.OK)

@user_bp.route('/by-city/<string:city>', methods=['GET'])
def get_users_by_city(city: str):
    return make_response(jsonify(user_controller.get_users_by_city(city)), HTTPStatus.OK)

