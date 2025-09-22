from my_project import db
from datetime import datetime
from typing import Dict, Any

class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ticket_histories = db.relationship('TicketHistory', backref='ticket_ref', lazy='dynamic')

    def __repr__(self) -> str:
        return f"Ticket({self.id}, flight_id={self.flight_id}, purchase_date='{self.purchase_date}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "flight_id": self.flight_id,
            "purchase_date": self.purchase_date.isoformat()
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> "Ticket":
        return Ticket(**dto_dict)
