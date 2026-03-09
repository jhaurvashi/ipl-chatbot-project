from flask import Flask, jsonify, render_template, request
from ipl_service import IPLAnalyticsService, DataLoadError


def create_app():
    app = Flask(__name__)

    # Initialize IPL analytics service (loads CSV once at startup)
    ipl_service = IPLAnalyticsService()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/top-scorer", methods=["GET"])
    def api_top_scorer():
        try:
            top_scorer = ipl_service.get_overall_top_scorer()
        except DataLoadError as e:
            return jsonify({"error": str(e)}), 500

        if top_scorer is None:
            return jsonify({"error": "No scorer data available"}), 404

        return jsonify(top_scorer)

    @app.route("/api/winner-by-year", methods=["GET"])
    def api_winner_by_year():
        year = request.args.get("year", type=int)
        if not year:
            return jsonify({"error": "Query parameter 'year' is required and must be an integer"}), 400

        try:
            winner = ipl_service.get_winner_by_year(year)
        except DataLoadError as e:
            return jsonify({"error": str(e)}), 500

        if winner is None:
            return jsonify({"error": f"No winner data found for year {year}"}), 404

        return jsonify(winner)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

