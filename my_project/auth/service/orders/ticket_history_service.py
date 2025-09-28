from my_project.auth.domain.orders.ticket_history import TicketHistory
from my_project.db import db

class TicketHistoryService:
    def find_by_ticket(self, ticket_id: int):
        """
        Знаходить всі записи історії для конкретного квитка.
        """
        return TicketHistory.query.filter_by(ticket_id=ticket_id).all()

    def create_ticket_history(self, data: dict):
        """
        Створює запис в історії для конкретного квитка.
        """
        ticket_history = TicketHistory(**data)
        db.session.add(ticket_history)
        db.session.commit()
        return ticket_history

ticket_history_service = TicketHistoryService()
