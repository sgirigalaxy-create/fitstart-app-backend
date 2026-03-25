from fastapi import APIRouter
from app.models.schemas import DietRequest, DietChartResponse, BMIRequest, BMIResponse
from app.services.diet import calculate_diet, calculate_bmi, DIET_CHARTS

router = APIRouter()


@router.post("/chart", response_model=DietChartResponse)
async def get_diet_chart(request: DietRequest):
    """Calculate a diet chart based on diet type, calorie target, and goal."""
    result = calculate_diet(
        diet_type=request.diet_type.value,
        calories=request.calories,
        goal=request.goal.value,
    )
    return DietChartResponse(**result)


@router.get("/types")
async def get_diet_types():
    """Get available diet types with their base nutritional data."""
    types = []
    for key, chart in DIET_CHARTS.items():
        types.append({
            "type": key,
            "base_total": chart["base_total"],
            "base_protein": chart["base_protein"],
            "meal_count": len(chart["meals"]),
        })
    return types


@router.post("/bmi", response_model=BMIResponse)
async def calculate_bmi_endpoint(request: BMIRequest):
    """Calculate BMI from height and weight."""
    result = calculate_bmi(request.height_cm, request.weight_kg)
    return BMIResponse(**result)
