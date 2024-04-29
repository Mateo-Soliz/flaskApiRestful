from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GastosModal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.String(200), nullable=False)
    concepto = db.Column(db.String(200), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(200))

class IngresosModal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.String(200), nullable=False)
    concepto = db.Column(db.String(200), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(200))

class DeudasModal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deudor = db.Column(db.String(200), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    desde_cuando = db.Column(db.String(200), nullable=False)
    comentarios = db.Column(db.String(200))
    resuelto = db.Column(db.Boolean, nullable=False)