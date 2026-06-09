# AtlasIQ - Business Expansion Operating System
<img width="832" height="400" alt="Screenshot 2026-06-09 at 22 34 09" src="https://github.com/user-attachments/assets/61046986-a926-4956-9559-2b504a40f750" />


AtlasIQ is a cutting-edge **Multi-Agent Business Expansion Operating System** designed to help entrepreneurs, franchises, and corporations make data-driven decisions when opening new locations. By leveraging an AI swarm, geospatial data, and financial modeling, AtlasIQ runs comprehensive "What-If" scenarios to project revenue, assess risk, and generate actionable strategic recommendations.

## 🌟 Key Features

* **🤖 Multi-Agent AI Swarm:** Powered by LangGraph and GPT-4o-mini, a specialized team of agents (Market, Competitor, Revenue, Risk, and Strategy) works asynchronously to analyze your expansion queries.
* **📍 Location Intelligence:** Real-time geocoding and competitor fetching using OpenStreetMap (Nominatim & Overpass APIs) to understand local market density.
* **📈 Financial Forecasting:** Deterministic revenue projections, ROI calculations, and risk modeling based on industry benchmarks.
* **🔐 Secure Authentication:** JWT-based authentication with a secure OTP verification flow and bcrypt password hashing.
* **⚡ Modern Tech Stack:** 
  * **Frontend:** Next.js (React), Tailwind CSS, Lucide Icons, Modern UI Components.
  * **Backend:** Python, FastAPI, SQLAlchemy (SQLite), Alembic, LangChain, Qdrant (Vector DB for RAG).

---

## 🏗 Architecture & Stack

### Frontend (`atlasiq-frontend`)
* Framework: **Next.js 14** (App Router)
* Styling: **Tailwind CSS**
* Language: **TypeScript**
* Deployment: Designed for Vercel or Node environments.

### Backend (`atlasiq-backend`)
* Framework: **FastAPI**
* AI/LLM: **LangChain**, **LangGraph**, **OpenRouter API**
* Database: **SQLite** with **SQLAlchemy** ORM & **Alembic** migrations
* External APIs: **OpenStreetMap**, **Overpass API**

---

## 🚀 Getting Started (Local Development)

### Prerequisites
* Node.js (v18+)
* Python 3.10+
* An OpenRouter API Key (for LLM capabilities)

### 1. Setup the Backend

```bash
cd atlasiq-backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Setup Environment Variables
cp .env.example .env
# Open .env and add your OPENROUTER_API_KEY and other configuration

# Run Database Migrations
alembic upgrade head

# Start the FastAPI Server
uvicorn src.main:app --reload
```
*The backend will now be running at `http://127.0.0.1:8000`*

### 2. Setup the Frontend

```bash
cd atlasiq-frontend

# Install dependencies
npm install

# Start the Development Server
npm run dev
```
*The frontend will now be running at `http://localhost:3000`*

---

## 🧪 Testing Credentials

When running locally in development mode, the system is configured to allow rapid testing without needing a real email server:

* **Test Email:** `hello@gmail.com`
* **Test OTP:** `123456`
*(Using this specific email bypasses the 60-second OTP cooldown).*

---

## 🗄 Database Migrations

If you make changes to the SQLAlchemy models in `src/infrastructure/database/models.py`, you must generate and apply an Alembic migration:

```bash
cd atlasiq-backend
source venv/bin/activate

# Auto-generate migration script
alembic revision --autogenerate -m "Describe your changes"

# Apply migration to the database
alembic upgrade head
```

---

## 📜 License

This project is proprietary and confidential. All rights reserved.
