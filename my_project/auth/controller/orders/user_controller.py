from typing import List
from my_project.auth.service import UserService
from my_project.auth.controller.general_controller import GeneralController

class UserController(GeneralController):
    _service = UserService()

    def get_user_by_email(self, email: str) -> List[object]:
        users = self._service.find_user_by_email(email)
        return [user.put_into_dto() for user in users]

    def get_users_by_city(self, city: str) -> List[object]:
        users = self._service.find_users_by_city(city)
        return [user.put_into_dto() for user in users]
