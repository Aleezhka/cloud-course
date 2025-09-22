from my_project import db
from datetime import datetime
from typing import Dict, Any

class TicketHistory(db.Model):
    __tablename__ = "ticket_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    change_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ticket = db.relationship('Ticket', backref=db.backref('history', lazy='dynamic'))

    user = db.relationship('User', backref=db.backref('user_ticket_histories', lazy='dynamic'))

    def __repr__(self) -> str:
        return (f"TicketHistory(id={self.id}, ticket_id={self.ticket_id}, "
                f"user_id={self.user_id}, status='{self.status}', "
                f"change_time='{self.change_time}')")

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "status": self.status,
            "change_time": self.change_time.isoformat(),
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> "TicketHistory":
        return TicketHistory(**dto_dict)
