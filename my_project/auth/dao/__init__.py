
from .orders.flight_dao import FlightDAO
from .orders.user_dao import UserDAO
from .orders.ticket_dao import TicketDAO
from .orders.ticket_history_dao import TicketHistoryDAO
from .orders.connected_flight_dao import ConnectedFlightDAO


flight_dao = FlightDAO()
users_dao = UserDAO()
ticket_dao = TicketDAO()
ticket_history_dao = TicketHistoryDAO()
connected_flight_dao = ConnectedFlightDAO()