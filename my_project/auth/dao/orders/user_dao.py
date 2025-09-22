from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain import User

class UserDAO(GeneralDAO):
    _domain_type = User

    def find_by_email(self, email: str) -> List[User]:
        return self._session.query(User).filter(User.email == email).all()

    def find_users_by_city(self, city: str) -> List[User]:
        return self._session.query(User).filter(User.city == city).all()

