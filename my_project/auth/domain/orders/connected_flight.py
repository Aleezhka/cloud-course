from my_project import db
from my_project.auth.domain.i_dto import IDto
from typing import Dict, Any

class ConnectedFlight(db.Model, IDto):
    __tablename__ = "connected_flights"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    connected_flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))

    flight = db.relationship('Flight', foreign_keys=[flight_id], backref='departures')
    connected_flight = db.relationship('Flight', foreign_keys=[connected_flight_id], backref='arrivals')

    def __repr__(self) -> str:
        return f"ConnectedFlight(id={self.id}, flight_id={self.flight_id}, connected_flight_id={self.connected_flight_id})"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "flight_id": self.flight_id,
            "connected_flight_id": self.connected_flight_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> "ConnectedFlight":
        return ConnectedFlight(**dto_dict)
