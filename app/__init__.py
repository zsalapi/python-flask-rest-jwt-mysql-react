# Importáljuk a szükséges csomagokat és modulokat.
from flask import Flask
# A Flask keretrendszer magja.
from config import Config
# A konfigurációs beállításaink (config.py-ból).
from flask_jwt_extended import JWTManager
# A JWT (JSON Web Token) kezeléséhez.
from flask_cors import CORS
# A böngészőből érkező kérések engedélyezéséhez (Cross-Origin Resource Sharing).
from models import db, TokenBlocklist
# Az adatbázis modelljeink (models.py-ból).
from commands import db_seed
# Az adatbázis feltöltésére szolgáló parancsunk (commands.py-ból).


# Létrehozunk egy JWTManager példányt, ami a tokenek kezelését végzi.
jwt = JWTManager()


# Ez egy speciális "dekorátor" a JWTManager-től.
# Minden védett végpont hívásakor lefut, hogy ellenőrizze, a kapott token érvényes-e még.
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """
    Visszahívó függvény, ami ellenőrzi, hogy egy JWT token vissza lett-e vonva.
    A kijelentkezéskor a token azonosítóját (jti) eltároljuk az adatbázisban.
    Ez a függvény megnézi, hogy a bejövő token jti-je szerepel-e a visszavontak listáján.
    """
    # Kiolvassuk a token egyedi azonosítóját (jti).
    jti = decrypted_token["jti"]
    # Megkeressük a TokenBlocklist táblában ezt a jti-t.
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    # Ha a token létezik a táblában, az azt jelenti, hogy vissza lett vonva (a felhasználó kijelentkezett).
    # A 'is not None' egy logikai értéket (True/False) ad vissza.
    return token is not None


# Ez az "alkalmazás gyár" (application factory) függvény.
# Azért jó gyakorlat így létrehozni az appot, mert könnyebb tesztelni és több példányt is létrehozni belőle.
def create_app(config_class=Config):
    # Létrehozzuk a Flask alkalmazás példányát.
    app = Flask(__name__)
    # Betöltjük a konfigurációt a config.py-ban definiált Config osztályból.
    app.config.from_object(config_class)
    # Engedélyezzük a CORS-t az alkalmazáson, ami lehetővé teszi,
    # hogy a frontend (másik "origin", pl. localhost:3000) kéréseket küldhessen a backendnek (localhost:5000).
    CORS(app)

    # Inicializáljuk az adatbázis-kezelőt (SQLAlchemy) az alkalmazással.
    db.init_app(app)
    # Inicializáljuk a JWT-kezelőt az alkalmazással.
    jwt.init_app(app)

    # Regisztráljuk a parancssori parancsunkat ('flask db-seed').
    app.cli.add_command(db_seed)

    # Importáljuk és regisztráljuk a "blueprint"-eket.
    # A blueprint-ek segítségével logikailag szétválaszthatjuk az alkalmazás részeit (pl. API, authentikáció).
    from app.api import bp as api_bp
    # Az 'api_bp'-ben definiált útvonalak a '/api' előtaggal lesznek elérhetők (pl. /api/ships).
    app.register_blueprint(api_bp, url_prefix="/api")

    from app.auth import bp as auth_bp
    # Az 'auth_bp'-ben definiált útvonalak a '/auth' előtaggal lesznek elérhetők (pl. /auth/login).
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Az alkalmazás kontextusán belül létrehozzuk az adatbázis táblákat, ha még nem léteznek.
    # Ez a 'db.create_all()' parancs végignézi a 'models.py'-ban definiált osztályokat és létrehozza a sémát.
    with app.app_context():
        db.create_all()

    # Visszaadjuk a beállított alkalmazás példányt.
    return app
