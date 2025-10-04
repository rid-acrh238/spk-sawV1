const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const rankingRoute = require('./src/routes/ranking');

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.use('/ranking', rankingRoute);

app.listen(3001, () => console.log('Server running on http://localhost:3001'));
