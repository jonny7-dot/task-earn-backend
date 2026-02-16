# Task Earn Backend (Demo)

Ye ek simple backend hai jahan user chhote tasks complete karke rewards earn karta hai.

> ⚠️ **Important:** Ye project **demo/simulation** mode me hai. Real-money game banane ke liye legal compliance, KYC, anti-fraud system, taxation, state-wise gaming laws aur licensed payout integration zaroori hai.

## Features
- User register aur token-based session
- Task list API
- Task complete karke wallet me reward add
- Daily earning limit
- Wallet check
- Withdrawal request (PENDING demo mode)

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## Test
```bash
pytest -q
```

## API Endpoints
- `POST /register` -> `{ "name": "Aman" }`
- `GET /tasks`
- `POST /tasks/{task_id}/complete` -> `{ "token": "..." }`
- `POST /wallet` -> `{ "token": "..." }`
- `POST /withdraw` -> `{ "token": "...", "amount": 50, "upi_id": "aman@upi" }`

## Troubleshooting
- Agar `pip install -r requirements.txt` me network/proxy error aaye, to apne environment ka internet/proxy config check karein.
- Offline/sandbox environment me dependencies install na ho paaye to pehle connected machine par install karke phir `pytest -q` run karein.
