from typing import List
from my_project.auth.dao import UserDAO
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain import User


class UserService(GeneralService):
    _dao = UserDAO()

    def find_user_by_email(self, email: str) -> List[User]:
        return self._dao.find_by_email(email)

    def find_users_by_city(self, city: str) -> List[User]:
        return self._dao.find_users_by_city(city)
