from pydantic import BaseModel

class GeneratePlanRequest(BaseModel):
    goal: str
    total_days: int
    daily_minutes: int
    start_date: str

class UpdateTaskRequest(BaseModel):
    task_id: int
    is_completed: int
