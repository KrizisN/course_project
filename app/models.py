from app import db


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
