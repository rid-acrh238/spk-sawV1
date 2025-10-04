from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pasien(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    usia = db.Column(db.Integer)
    tekanan_sistolik = db.Column(db.Integer)
    tekanan_diastolik = db.Column(db.Integer)

class Kriteria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    bobot = db.Column(db.Float)
    jenis = db.Column(db.String(10))  # 'benefit' atau 'cost'

class Nilai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pasien_id = db.Column(db.Integer, db.ForeignKey('pasien.id'))
    kriteria_id = db.Column(db.Integer, db.ForeignKey('kriteria.id'))
    value = db.Column(db.Float)
