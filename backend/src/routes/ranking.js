const express = require('express');
const router = express.Router();
const { calculateRanking } = require('../controllers/ranking');

router.get('/', calculateRanking);

module.exports = router;
