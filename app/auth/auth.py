# Importáljuk a szükséges modulokat.
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,  # Tokenek létrehozására szolgáló függvények.
    jwt_required, jwt_refresh_token_required,  # Dekorátorok a végpontok védelmére.
    get_jwt_identity, get_raw_jwt  # Segédfüggvények a token adatainak kiolvasásához.
)
from app.auth import bp  # Az authentikációs blueprint.
from app.errors import error_response  # Egységes hibakezelő.
from models import db, User, TokenBlocklist  # Adatbázis modellek.
from datetime import datetime  # Dátum és idő kezeléséhez.


# Bejelentkezési végpont.
@bp.route("/login", methods=["POST"])
def login():
    # Ellenőrizzük, hogy a kérés JSON formátumú-e.
    if not request.is_json:
        return error_response(400)

    # Kiolvassuk a JSON adatokat.
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Ellenőrizzük, hogy a felhasználónév és jelszó meg van-e adva.
    if not username or not password:
        return error_response(400, "Username or password missing.")

    # Megkeressük a felhasználót a neve alapján az adatbázisban.
    user = User.query.filter_by(name=username).first()

    # Ellenőrizzük, hogy a felhasználó létezik-e, és a megadott jelszó helyes-e.
    # A 'check_password' a hash-elt jelszót hasonlítja össze a kapott jelszóval.
    if not user or not user.check_password(password):
        return error_response(401, "Username or password invalid.")

    # Ha a bejelentkezés sikeres, létrehozunk egy access tokent és egy refresh tokent.
    # Az 'identity' a token "tulajdonosa", itt a felhasználó ID-ját tároljuk el benne.
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    # Visszaadjuk a tokeneket a kliensnek.
    return jsonify(access_token=access_token, refresh_token=refresh_token)


# Végpont az access token frissítésére.
@bp.route("/refresh", methods=["POST"])
@jwt_refresh_token_required  # Ezt a végpontot csak érvényes REFRESH token-nel lehet elérni.
def refresh():
    # Kiolvassuk a felhasználó ID-ját a refresh tokenből.
    user_id = get_jwt_identity()
    # Lekérdezzük a felhasználót az adatbázisból.
    user = User.query.get(user_id)
    if not user:
        return error_response(401, "Unknown user.")
    # Létrehozunk egy új access tokent.
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


# Végpont a kijelentkezéshez (access token visszavonása).
@bp.route("/logout", methods=["DELETE"])
@jwt_required  # Ezt a végpontot csak érvényes ACCESS token-nel lehet elérni.
def logout_access_token():
    # Kiolvassuk a token egyedi azonosítóját (jti).
    jti = get_raw_jwt()["jti"]
    # Hozzáadjuk a jti-t a 'TokenBlocklist' táblához, jelezve, hogy ez a token érvénytelen.
    db.session.add(TokenBlocklist(jti=jti, created_at=datetime.now()))
    db.session.commit()
    return jsonify(message="Successfully logged out.")


# Végpont a kijelentkezéshez (refresh token visszavonása).
@bp.route("/logout2", methods=["DELETE"])
@jwt_refresh_token_required  # Ezt a végpontot csak érvényes REFRESH token-nel lehet elérni.
def logout_refresh_token():
    # Ugyanaz a logika, mint a logout_access_token-nél, csak refresh tokenre.
    jti = get_raw_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti, created_at=datetime.now()))
    db.session.commit()
    return jsonify(message="Successfully logged out.")
