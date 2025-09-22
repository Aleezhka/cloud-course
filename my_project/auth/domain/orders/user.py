from my_project import db
from datetime import datetime
from typing import Dict, Any

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=True)

    ticket_histories = db.relationship('TicketHistory', backref='ticket_user', lazy='dynamic')

    def __repr__(self) -> str:
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', city='{self.city}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "city": self.city
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> "User":
        return User(**dto_dict)
