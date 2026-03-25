from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.firebase import init_firebase
from app.routers import workouts, plans, diet, health

app = FastAPI(
    title="FitStart API",
    description="Backend API for the FitStart Gym Workout Planner",
    version="1.0.0",
)

allowed_origins = [
    settings.FRONTEND_URL,
    "http://localhost:3000",
    "https://fitstart-workout-planner.netlify.app",
]
# Remove empty strings and duplicates
allowed_origins = list(set(o for o in allowed_origins if o))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    try:
        init_firebase()
    except Exception as e:
        print(f"Firebase init warning (will work without admin features): {e}")


app.include_router(health.router, tags=["Health"])
app.include_router(workouts.router, prefix="/api/workouts", tags=["Workouts"])
app.include_router(plans.router, prefix="/api/plans", tags=["Plans"])
app.include_router(diet.router, prefix="/api/diet", tags=["Diet"])
