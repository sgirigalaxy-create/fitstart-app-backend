# FitStart Backend API

FastAPI backend for the FitStart Gym Workout Planner application.

## Tech Stack

- **Python 3.11+** with **FastAPI** and **Uvicorn**
- **Firebase Admin SDK** for authentication verification and Firestore
- **Pydantic** for data validation

## Project Structure

```
fitstart-app-backend/
├── app/
│   ├── core/
│   │   ├── config.py          # Environment configuration
│   │   ├── dependencies.py    # Auth dependency injection
│   │   └── firebase.py        # Firebase Admin SDK setup
│   ├── models/
│   │   └── schemas.py         # Pydantic request/response models
│   ├── routers/
│   │   ├── diet.py            # Diet chart & BMI endpoints
│   │   ├── health.py          # Health check endpoint
│   │   ├── plans.py           # CRUD for saved plans (authenticated)
│   │   └── workouts.py        # Workout generation & exercise database
│   ├── services/
│   │   ├── diet.py            # Diet calculation logic
│   │   ├── exercises.py       # Complete exercise database (60+ exercises)
│   │   └── workout_generator.py  # Plan generation engine
│   └── main.py                # FastAPI app entry point
├── .env.example
├── requirements.txt
└── run.py                     # Uvicorn runner
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/api/workouts/generate` | Generate a workout plan |
| GET | `/api/workouts/exercises` | Get all exercises |
| GET | `/api/workouts/exercises/{group}` | Get exercises by muscle group |
| POST | `/api/diet/chart` | Calculate diet chart |
| POST | `/api/diet/bmi` | Calculate BMI |
| GET | `/api/diet/types` | Get available diet types |
| POST | `/api/plans/save` | Save a plan (auth required) |
| GET | `/api/plans/` | Get saved plans (auth required) |
| GET | `/api/plans/{id}` | Get a specific plan (auth required) |
| DELETE | `/api/plans/{id}` | Delete a plan (auth required) |

## Bodybuilding Levels

The workout generator supports three experience levels:

- **Beginner** (0-6 months): Fewer sets, higher rest, simpler exercises
- **Intermediate** (6-24 months): Standard sets/reps, full exercise pool
- **Expert** (2+ years): More sets, shorter rest, advanced exercises included

## Setup

1. Copy `.env.example` to `.env` and fill in your Firebase credentials
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python run.py
   ```
   The API will be available at `http://localhost:8000`

4. View API docs at `http://localhost:8000/docs`
