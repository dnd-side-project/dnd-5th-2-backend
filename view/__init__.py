from .auth_view import create_auth_blueprint


def create_endpoints(app, services):
    @app.route("/ping", methods=["GET"])
    def ping():
        return "pong"

    app.register_blueprint(create_auth_blueprint(services))
