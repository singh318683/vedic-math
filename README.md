# Vedic Math — Learn & Quiz

A full-stack web app for learning and practicing all 8 core Vedic math sutras with step-by-step lessons, worked examples, and 4 quiz modes.

## Tech stack
- **Backend**: Python / Flask (Vercel serverless)
- **Frontend**: Pure HTML/CSS/JS (no frameworks)
- **Deploy**: Vercel

---

## Deploy to Vercel (3 steps)

### 1. Push to GitHub
```bash
cd vedic-math
git init
git add .
git commit -m "Initial commit — Vedic Math app"
git remote add origin https://github.com/singh318683/vedic-math.git
git push -u origin main
```

### 2. Connect to Vercel
1. Go to https://vercel.com and log in
2. Click **Add New → Project**
3. Import your `vedic-math` GitHub repo
4. Leave all settings as default (Vercel auto-detects Python)
5. Click **Deploy**

### 3. Done!
Your app will be live at `https://vedic-math-<hash>.vercel.app`

---

## Local development

```bash
pip install flask
cd vedic-math
python api/index.py
# Open http://localhost:5000
```

---

## Project structure

```
vedic-math/
├── api/
│   └── index.py        # Flask backend (all 8 sutras + quiz API)
├── public/
│   └── index.html      # Full frontend (learn + quiz + progress)
├── requirements.txt    # Flask dependency
├── vercel.json         # Vercel routing config
└── README.md
```

## API endpoints

| Endpoint | Description |
|---|---|
| `GET /api/sutras` | All sutras (no questions) |
| `GET /api/sutras/:id` | Single sutra with steps, examples, questions |
| `GET /api/quiz/:id` | 5 random questions for a sutra |
| `GET /api/quiz/mixed` | 10 random questions from all sutras |

## Features
- 8 Vedic sutras with full Sanskrit + meaning
- Step-by-step method for each sutra
- Worked examples with highlighted answers
- 4 quiz modes: current sutra / mixed / speed (10s) / challenge (8s, no hints)
- XP + level progression system
- Accuracy and streak tracking
- Fully mobile responsive
