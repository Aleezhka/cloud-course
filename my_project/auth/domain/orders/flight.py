from my_project import db
from my_project.auth.domain.i_dto import IDto
from typing import Dict, Any


class Flight(db.Model, IDto):
    __tablename__ = "flights"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    airline_id = db.Column(db.Integer)
    departure_airport_id = db.Column(db.Integer)
    arrival_airport_id = db.Column(db.Integer)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    ticket_price = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self) -> str:
        return (f"Flight(id={self.id}, airline_id={self.airline_id}, "
                f"departure_airport_id={self.departure_airport_id}, arrival_airport_id={self.arrival_airport_id}, "
                f"departure_time='{self.departure_time}', arrival_time='{self.arrival_time}', "
                f"ticket_price={self.ticket_price})")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "airline_id": self.airline_id,
            "departure_airport_id": self.departure_airport_id,
            "arrival_airport_id": self.arrival_airport_id,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "ticket_price": str(self.ticket_price),
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> "Flight":
        return Flight(**dto_dict)
