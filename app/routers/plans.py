from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_current_user
from app.core.firebase import get_db
from app.models.schemas import SavePlanRequest
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

router = APIRouter()

GOAL_LABELS = {
    "muscle": "Build Muscle",
    "weight-loss": "Lose Weight",
    "general": "General Fitness",
    "strength": "Get Stronger",
}


@router.post("/save")
async def save_plan(request: SavePlanRequest, user: dict = Depends(get_current_user)):
    """Save a workout plan to Firestore for the authenticated user."""
    uid = user["uid"]
    db = get_db()

    plan_doc = {
        "userName": request.user_name,
        "goal": request.goal.value,
        "goalLabel": GOAL_LABELS.get(request.goal.value, request.goal.value),
        "equipment": request.equipment.value,
        "level": request.level.value,
        "days": request.days,
        "age": request.age,
        "sex": request.sex.value,
        "plan": request.plan,
        "createdAt": SERVER_TIMESTAMP,
        "updatedAt": SERVER_TIMESTAMP,
    }

    doc_ref = db.collection("users").document(uid).collection("plans").add(plan_doc)
    return {"id": doc_ref[1].id, "message": "Plan saved successfully"}


@router.get("/")
async def get_saved_plans(user: dict = Depends(get_current_user)):
    """Get all saved plans for the authenticated user."""
    uid = user["uid"]
    db = get_db()

    plans_ref = (
        db.collection("users")
        .document(uid)
        .collection("plans")
        .order_by("createdAt", direction="DESCENDING")
        .limit(20)
    )

    plans = []
    for doc in plans_ref.stream():
        data = doc.to_dict()
        data["id"] = doc.id
        # Convert timestamps to ISO strings
        if data.get("createdAt"):
            data["createdAt"] = data["createdAt"].isoformat()
        if data.get("updatedAt"):
            data["updatedAt"] = data["updatedAt"].isoformat()
        plans.append(data)

    return plans


@router.get("/{plan_id}")
async def get_plan(plan_id: str, user: dict = Depends(get_current_user)):
    """Get a specific saved plan by ID."""
    uid = user["uid"]
    db = get_db()

    doc = db.collection("users").document(uid).collection("plans").document(plan_id).get()

    if not doc.exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

    data = doc.to_dict()
    data["id"] = doc.id
    if data.get("createdAt"):
        data["createdAt"] = data["createdAt"].isoformat()
    if data.get("updatedAt"):
        data["updatedAt"] = data["updatedAt"].isoformat()

    return data


@router.delete("/{plan_id}")
async def delete_plan(plan_id: str, user: dict = Depends(get_current_user)):
    """Delete a saved plan."""
    uid = user["uid"]
    db = get_db()

    doc_ref = db.collection("users").document(uid).collection("plans").document(plan_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

    doc_ref.delete()
    return {"message": "Plan deleted successfully"}
