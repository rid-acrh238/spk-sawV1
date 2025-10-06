import os
from flask import Flask, render_template
from models import db, Pasien, Kriteria, Nilai
from saw import hitung_saw
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'os.urandom'

#biasr database jadi dinamis
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
#db = SQLAlchemy(app)

@app.cli.command("init-db")
def init_db_command():
    with app.app_context():
        db.create_all()
    print("Database telah diinisialisasi")

@app.route('/')
def index():
    pasien_list = Pasien.query.order_by(Pasien.nama).all()
    #pasien = Pasien.query.all()
    #kriteria = Kriteria.query.all()
    #return render_template('index.html', pasien=pasien, kriteria=kriteria)
    return render_template('index.html', pasien_list=pasien_list)

#form tambah pasien
@app.route('/tambah_pasien', methods=['GET', 'POST'])
def tambah_pasien():
    if request.method == 'POST':
        # Validasi sederhana
        if not request.form['nama'] or not request.form['tanggal_lahir']:
            flash('Nama dan Tanggal Lahir wajib diisi.', 'danger')
            return render_template('tambah_pasien.html') # Tetap di halaman form

        try:
            tanggal_lahir_dt = date.fromisoformat(request.form['tanggal_lahir'])
        except ValueError:
            flash('Format Tanggal Lahir tidak valid.', 'danger')
            return render_template('tambah_pasien.html')
        
        #Cek apabila nama terduplikasi
        if Pasien.query.filter_by(nama=request.form['nama']).first():
            flash(f"Pasien dengan nama '{request.form['nama']}' sudah ada.", 'warning')
            return render_template('tambah_pasien.html')

        pasien = Pasien(
            nama=request.form['nama'],
            tanggal_lahir=tanggal_lahir_dt
            # tambahkan alamat jika ada di form dan model
        )
        db.session.add(pasien)
        db.session.commit()
        flash(f'Pasien "{pasien.nama}" berhasil ditambahkan.', 'success')
        return redirect(url_for('index'))
    # Untuk metode GET, tampilkan form
    return render_template('tambah_pasien.html') # Buat file HTML terpisah untuk form ini

@app.route('/tambah_kriteria', methods=['GET', 'POST'])
def tambah_kriteria():
    if request.method == 'POST':
        nama = request.form.get('nama')
        jenis = request.form.get('jenis')
        if not nama or not jenis:
            flash('Nama dan Jenis kriteria wajib diiisi.', 'danger')
            return redirect(url_for('tambah_kriteria'))
        try:
            bobot_str = request.form.get('bobot')
            if bobot_str is None:
                raise ValueError("Bobot tidak boleh kosong")
            bobot = float(bobot_str)
        except (ValueError, TypeError):
            flash('Bobot harus berupa angka dan tidak boleh kosong', 'danger')
            return redirect(url_for('tambah_kriteria'))
        
        kriteria = Kriteria(nama=nama, bobot=bobot, jenis=jenis)
        db.session.add(kriteria)
        db.session.commit()
        flash('kriteria baru berhasil ditambahkan', 'success')
        return redirect(url_for('index'))
    kriteria_list = kriteria.querry.all()
    return render_template('kriteria.html')

@app.route('/input_nilai/<int:pasien_id>', methods=['GET', 'POST'])
def input_nilai(pasien_id):
    pasien = Pasien.query.get_or_404(pasien_id)
    pasien_list = Pasien.query.all()
    kriteria_list = Kriteria.query.all()
    if request.method == 'POST':
        for k in kriteria_list:
            value_str = request.form.get(f'nilai_{k.id}')
            if not value_str: continue

            try:
                value = float(value_str)
            except ValueError:
                flash(f"input '{value_str}' untuk '{k.nama}' tidak valid. Diabaikan.", "Warning")
                continue
            
            # for p in pasien_list:
            #     value = float(request.form.get(f'nilai_{p.id}_{k.id}', 0))
            #     nilai = Nilai.query.filter_by(pasien_id=p.id, kriteria_id=k.id).first()
            #     if nilai:
            #         nilai.value = value
            #     else:
            #         new_nilai = Nilai(pasien_id=p.id, kriteria_id=k.id, value=value)
            #         db.session.add(new_nilai)

            if nilai_obj:
                nilai_obj.value = value
            else:
                nilai_obj = Nilai(pasien_id=pasien.id, kriteria_id=k.id, value=value)
                db.session.add(nilai_obj)

        db.session.commit()
        flash(f'Nilai untuk {pasien.nama} berhasil disimpan.', 'success')
        return redirect(url_for('index'))
    
    existing_values = {n.kriteria_id: n.value for n in pasien.nilai}
    return render_template('input_nilai.html', pasien=pasien, kriteria_list=kriteria_list, existing_values=existing_values)

@app.route('/hitung')
def hasil():
    hasil_saw = hitung_saw()
    return render_template('results.html', hasil=hasil_saw)

if __name__ == '__main__':
    app.run(debug=True)
