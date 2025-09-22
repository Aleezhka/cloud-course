
from .orders.flight_controller import FlightController
from .orders.user_controller import UserController
from .orders.ticket_controller import TicketController
from .orders.ticket_history_controller import TicketHistoryController
from .orders.connected_flight_controller import ConnectedFlightController


flight_controller = FlightController()
user_controller = UserController()
ticket_controller = TicketController()
ticket_history_controller = TicketHistoryController()
connected_flight_controller = ConnectedFlightController()




