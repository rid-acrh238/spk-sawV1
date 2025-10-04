from flask import Flask, render_template
from models import db, Pasien, Kriteria, Nilai
from saw import hitung_saw

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    pasien = Pasien.query.all()
    kriteria = Kriteria.query.all()
    return render_template('index.html', pasien=pasien, kriteria=kriteria)

#form tambah pasien
@app.route('/tambah_pasien', methods=['GET', 'POST'])
def tambah_pasien():
    if request.method == 'POST':
        nama = request.form['nama']
        usia = request.form['usia']
        tekanan_sistolik = request.form['tekanan_sistolik']
        tekanan_diastolik = request.form['tekanan_diastolik']
        pasien = Pasien(nama=nama, usia=usia, tekanan_sistolik=tekanan_sistolik, tekanan_diastolik=tekanan_diastolik)
        db.session.add(pasien)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/tambah_kriteria', methods=['GET', 'POST'])
def tambah_kriteria():
    if request.method == 'POST':
        nama = request.form['nama']
        bobot = float(request.form['bobot'])
        jenis = request.form['jenis']
        kriteria = Kriteria(nama=nama, bobot=bobot, jenis=jenis)
        db.session.add(kriteria)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('kriteria.html')

@app.route('/input_nilai', methods=['GET', 'POST'])
def input_nilai():
    pasien_list = Pasien.query.all()
    kriteria_list = Kriteria.query.all()
    if request.method == 'POST':
        for k in kriteria_list:
            for p in pasien_list:
                value = float(request.form.get(f'nilai_{p.id}_{k.id}', 0))
                nilai = Nilai.query.filter_by(pasien_id=p.id, kriteria_id=k.id).first()
                if nilai:
                    nilai.value = value
                else:
                    new_nilai = Nilai(pasien_id=p.id, kriteria_id=k.id, value=value)
                    db.session.add(new_nilai)

@app.route('/hitung')
def hasil():
    hasil_saw = hitung_saw()
    return render_template('results.html', hasil=hasil_saw)

if __name__ == '__main__':
    app.run(debug=True)
