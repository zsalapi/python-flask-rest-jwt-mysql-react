# Import necessary modules.
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,  # Functions for creating tokens.
    jwt_required, jwt_refresh_token_required,  # Decorators for protecting endpoints.
    get_jwt_identity, get_raw_jwt  # Helper functions for reading token data.
)
from app.auth import bp  # The authentication blueprint.
from app.errors import error_response  # Uniform error handler.
from models import db, User, TokenBlocklist  # Database models.
from datetime import datetime  # For handling date and time.


# Login endpoint.
@bp.route("/login", methods=["POST"])
def login():
    # Check if the request is in JSON format.
    if not request.is_json:
        return error_response(400)

    # Read the JSON data.
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Check if username and password are provided.
    if not username or not password:
        return error_response(400, "Username or password missing.")

    # Find the user by name in the database.
    user = User.query.filter_by(name=username).first()

    # Check if the user exists and the provided password is correct.
    # 'check_password' compares the hashed password with the received password.
    if not user or not user.check_password(password):
        return error_response(401, "Username or password invalid.")

    # If login is successful, create an access token and a refresh token.
    # The 'identity' is the "owner" of the token, here we store the user's ID in it.
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    # Return the tokens to the client.
    return jsonify(access_token=access_token, refresh_token=refresh_token)


# Endpoint for refreshing the access token.
@bp.route("/refresh", methods=["POST"])
@jwt_refresh_token_required  # This endpoint can only be accessed with a valid REFRESH token.
def refresh():
    # Read the user ID from the refresh token.
    user_id = get_jwt_identity()
    # Query the user from the database.
    user = User.query.get(user_id)
    if not user:
        return error_response(401, "Unknown user.")
    # Create a new access token.
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


# Endpoint for logout (revoking access token).
@bp.route("/logout", methods=["DELETE"])
@jwt_required  # This endpoint can only be accessed with a valid ACCESS token.
def logout_access_token():
    # Read the unique identifier (jti) of the token.
    jti = get_raw_jwt()["jti"]
    # Add the jti to the 'TokenBlocklist' table, indicating that this token is invalid.
    db.session.add(TokenBlocklist(jti=jti, created_at=datetime.now()))
    db.session.commit()
    return jsonify(message="Successfully logged out.")


# Endpoint for logout (revoking refresh token).
@bp.route("/logout2", methods=["DELETE"])
@jwt_refresh_token_required  # This endpoint can only be accessed with a valid REFRESH token.
def logout_refresh_token():
    # Same logic as for logout_access_token, but for the refresh token.
    jti = get_raw_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti, created_at=datetime.now()))
    db.session.commit()
    return jsonify(message="Successfully logged out.")
