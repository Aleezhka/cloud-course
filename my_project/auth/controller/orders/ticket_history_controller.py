from my_project.auth.service import ticket_history_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain import TicketHistory
from my_project.db import db

class TicketHistoryController(GeneralController):
    _service = ticket_history_service

    def get_all_ticket_history(self):
        history = TicketHistory.query.all()
        return [self.ticket_history_to_dict(item) for item in history]

    def get_ticket_history_by_ticket(self, ticket_id):
        history = TicketHistory.query.filter_by(ticket_id=ticket_id).all()
        return [self.ticket_history_to_dict(item) for item in history]

    def create_ticket_history(self, data):
        new_history = TicketHistory(
            ticket_id=data['ticket_id'],
            user_id=data['user_id'],
            status=data['status'],
        )
        db.session.add(new_history)
        db.session.commit()
        return self.ticket_history_to_dict(new_history)

    def delete_ticket_history(self, ticket_history_id):
        ticket_history = TicketHistory.query.get(ticket_history_id)
        if ticket_history:
            db.session.delete(ticket_history)
            db.session.commit()
            return {'message': 'History record deleted successfully'}
        return {'message': 'Ticket history not found'}, 404

    def ticket_history_to_dict(self, ticket_history):
        return {
            'id': ticket_history.id,
            'ticket_id': ticket_history.ticket_id,
            'user_id': ticket_history.user_id,
            'status': ticket_history.status,
            'change_time': ticket_history.change_time,
        }