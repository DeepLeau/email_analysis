const express = require('express');
const path = require('path');
const axios = require('axios');
require('dotenv').config(); 

const app = express();
const port = 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

app.get('/', (req, res) => {
  res.render('index', { 
    googleClientId: process.env.GOOGLE_CLIENT_ID,
    googleApiKey: process.env.GOOGLE_API_KEY,
    openApiToken: process.env.OPENAI_API_KEY
  });
});

app.get('/chatbot', (req, res) => {
  res.render('chatbot', { 
    openApiToken: process.env.OPENAI_API_KEY
  });
});

app.post('/auth/google/callback', async (req, res) => {
  try {
    const { code } = req.body;
    
    const tokenResponse = await axios.post('https://oauth2.googleapis.com/token', {
      code,
      client_id: process.env.GOOGLE_CLIENT_ID,
      client_secret: process.env.GOOGLE_CLIENT_SECRET,
      redirect_uri: 'http://localhost:3000',
      grant_type: 'authorization_code'
    });

    res.json(tokenResponse.data);
  } catch (error) {
    console.error('Erreur lors de l\'échange du code:', error.response?.data || error.message);
    res.status(500).json({ error: 'Erreur lors de l\'authentification' });
  }
});

app.listen(port, () => {
  console.log(`Serveur démarré sur http://localhost:${port}`);
});