const db = require('../db');

async function calculateRanking(req, res) {
  try {
    // 1. Ambil semua kriteria & bobot
    const [criteria] = await db.query('SELECT * FROM criteria');
    // 2. Ambil semua pasien & nilai
    const [patients] = await db.query('SELECT * FROM patients');
    const [values] = await db.query('SELECT * FROM values');

    // 3. Normalisasi & hitung skor (SAW)
    let result = patients.map(patient => {
      let score = 0;
      criteria.forEach(c => {
        const val = values.find(v => v.patient_id === patient.id && v.criteria_id === c.id)?.value || 0;
        if (c.type === 'benefit') {
          const maxVal = Math.max(...values.filter(v => v.criteria_id === c.id).map(v => v.value));
          score += (val / maxVal) * c.weight;
        } else { // cost
          const minVal = Math.min(...values.filter(v => v.criteria_id === c.id).map(v => v.value));
          score += (minVal / val) * c.weight;
        }
      });
      return { ...patient, score };
    });

    // 4. Urutkan descending
    result.sort((a, b) => b.score - a.score);

    res.json(result);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  }
}

module.exports = { calculateRanking };
