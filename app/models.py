from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Ops(db.Model):
    buyer = db.Column(db.String(64))
    sku = db.Column(db.Integer, index=True, primary_key=True)
    ingredient = db.Column(db.String(400))

    def __repr__(self):
        return f"{self.buyer} - {self.sku}"


class PoDataTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_quantity = db.Column(db.Integer)
    mid_sku = db.Column(db.Integer)
    destination = db.Column(db.String(64))
    origin = db.Column(db.String(64))

    def __repr__(self):
        return f"Id:{self.id}, Sku:{self.mid_sku}"


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    ops_data = db.relationship("OpsData", backref="region")

    def __repr__(self):
        return f"{self.name}"


class OpsData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_units = db.Column(db.Integer)
    sku = db.Column(db.Integer)
    region_id = db.Column(db.Integer, db.ForeignKey("region.id"))

    def __repr__(self):
        return f"Id:{self.id}, Sku:{self.sku}"
