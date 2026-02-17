# Import necessary packages and modules.
from flask import Flask
# The core of the Flask framework.
from config import Config
# Our configuration settings (from config.py).
from flask_jwt_extended import JWTManager
# For handling JWT (JSON Web Token).
from flask_cors import CORS
# To allow requests from the browser (Cross-Origin Resource Sharing).
from models import db, TokenBlocklist
# Our database models (from models.py).
from commands import db_seed
# Our command for seeding the database (from commands.py).


# Create a JWTManager instance, which handles token management.
jwt = JWTManager()


# This is a special "decorator" from JWTManager.
# It runs on every call to a protected endpoint to check if the received token is still valid.
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """
    Callback function that checks if a JWT token has been revoked.
    On logout, the token's identifier (jti) is stored in the database.
    This function checks if the incoming token's jti is on the revoked list.
    """
    # Read the unique identifier (jti) of the token.
    jti = decrypted_token["jti"]
    # Look for this jti in the TokenBlocklist table.
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    # If the token exists in the table, it means it has been revoked (the user has logged out).
    # 'is not None' returns a boolean value (True/False).
    return token is not None


# This is the "application factory" function.
# It's good practice to create the app this way because it's easier to test and create multiple instances of it.
def create_app(config_class=Config):
    # Create the Flask application instance.
    app = Flask(__name__)
    # Load the configuration from the Config class defined in config.py.
    app.config.from_object(config_class)
    # Enable CORS on the application, which allows
    # the frontend (another "origin", e.g., localhost:3000) to send requests to the backend (localhost:5000).
    CORS(app)

    # Initialize the database manager (SQLAlchemy) with the application.
    db.init_app(app)
    # Initialize the JWT manager with the application.
    jwt.init_app(app)

    # Register our command-line command ('flask db-seed').
    app.cli.add_command(db_seed)

    # Import and register the "blueprints".
    # Blueprints help to logically separate parts of the application (e.g., API, authentication).
    from app.api import bp as api_bp
    # The routes defined in 'api_bp' will be accessible with the '/api' prefix (e.g., /api/ships).
    app.register_blueprint(api_bp, url_prefix="/api")

    from app.auth import bp as auth_bp
    # The routes defined in 'auth_bp' will be accessible with the '/auth' prefix (e.g., /auth/login).
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Within the application context, we create the database tables if they don't already exist.
    # This 'db.create_all()' command goes through the classes defined in 'models.py' and creates the schema.
    with app.app_context():
        db.create_all()

    # Return the configured application instance.
    return app
