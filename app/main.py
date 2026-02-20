from datetime import datetime
from typing import Dict, List
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Task Earn Demo API", version="1.0.0")


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=40)


class WithdrawRequest(BaseModel):
    token: str
    amount: int = Field(gt=0)
    upi_id: str = Field(min_length=5)


class TokenRequest(BaseModel):
    token: str


class CompleteTaskRequest(BaseModel):
    token: str


TASKS: List[Dict] = [
    {"id": 1, "title": "App open karo", "reward": 5},
    {"id": 2, "title": "Daily quiz complete karo", "reward": 20},
    {"id": 3, "title": "Ad video dekho", "reward": 10},
    {"id": 4, "title": "Friend invite karo", "reward": 25},
]

USERS: Dict[str, Dict] = {}
MAX_DAILY_EARNING = 500


def _today() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def _find_task(task_id: int) -> Dict:
    task = next((t for t in TASKS if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def _get_user(token: str) -> Dict:
    user = USERS.get(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    if user["date"] != _today():
        user["date"] = _today()
        user["today_earning"] = 0
        user["completed_tasks"] = []
    return user


@app.get("/")
def home():
    return {
        "message": "Simple task karke reward earn demo API",
        "note": "Real money payout ke liye legal + KYC + payment gateway integration zaroori hai.",
    }


@app.post("/register")
def register(payload: RegisterRequest):
    token = str(uuid4())
    USERS[token] = {
        "name": payload.name,
        "wallet": 0,
        "today_earning": 0,
        "date": _today(),
        "completed_tasks": [],
        "withdrawals": [],
    }
    return {"token": token, "name": payload.name}


@app.get("/tasks")
def list_tasks():
    return {"tasks": TASKS, "max_daily_earning": MAX_DAILY_EARNING}


@app.post("/tasks/{task_id}/complete")
def complete_task(task_id: int, payload: CompleteTaskRequest):
    user = _get_user(payload.token)
    task = _find_task(task_id)

    if task_id in user["completed_tasks"]:
        raise HTTPException(status_code=400, detail="Task already completed")

    if user["today_earning"] + task["reward"] > MAX_DAILY_EARNING:
        raise HTTPException(status_code=400, detail="Daily earning limit reached")

    user["completed_tasks"].append(task_id)
    user["wallet"] += task["reward"]
    user["today_earning"] += task["reward"]

    return {
        "message": "Task complete! Reward add ho gaya.",
        "reward": task["reward"],
        "wallet": user["wallet"],
        "today_earning": user["today_earning"],
    }


@app.post("/wallet")
def wallet(payload: TokenRequest):
    user = _get_user(payload.token)
    return {
        "name": user["name"],
        "wallet": user["wallet"],
        "today_earning": user["today_earning"],
        "completed_tasks": user["completed_tasks"],
    }


@app.post("/withdraw")
def withdraw(payload: WithdrawRequest):
    user = _get_user(payload.token)

    if payload.amount > user["wallet"]:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    user["wallet"] -= payload.amount
    request_data = {
        "amount": payload.amount,
        "upi_id": payload.upi_id,
        "status": "PENDING",
        "created_at": datetime.utcnow().isoformat(),
    }
    user["withdrawals"].append(request_data)

    return {
        "message": "Withdrawal request created (demo mode)",
        "request": request_data,
        "wallet": user["wallet"],
    }
