from models import db, Pasien, Kriteria, Nilai

def hitung_saw():
    pasien_list = Pasien.query.all()
    kriteria_list = Kriteria.query.all()

    # Normalisasi
    hasil = []
    for p in pasien_list:
        total = 0
        for k in kriteria_list:
            nilai = Nilai.query.filter_by(pasien_id=p.id, kriteria_id=k.id).first()
            if not nilai:
                continue
            if k.jenis == 'benefit':
                max_value = max([Nilai.query.filter_by(kriteria_id=k.id).all()], key=lambda x: x.value)[0].value
                norm = nilai.value / max_value
            else:  # cost
                min_value = min([Nilai.query.filter_by(kriteria_id=k.id).all()], key=lambda x: x.value)[0].value
                norm = min_value / nilai.value
            total += norm * k.bobot
        hasil.append({'nama': p.nama, 'skor': round(total, 3)})
    
    hasil.sort(key=lambda x: x['skor'], reverse=True)
    return hasil
