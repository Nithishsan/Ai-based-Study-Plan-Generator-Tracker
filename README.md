#🧠 Ai-based-Study-Plan-Generator-Tracker


An AI-powered study planning and progress tracking application that helps learners convert goals into structured daily tasks and monitor their progress.
This project focuses on planning + execution, not testing knowledge.
Users define their learning goal and available time, and the system generates a personalized study plan, tracks daily progress, and shows how close they are to completing their goal.
The application is built using FastAPI (backend), Streamlit (frontend), SQLite (database), and Gemini API (AI generation).


## 🚀 Features

- AI-based study task generation using Gemini API  
- Goal-based planning  
- Daily task breakdown  
- Mark tasks as completed  
- Progress tracking (completed vs total tasks)  
- Persistent storage using SQLite  
- Simple and clean Streamlit UI  
- REST API backend with FastAPI  

---

## 🏗 Tech Stack

### Backend
- Python  
- FastAPI  
- SQLite  
- Google Gemini API  
- python-dotenv  

### Frontend
- Streamlit  

### Version Control
- Git + Git LFS  

---

## 📂 Project Structure

<img width="555" height="482" alt="Screenshot 2026-02-04 143732" src="https://github.com/user-attachments/assets/567eb09b-c229-4052-a300-e1ea770669a1" />

---

## ▶️ How to Run Locally

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ai-study-planner.git
cd ai-study-planner

---

### 2. Backend Setup

Create virtual environment and activate:

python -m venv .venv
.venv\Scripts\activate

Install dependencies:

cd backend
pip install -r requirements.txt

Create .env inside backend/:

GEMINI_API_KEY=your_api_key_here


Run backend:

uvicorn main:app --reload


Backend runs at:

http://localhost:8000

3. Frontend Setup

Open new terminal:

cd frontend
streamlit run app.py
Streamlit UI opens in browser.

## 🧠 How the System Works (Explanation)

1. The user enters:
   - Learning goal  
   - Total number of days  
   - Daily study time  

2. The Streamlit frontend sends this information to the FastAPI backend.

3. FastAPI calls the Gemini API to generate learning guidance based on the user’s goal.

4. The backend converts this guidance into structured daily study tasks.

5. All tasks are stored in a SQLite database for persistence.

6. Streamlit displays:
   - Today’s tasks  
   - Task completion status  
   - Overall learning progress  

7. The user marks tasks as completed, and progress is updated automatically in real time.

To ensure reliability, the backend includes fallback logic.  
Even if the AI service fails or is unavailable, the application continues to work by generating deterministic tasks, so users can always track their learning journey.


