"""Main Flask application."""
from flask import Flask, jsonify
from flask_cors import CORS

from app.db import Base, engine
from app.core.config import get_config
from app.shared.exceptions import AppException
from app.features.auth.routes import auth_bp
from app.features.users.routes import users_bp
from app.features.clinics.routes import clinics_bp


def create_app():
    """Create and configure Flask application."""
    config = get_config()
    
    app = Flask(__name__)
    app.config['DEBUG'] = config.DEBUG
    
    # Enable CORS with explicit configuration
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Create all database tables
    Base.metadata.create_all(bind=engine)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(clinics_bp)
    
    # Error handlers
    @app.errorhandler(AppException)
    def handle_app_exception(e):
        """Handle custom application exceptions."""
        return jsonify({
            "success": False,
            "error": e.error_code,
            "message": e.message,
        }), e.status_code
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """Handle 404 errors."""
        return jsonify({
            "success": False,
            "error": "NOT_FOUND",
            "message": "Resource not found",
        }), 404
    
    @app.errorhandler(500)
    def handle_server_error(e):
        """Handle 500 errors."""
        return jsonify({
            "success": False,
            "error": "SERVER_ERROR",
            "message": "Internal server error",
        }), 500
    
    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy"}), 200
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
