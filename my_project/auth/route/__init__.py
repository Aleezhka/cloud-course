from flask import Flask

from .error_handler import err_handler_bp


def register_routes(app: Flask) -> None:
    app.register_blueprint(err_handler_bp)

    from .orders.flight_route import flight_bp
    from .orders.user_route import user_bp
    from .orders.ticket_route import ticket_bp
    from .orders.ticket_history_route import ticket_history_bp
    from .orders.connected_flight_route import connected_flight_bp

    app.register_blueprint(flight_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(ticket_history_bp)
    app.register_blueprint(connected_flight_bp)