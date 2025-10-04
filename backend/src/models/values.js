const db = require('../db');

async function getAllPatients() {
  const [rows] = await db.query('SELECT * FROM nilai');
  return rows;
}

async function addPatient(name, age) {
  const [result] = await db.query('INSERT INTO nilai (name, age) VALUES (?, ?)', [name, age]);
  return result;
}

module.exports = { getAllPatients, addPatient };
