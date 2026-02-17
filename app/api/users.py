# Importáljuk a szükséges Flask és Flask-JWT-Extended modulokat.
from flask import jsonify, request, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity  # jwt_required: védelem; get_jwt_identity: a tokenből kiolvassa a bejelentkezett user ID-ját.
from app.api import bp
from models import db, User  # Adatbázis kapcsolat és User modell.
from app.errors import error_response


# Végpont az összes felhasználó lekérdezésére.
@bp.route("/users", methods=["GET"])
def get_users():
    # Lekérdezzük az összes felhasználót.
    users = User.query.all()
    # Visszaadjuk a felhasználók listáját JSON formátumban. A 'to_json' metódus gondoskodik róla, hogy a jelszó ne kerüljön bele.
    return jsonify([user.to_json() for user in users])


# Végpont egy felhasználó lekérdezésére ID alapján.
@bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    # Megkeressük a felhasználót ID alapján.
    user = User.query.get(id)
    # Ha nem létezik, 404-es hibát adunk.
    if user is None:
        return error_response(404)
    # Visszaadjuk az adatait JSON-ként.
    return jsonify(user.to_json())


# Végpont új felhasználó létrehozására (regisztráció).
@bp.route("/users", methods=["POST"])
def create_user():
    # Lekérjük a JSON adatokat a kérésből.
    data = request.get_json()
    # Ellenőrizzük, hogy a kötelező 'name' és 'password' mezők meg lettek-e adva.
    if not data or not data.get('name') or not data.get('password'):
        return error_response(400, "A 'name' és 'password' mezők kötelezőek.")

    # Ellenőrizzük, hogy a felhasználónév foglalt-e már.
    if User.query.filter_by(name=data['name']).first():
        return error_response(400, "A felhasználónév már foglalt.")

    # Létrehozunk egy új User objektumot a névvel.
    new_user = User(name=data['name'])
    # A 'set_password' metódus segítségével beállítjuk a hash-elt jelszót.
    new_user.set_password(data['password'])
    # Hozzáadjuk az új felhasználót az adatbázis-munkamenethez.
    db.session.add(new_user)
    # Véglegesítjük a változtatásokat.
    db.session.commit()

    # Létrehozzuk a választ.
    response = jsonify(new_user.to_json())
    # Beállítjuk a 201 Created státuszkódot.
    response.status_code = 201
    # A válasz fejlécébe beletesszük az új felhasználó URL-jét.
    response.headers["Location"] = url_for("api.get_user", id=new_user.id)
    return response


# Végpont egy felhasználó adatainak módosítására.
@bp.route("/users/<int:id>", methods=["PUT"])
@jwt_required  # Csak bejelentkezett felhasználó érheti el.
def update_user(id):
    # Lekérdezzük a tokenből a bejelentkezett felhasználó ID-ját.
    current_user_id = get_jwt_identity()
    # Ellenőrizzük, hogy a felhasználó a saját adatait próbálja-e módosítani.
    if id != current_user_id:
        # Ha nem, 403 Forbidden (Tiltott) hibát adunk.
        return error_response(403)

    # Lekérdezzük a módosítandó felhasználót az adatbázisból.
    user = User.query.get(id)
    if user is None:
        return error_response(404)

    data = request.get_json()
    if not data:
        return error_response(400, "Nincs adat a kérésben.")

    # Ha új nevet adtak meg, és az különbözik a régitől, ÉS már foglalt, akkor hibát dobunk.
    if 'name' in data and data['name'] != user.name and User.query.filter_by(name=data['name']).first():
        return error_response(400, "A felhasználónév már foglalt.")

    # Frissítjük a nevet, ha megadták.
    user.name = data.get('name', user.name)
    # Frissítjük a jelszót, ha megadták.
    if 'password' in data:
        user.set_password(data['password'])

    # Véglegesítjük a változtatásokat.
    db.session.commit()
    return jsonify(user.to_json())


# Végpont egy felhasználó törlésére.
@bp.route("/users/<int:id>", methods=["DELETE"])
@jwt_required  # Csak bejelentkezett felhasználó érheti el.
def delete_user(id):
    # Lekérdezzük a bejelentkezett felhasználó ID-ját.
    current_user_id = get_jwt_identity()
    # Ellenőrizzük, hogy a saját fiókját próbálja-e törölni.
    if id != current_user_id:
        return error_response(403)

    # Lekérdezzük a törlendő felhasználót.
    user = User.query.get(id)
    if user is None:
        return error_response(404)

    # Töröljük a felhasználót.
    db.session.delete(user)
    db.session.commit()
    # 204 No Content válasszal jelezzük a sikeres törlést.
    return "", 204
