from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Ship(db.Model):
    __tablename__ = 'ships'

    id = db.Column(db.Integer, primary_key=True)
    affiliation = db.Column(db.String(100))
    category = db.Column(db.String(100))
    crew = db.Column(db.Integer)
    length = db.Column(db.Integer)
    manufacturer = db.Column(db.String(200))
    model = db.Column(db.String(100))
    roles = db.Column(db.JSON)
    ship_class = db.Column(db.String(100))

    def to_json(self):
        return {
            "id": self.id,
            "affiliation": self.affiliation,
            "category": self.category,
            "crew": self.crew,
            "length": self.length,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "roles": self.roles,
            "ship_class": self.ship_class
        }

class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)