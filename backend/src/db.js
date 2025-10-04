const mysql = require('mysql2');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: '', // ganti sesuai db kamu
  database: 'spk_saw'
});

module.exports = pool.promise();
