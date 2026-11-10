from flask import Flask, jsonify, render_template, request

if __package__:
    from .controller import AGVController, ControllerError, SimulatedAGVController
else:
    from controller import AGVController, ControllerError, SimulatedAGVController


def create_app(controller: AGVController | None = None) -> Flask:
    app = Flask(__name__)
    app.extensions["agv_controller"] = controller or SimulatedAGVController()

    def get_controller() -> AGVController:
        return app.extensions["agv_controller"]

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/api/state")
    def state():
        return jsonify(get_controller().get_state())

    @app.route("/api/mission/start", methods=["POST"])
    def start_mission():
        try:
            return jsonify(get_controller().start_mission())
        except ControllerError as error:
            return jsonify({"error": str(error)}), 400

    @app.route("/api/mission/pause", methods=["POST"])
    def pause_mission():
        return jsonify(get_controller().pause_mission())

    @app.route("/api/command", methods=["POST"])
    def command():
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not isinstance(data.get("action"), str):
            return jsonify({"error": "A command action is required"}), 400

        try:
            return jsonify(get_controller().command(data["action"]))
        except ControllerError as error:
            return jsonify({"error": str(error)}), 400

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
