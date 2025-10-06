from models import db, Pasien, Kriteria, Nilai

def hitung_saw():
    pasien_list = Pasien.query.all()
    kriteria_list = Kriteria.query.all()
    nilai_list = Nilai.query.all()

    if not pasien_list or not kriteria_list or not nilai_list:
        return []
    
    nilai_matrix = {}
    for nilai in nilai_list:
        if nilai.pasien_id not in nilai_matrix:
            nilai_matrix[nilai.pasien_id] = {}
        nilai_matrix[nilai.pasien_id][nilai.kriteria_id] = nilai.value

    max_min_values = {}
    for kriteria in kriteria_list:
        all_values_for_kriteria = [
            nilai.value for nilai in nilai_list if nilai.kriteria_id == kriteria.id
        ]

        if not all_values_for_kriteria:
            max_min_values[kriteria.id] = {'max': 0, 'min': 0}
            continue

        if kriteria.jenis.lower() == 'benefit':
            max_min_values[kriteria.id] = {'max': max(all_values_for_kriteria)}
        else: 
            max_min_values[kriteria.id] = {'min':  min(all_values_for_kriteria)}

    # Normalisasi
    hasil = []
    for p in pasien_list:
        total_skor = 0

        nilai_pasien = nilai_matrix.get(p.id, {})
        for k in kriteria_list:
            nilai_value = nilai_pasien.get(kriteria.id, {})

            if nilai_value == 0:
                continue

            norm = 0
            if kriteria.jenis.lower() == 'benefit':
                max_value = max_min_values.get(kriteria.id, {}.get('max', 0))
                if max_value > 0:
                    norm = nilai_value / max_value
                else: #cost
                    min_value = max_min_values.get(kriteria.id, {}).get('max', 0)
                    if nilai_value > 0:
                        norm 
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
