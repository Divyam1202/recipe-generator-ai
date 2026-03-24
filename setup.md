🚀 Local Development Setup
To run this project locally, you must run both the Python FastAPI backend and the React Vite frontend concurrently in separate terminals.

1. Environment Variables
Create .env files in both the frontend and backend directories.

Backend (backend/.env)

Code snippet
PORT=8000
MODEL_PATH=./models/finalmodel
UNSPLASH_ACCESS_KEY=your_unsplash_api_key
Frontend (frontend/.env)

Code snippet
VITE_API_BASE_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
2. Backend Initialization (FastAPI)
Bash
cd backend
python -m venv venv

# Activate Virtual Env
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
API Endpoint: http://127.0.0.1:8000

3. Frontend Initialization (React + Vite)
Bash
cd frontend
npm install
npm run dev
UI Endpoint: http://localhost:5173

🔗 API Contract
The frontend expects the backend to adhere to this strictly:

POST /generate

Request: { "ingredients": "string" }

Response: { "recipe": "Markdown String", "responseTime": "float" }

🛠️ Tech Stack
Frontend: React 18, Vite, Custom CSS.

Backend: Python 3.x, FastAPI, Pydantic.

External APIs: Unsplash Image API.

📝 License
MIT License. Created by Divyam Chandak.


***

### ⚠️ Critical Warning: Your `.gitignore`
Before you push this to GitHub, ensure you have a `.gitignore` file at the root. If you don't, you will leak your **Unsplash API Key** and your repo will be bloated with thousands of `node_modules`. 

**Does your repository already have a `.gitignore` that includes `.env`, `node_modules/`, and `venv/`?** If not, I can provide that next so you don't ruin your GitHub history.
