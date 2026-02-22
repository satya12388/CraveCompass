# CraveCompass: Your Intelligent Menu Guide 🧭

CraveCompass is an AI-powered culinary companion that transforms static restaurant menus into deep, intelligent insights. By simply uploading a photo of a menu, users receive tailored dish recommendations, authentic ingredient breakdowns, chef preparation details, and matching imagery.

This project uses a decoupled monorepo architecture with a sleek **Vanilla JS Frontend** providing a rich user experience and a robust **FastAPI Backend**, leveraging state-of-the-art Large Vision Models (LVMs) and LangChain tool-calling agents to source live intelligence from the internet.

---

## Architecture Overview 🏗️

The codebase is organized into a single monorepo for ease of development:

- **`Frontend/`**: A lightweight HTML, CSS, and vanilla JS web application. Features a dark-mode visual interface with beautiful micro-animations, custom tag generation, and bottom-sheet modals for deep dish insights without page reloads.
- **`Backend/`**: A Python FastAPI server. It houses:
  - **Vision Extraction Node**: Analyzes raw menu images via Groq Llama 3 Vision to identify discrete menu items and map them to standard categories (Veg/Non-Veg).
  - **LangChain Details Agent**: A secondary LLM agent equipped with the Tavily Search API. It executes dynamic web queries to scrape nutritional facts, authentic ingredients, preparation tips, and high-quality image URLs for any specific dish.
- **`requirements.txt`**: Located in the root menu folder, this file contains all the necessary dependencies for spinning up the Python backend infrastructure.

---

## Local Development Setup 💻

### 1. Prerequisites

- Python 3.10+
- Node.js (optional, for running a local live-server)
- **API Keys Required**:
  - `GROQ_API_KEY` (For the core LLM and LVM processing)
  - `TAVILY_API_KEY` (For the LangChain live-search agent)

### 2. Backend Setup

1. Open a terminal in the root project folder.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```
3. Install the dependencies found in the root directory:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file inside the `Backend/` directory and add your keys:
   ```env
   GROQ_API_KEY=your_groq_key_here
   TAVILY_API_KEY=your_tavily_key_here
   ```
5. Start the FastAPI server (it runs on port 8000 by default):
   ```bash
   cd Backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### 3. Frontend Setup

1. The frontend relies purely on static browser rendering. You can open `Frontend/index.html` directly in your browser.
2. For the best experience without CORS issues during development, use a local server like VS Code's "Live Server" extension, or run:
   ```bash
   cd Frontend
   python -m http.server 3000
   ```
3. Ensure the `API_URL` variable at the top of `Frontend/app.js` points to your running backend:
   ```javascript
   const API_URL = "http://127.0.0.1:8000/analyze";
   ```

---

## Deployment Guide 🚀 (Free Platforms)

Because this is a decoupled monorepo, you can host the Frontend and Backend on separate dedicated cloud platforms for maximum performance.

### Step 1: Push to GitHub

Ensure this entire root folder (including both `Frontend/` and `Backend/` and `requirements.txt`) is pushed to a Github Repository.

### Step 2: Deploy Backend (Any Cloud Provider)

1. Log into your preferred cloud hosting platform that supports Python (e.g., Render, Railway, Heroku).
2. Connect your GitHub repository.
3. Configure the **Build/Start Commands**:
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `cd Backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add your `GROQ_API_KEY` and `TAVILY_API_KEY` as secure Environment Variables in your hosting dashboard.
5. Deploy! The provider will give you a live URL for your application.

### Step 3: Wire the Frontend

1. Open `Frontend/app.js` locally.
2. Change the `API_URL` to point to the new remote URL you just generated:
   ```javascript
   const API_URL = "https://your-new-api-url.com/analyze";
   ```
3. In the `fetchItemDetails` function further down, change the fetch URL to point to `https://your-new-api-url.com/item-details?item_name=...`
4. Commit and push these changes to GitHub.

### Step 4: Deploy Frontend (Any Static Host)

1. Log into your preferred static site hosting platform (e.g., Vercel, Netlify, GitHub Pages).
2. Import your GitHub repository.
3. Open the platform's **"Root Directory"** settings, and explicitly select the `Frontend` folder.
4. Deploy! The platform will give you a live URL where your UI is hosted.

### Step 5: Final Security Handshake

1. To ensure your backend strictly accepts requests from your live frontend, open `Backend/app/main.py`.
2. Find the `CORSMiddleware` configuration block.
3. Add your exact frontend URL to the `allow_origins=` list.
4. Commit and push. Your backend server will reboot, and your full-stack AI app is now securely live!
