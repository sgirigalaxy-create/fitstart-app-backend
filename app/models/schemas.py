from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class GoalEnum(str, Enum):
    MUSCLE = "muscle"
    WEIGHT_LOSS = "weight-loss"
    GENERAL = "general"
    STRENGTH = "strength"


class EquipmentEnum(str, Enum):
    FULL_GYM = "full-gym"
    BASIC = "basic"
    BODYWEIGHT = "bodyweight"


class LevelEnum(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class SexEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


class DietTypeEnum(str, Enum):
    VEGETARIAN = "vegetarian"
    NON_VEGETARIAN = "non-vegetarian"
    EGGETARIAN = "eggetarian"


class DietGoalEnum(str, Enum):
    MAINTAIN = "maintain"
    LEAN_BULK = "lean-bulk"
    CUT = "cut"


# --- Request Models ---

class GeneratePlanRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)
    age: int = Field(..., ge=14, le=80)
    sex: SexEnum
    goal: GoalEnum
    equipment: EquipmentEnum
    level: LevelEnum = LevelEnum.BEGINNER
    days: list[str] = Field(..., min_length=3, max_length=6)
    height: Optional[float] = Field(None, ge=100, le=250)
    weight: Optional[float] = Field(None, ge=30, le=250)


class SavePlanRequest(BaseModel):
    user_name: str
    goal: GoalEnum
    equipment: EquipmentEnum
    level: LevelEnum
    days: list[str]
    age: int
    sex: SexEnum
    plan: list[dict]


class DietRequest(BaseModel):
    diet_type: DietTypeEnum = DietTypeEnum.VEGETARIAN
    calories: int = Field(2200, ge=1200, le=4000)
    goal: DietGoalEnum = DietGoalEnum.MAINTAIN


# --- Response Models ---

class ExerciseResponse(BaseModel):
    name: str
    muscles: list[str]
    sets: int
    reps: str
    equipment: list[str]
    youtube_id: str
    tips: list[str]
    rest_note: Optional[str] = None
    difficulty: Optional[str] = None


class DayPlanResponse(BaseModel):
    day: str
    label: str
    exercises: list[ExerciseResponse]
    is_rest: bool


class WorkoutPlanResponse(BaseModel):
    plan: list[DayPlanResponse]
    summary: dict


class BMIRequest(BaseModel):
    height_cm: float = Field(..., ge=100, le=250)
    weight_kg: float = Field(..., ge=30, le=250)


class BMIResponse(BaseModel):
    bmi: float
    category: str
    indicator_percent: float


class MealResponse(BaseModel):
    meal: str
    menu: str
    calories: int
    protein: int
    carbs: int
    fats: int


class DietChartResponse(BaseModel):
    diet_type: str
    total_calories: int
    total_protein: int
    total_carbs: int
    total_fats: int
    protein_percent: int
    carbs_percent: int
    fats_percent: int
    meals: list[MealResponse]
    meal_notes: list[str]
