from flask import Flask, jsonify


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request"}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method Not Allowed"}), 405

    @app.errorhandler(415)
    def unsupported_media_type(error):
        return jsonify({"error": "Unsupported Media Type"})

    @app.errorhandler(422)
    def unprocessable_content(error):
        return jsonify({"error": "Unprocessable Content"}), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal Server Error"}), 500
