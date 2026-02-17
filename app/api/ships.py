# Importáljuk a szükséges Flask és Flask-JWT-Extended modulokat.
from flask import jsonify, request, url_for
# jsonify: Python dict-ből JSON választ készít; request: a bejövő kérés adatai; url_for: URL-t generál egy végponthoz.
from flask_jwt_extended import jwt_required  # Dekorátor, ami megköveteli az érvényes JWT tokent a végpont eléréséhez.
from app.api import bp  # A blueprint példányunk, amire a végpontokat regisztráljuk.
from models import db, Ship  # Az adatbázis kapcsolat és a Ship modell.
from app.errors import error_response  # Egységes hibakezelő függvény.


# Végpont az összes hajó lekérdezésére.
@bp.route("/ships", methods=["GET"])
def get_ships():
    # Lekérdezzük az összes rekordot a 'ships' táblából az SQLAlchemy segítségével.
    ships = Ship.query.all()
    # A kapott 'Ship' objektumok listáját átalakítjuk JSON formátumú listává a 'to_json' metódussal, majd visszaadjuk.
    return jsonify([ship.to_json() for ship in ships])


# Végpont egy konkrét hajó lekérdezésére azonosító (ID) alapján.
@bp.route("/ships/<int:id>", methods=["GET"])
def get_ship(id):
    # Megkeressük a hajót az ID alapján. A 'get' egy gyors keresés a primary key-re.
    ship = Ship.query.get(id)
    # Ha a hajó nem található (a 'get' None-t ad vissza), 404-es hibát küldünk.
    if ship is None:
        return error_response(404)
    # Ha megvan, visszaadjuk a hajó adatait JSON formátumban.
    return jsonify(ship.to_json())


# Végpont új hajó létrehozására.
@bp.route("/ships", methods=["POST"])
@jwt_required  # Csak bejelentkezett felhasználó (érvényes access token-nel) érheti el.
def create_ship():
    # Lekérjük a kérés törzséből a JSON adatokat.
    data = request.get_json()
    # Ha nincs adat, hibát dobunk.
    if not data:
        return error_response(400, "Nincs adat a kérésben.")

    # Ellenőrizzük, hogy a kötelező mezők meg lettek-e adva.
    required_fields = ['model', 'ship_class']
    if not all(field in data for field in required_fields):
        return error_response(400, f"Hiányzó kötelező mezők: {', '.join(required_fields)}")

    # Létrehozunk egy új 'Ship' objektumot a kapott adatokból.
    new_ship = Ship(
        affiliation=data.get('affiliation'),
        category=data.get('category'),
        crew=data.get('crew'),
        length=data.get('length'),
        manufacturer=data.get('manufacturer'),
        model=data.get('model'),
        roles=data.get('roles'),
        ship_class=data.get('ship_class')
    )
    # Hozzáadjuk az új objektumot az adatbázis "session"-höz (munkamenethez).
    db.session.add(new_ship)
    # Véglegesítjük a változtatásokat az adatbázisban.
    db.session.commit()

    # Visszaadjuk az újonnan létrehozott hajó adatait JSON-ként.
    response = jsonify(new_ship.to_json())
    # A HTTP státuszkódot 201 Created-re állítjuk, jelezve a sikeres létrehozást.
    response.status_code = 201
    # A válasz 'Location' fejlécébe beletesszük az új erőforrás URL-jét.
    response.headers["Location"] = url_for("api.get_ship", id=new_ship.id)
    return response


# Végpont egy meglévő hajó módosítására.
@bp.route("/ships/<int:id>", methods=["PUT"])
@jwt_required  # Csak bejelentkezett felhasználó érheti el.
def update_ship(id):
    # Megkeressük a módosítandó hajót az ID alapján.
    ship = Ship.query.get(id)
    # Ha nem létezik, 404-es hibát adunk.
    if ship is None:
        return error_response(404)

    # Lekérjük a kérés törzséből a JSON adatokat.
    data = request.get_json()
    if not data:
        return error_response(400, "Nincs adat a kérésben.")

    # Frissítjük a hajó attribútumait a kapott adatokkal.
    # A 'data.get(key, default_value)' biztonságosabb, mert ha egy kulcs hiányzik, a meglévő értéket tartja meg.
    ship.affiliation = data.get('affiliation', ship.affiliation)
    ship.category = data.get('category', ship.category)
    ship.crew = data.get('crew', ship.crew)
    ship.length = data.get('length', ship.length)
    ship.manufacturer = data.get('manufacturer', ship.manufacturer)
    ship.model = data.get('model', ship.model)
    ship.roles = data.get('roles', ship.roles)
    ship.ship_class = data.get('ship_class', ship.ship_class)

    # Véglegesítjük a változtatásokat az adatbázisban.
    db.session.commit()
    # Visszaadjuk a frissített hajó adatait.
    return jsonify(ship.to_json())


# Végpont egy hajó törlésére.
@bp.route("/ships/<int:id>", methods=["DELETE"])
@jwt_required  # Csak bejelentkezett felhasználó érheti el.
def delete_ship(id):
    # Megkeressük a törlendő hajót az ID alapján.
    ship = Ship.query.get(id)
    # Ha nem létezik, 404-es hibát adunk.
    if ship is None:
        return error_response(404)
    # Töröljük az objektumot az adatbázis "session"-ből.
    db.session.delete(ship)
    # Véglegesítjük a változtatást.
    db.session.commit()
    # Sikeres törlés esetén 204 No Content státuszkódot adunk vissza üres válasszal.
    return "", 204
