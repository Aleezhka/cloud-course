
from .orders.flight_service import FlightService
from .orders.user_service import UserService
from .orders.ticket_service import TicketService
from .orders.ticket_history_service import TicketHistoryService
from .orders.connected_flight_service import ConnectedFlightService

flight_service = FlightService()
user_service = UserService()
ticket_service = TicketService()
ticket_history_service = TicketHistoryService()
connected_flight_service = ConnectedFlightService()





