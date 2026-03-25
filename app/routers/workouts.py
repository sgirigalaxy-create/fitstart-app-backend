from fastapi import APIRouter
from app.models.schemas import GeneratePlanRequest, WorkoutPlanResponse
from app.services.workout_generator import generate_plan, estimate_calories, estimate_duration
from app.services.exercises import EXERCISES

router = APIRouter()


@router.post("/generate", response_model=WorkoutPlanResponse)
async def generate_workout_plan(request: GeneratePlanRequest):
    """Generate a personalized workout plan based on user preferences."""
    plan = generate_plan(
        name=request.name,
        days=request.days,
        goal=request.goal.value,
        equipment=request.equipment.value,
        level=request.level.value,
    )

    # Build summary
    training_days = [d for d in plan if not d["is_rest"]]
    total_exercises = sum(len(d["exercises"]) for d in plan)
    avg_exercises = (
        round(sum(len(d["exercises"]) for d in training_days) / len(training_days))
        if training_days
        else 0
    )

    goal_labels = {
        "muscle": "Build Muscle",
        "weight-loss": "Lose Weight",
        "general": "General Fitness",
        "strength": "Get Stronger",
    }
    equip_labels = {
        "full-gym": "Full Gym",
        "basic": "Basic Equipment",
        "bodyweight": "Bodyweight",
    }
    level_labels = {
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "expert": "Expert",
    }

    summary = {
        "name": request.name,
        "days_per_week": len(request.days),
        "goal": goal_labels.get(request.goal.value, request.goal.value),
        "equipment": equip_labels.get(request.equipment.value, request.equipment.value),
        "level": level_labels.get(request.level.value, request.level.value),
        "total_exercises": total_exercises,
        "est_calories_per_session": estimate_calories(avg_exercises, request.goal.value),
        "est_duration_per_session": estimate_duration(avg_exercises, request.goal.value),
    }

    # Convert exercises to response format
    response_plan = []
    for day in plan:
        exercises = []
        for ex in day["exercises"]:
            exercises.append({
                "name": ex["name"],
                "muscles": ex["muscles"],
                "sets": ex["sets"],
                "reps": ex["reps"],
                "equipment": ex.get("equipment", []),
                "youtube_id": ex.get("youtube_id", ""),
                "tips": ex.get("tips", []),
                "rest_note": ex.get("rest_note"),
                "difficulty": ex.get("difficulty"),
            })
        response_plan.append({
            "day": day["day"],
            "label": day["label"],
            "exercises": exercises,
            "is_rest": day["is_rest"],
        })

    return WorkoutPlanResponse(plan=response_plan, summary=summary)


@router.get("/exercises")
async def get_all_exercises():
    """Get the complete exercise database."""
    return EXERCISES


@router.get("/exercises/{muscle_group}")
async def get_exercises_by_group(muscle_group: str):
    """Get exercises for a specific muscle group."""
    exercises = EXERCISES.get(muscle_group)
    if exercises is None:
        return {"error": f"Muscle group '{muscle_group}' not found", "available": list(EXERCISES.keys())}
    return exercises
