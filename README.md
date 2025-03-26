# MailFilter Assistant

<p align="center">
  <img src="public/mail_filter_automated.PNG" width="45%" />
  <img src="public/mail_chatbot.PNG" width="45%" />
</p>

<p align="center">
  <em>Screenshot: Email classification and chatbot assistant</em>
</p>

MailFilter is a web-based AI-powered assistant that analyzes your email inbox to extract and model your relationships. It uses the Gmail API and OpenAI to identify which people you interact with the most and what kind of relationship you have with them. You can then use a chatbot interface to ask questions like "Who among my contacts is best suited to manage my finances?" and get an AI-powered recommendation.

---

## 🚀 Features

- Extract personal emails from Gmail using OAuth.
- Identify human contacts vs. automated messages.
- Analyze frequency, trust, emotional proximity, and expertise using OpenAI.
- Store a structured relationship model in JSON.
- Chatbot interface to interact with your personal network via natural language.
- Clean UI with progress tracking and suggestion prompts.

---

## 📁 Project Structure

```
.
├── datas/
│   ├── emails.json               # Extracted emails
│   ├── relations.json            # Filtered human contacts
│   └── relations_modelization.json  # Final structured relationship data
│
├── scripts/
│   ├── get_emails.py             # Connects to Gmail and fetches emails
│   ├── identify_relations.py     # Filters real human senders using OpenAI
│   ├── create_relations.py       # Builds final JSON model of relations
│   └── server.py       # Flask backend to trigger Python scripts
│
├── views/
│   ├── index.ejs                 # Homepage with analysis trigger
│   └── chatbot.ejs               # Chatbot interface
│
├── server.js                     # Express.js server (frontend)
├── .env                          # Environment variables (API keys)
```

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/DeepLeau/email_analysis
cd email_analysis
```

### 2. Install dependencies

#### Frontend (Node.js + Express)

```bash
npm install
```

#### Backend (Python + Flask)

```bash
pip install flask flask-cors openai oauth2client google-api-python-client python-dotenv beautifulsoup4 lxml
```

### 3. Set up environment variables

Create a `.env` file in the root directory with the following:

```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_API_KEY=your-google-api-key
OPENAI_API_KEY=your-openai-key
MY_EMAIL=your-email@example.com
```

Also place your `credentials.json` (from Google Cloud Console) in the root.

---

## 🧪 Running the Project

### 1. Start the frontend (on port 3000)

```bash
node server.js
```

### 2. Start the backend Flask API (on port 5000)

```bash
python server.py
```

### 3. Visit the app

Open `http://localhost:3000` in your browser.

---

## ⚙️ Workflow

1. **Start Analysis** (on `/`) triggers:
   - `get_emails.py` → Fetch emails
   - `identify_relations.py` → Filter senders via OpenAI
   - `create_relations.py` → Generate structured relations JSON

2. **Use Chatbot** (on `/chatbot`) to ask questions like:
   - “Who can help me with AI?”
   - “Who could be my technical co-founder?”

---

## 📌 Notes

- You must authenticate with Google the first time.
- Emails and data are not stored in the cloud — everything runs locally.
- CORS is enabled in `server.py` to allow interaction between ports.

---

## 🤖 Powered by

- OpenAI GPT-3.5 Turbo
- Gmail API
- Flask + Express.js

---

## 📬 License

MIT – do whatever you want, but be cool 😎