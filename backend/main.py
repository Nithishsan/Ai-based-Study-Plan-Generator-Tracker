from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from planner import generate_plan
from database import init_db, insert_tasks, get_tasks, update_task, get_progress

# --------------------------------------------------
# App Initialization
# --------------------------------------------------

app = FastAPI(title="AI Study Planner API")

# Initialize SQLite DB on startup
init_db()


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class GeneratePlanRequest(BaseModel):
    goal: str
    total_days: int
    daily_minutes: int
    start_date: str

class UpdateTaskRequest(BaseModel):
    task_id: int
    is_completed: int


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/")
def root():
    return {"status": "Backend running"}


# --------------------------------------------------
# Generate Study Plan
# --------------------------------------------------

@app.post("/generate_plan")
def create_plan(req: GeneratePlanRequest):
    try:
        print("GOAL RECEIVED:", req.goal)

        if not req.goal.strip():
            raise Exception("Learning goal is empty")

        plan = generate_plan(
            goal=req.goal,
            total_days=req.total_days,
            daily_minutes=req.daily_minutes,
            start_date=req.start_date
        )

        print("PLAN GENERATED:", plan)

        if not plan:
            raise Exception("Planner returned empty plan")

        insert_tasks(plan)

        return {"status": "plan_created"}

    except Exception as e:
        # Print full error in backend terminal
        print("BACKEND EXCEPTION:", repr(e))

        # Send readable error to Streamlit
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------------------------------
# Fetch Tasks
# --------------------------------------------------

@app.get("/tasks")
def fetch_tasks():
    try:
        return get_tasks()
    except Exception as e:
        print("TASK FETCH ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------------------------------
# Update Task Completion
# --------------------------------------------------

@app.post("/update_task")
def update(req: UpdateTaskRequest):
    try:
        update_task(req.task_id, req.is_completed)
        return {"status": "updated"}
    except Exception as e:
        print("UPDATE ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------------------------------
# Progress Endpoint
# --------------------------------------------------

@app.get("/progress")
def progress():
    try:
        return get_progress()
    except Exception as e:
        print("PROGRESS ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))
