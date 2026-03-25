"""Diet chart data and calorie calculation service."""

import math

DIET_GOAL_MULTIPLIER = {
    "lean-bulk": 1.1,
    "maintain": 1.0,
    "cut": 0.9,
}

DIET_CHARTS: dict[str, dict] = {
    "vegetarian": {
        "base_total": 2200,
        "base_protein": 110,
        "meals": [
            {
                "meal": "Breakfast",
                "menu": "Oatmeal with berries & almonds",
                "base_cal": 520,
                "base_protein": 20,
                "base_carbs": 68,
                "base_fats": 18,
            },
            {
                "meal": "Lunch",
                "menu": "Chickpea salad with quinoa & greens",
                "base_cal": 610,
                "base_protein": 24,
                "base_carbs": 72,
                "base_fats": 20,
            },
            {
                "meal": "Snack",
                "menu": "Greek yogurt + walnuts + apple",
                "base_cal": 330,
                "base_protein": 18,
                "base_carbs": 32,
                "base_fats": 14,
            },
            {
                "meal": "Dinner",
                "menu": "Lentil soup + roasted veggies + brown rice",
                "base_cal": 740,
                "base_protein": 48,
                "base_carbs": 90,
                "base_fats": 22,
            },
        ],
        "meal_notes": [
            "Cook quinoa and lentils in larger batches for 3-4 days.",
            "Portion salads and dressings separately to keep freshness.",
            "Season plant proteins with turmeric, paprika, and garlic for flavor.",
            "Use Greek yogurt as a high-protein dip for snacks.",
        ],
    },
    "non-vegetarian": {
        "base_total": 2400,
        "base_protein": 135,
        "meals": [
            {
                "meal": "Breakfast",
                "menu": "Scrambled eggs, spinach & whole-grain toast",
                "base_cal": 560,
                "base_protein": 36,
                "base_carbs": 48,
                "base_fats": 24,
            },
            {
                "meal": "Lunch",
                "menu": "Grilled chicken, quinoa salad, mixed veggies",
                "base_cal": 680,
                "base_protein": 44,
                "base_carbs": 70,
                "base_fats": 22,
            },
            {
                "meal": "Snack",
                "menu": "Cottage cheese + carrots + seeds",
                "base_cal": 350,
                "base_protein": 24,
                "base_carbs": 24,
                "base_fats": 16,
            },
            {
                "meal": "Dinner",
                "menu": "Fish curry with brown rice and steamed broccoli",
                "base_cal": 810,
                "base_protein": 31,
                "base_carbs": 84,
                "base_fats": 28,
            },
        ],
        "meal_notes": [
            "Marinate chicken and fish the night before for flavor.",
            "Batch-cook sauces and use steamed vegetables for quick meals.",
            "Use portion containers to separate carbs and proteins.",
            "Keep cooked grains and meats chilled and reheat in microwave safely.",
        ],
    },
    "eggetarian": {
        "base_total": 2300,
        "base_protein": 128,
        "meals": [
            {
                "meal": "Breakfast",
                "menu": "Vegetable omelet with avocado slices",
                "base_cal": 520,
                "base_protein": 32,
                "base_carbs": 34,
                "base_fats": 26,
            },
            {
                "meal": "Lunch",
                "menu": "Egg salad whole grain wrap + mixed greens",
                "base_cal": 620,
                "base_protein": 38,
                "base_carbs": 58,
                "base_fats": 20,
            },
            {
                "meal": "Snack",
                "menu": "Cottage cheese + berries + nuts",
                "base_cal": 340,
                "base_protein": 26,
                "base_carbs": 30,
                "base_fats": 16,
            },
            {
                "meal": "Dinner",
                "menu": "Baked tofu stir-fry + brown rice + veggies",
                "base_cal": 820,
                "base_protein": 32,
                "base_carbs": 88,
                "base_fats": 24,
            },
        ],
        "meal_notes": [
            "Cook egg dishes in bulk and store in airtight containers.",
            "Keep sliced veggies crisp by storing with a tiny paper towel.",
            "Make a simple homemade dressing with olive oil, lemon and mustard.",
            "Use any leftover hard-boiled eggs as quick salad or breakfast add-on.",
        ],
    },
}


def calculate_diet(
    diet_type: str = "vegetarian",
    calories: int = 2200,
    goal: str = "maintain",
) -> dict:
    """Calculate a diet chart with adjusted macros based on calorie target and goal."""
    chart = DIET_CHARTS.get(diet_type, DIET_CHARTS["vegetarian"])
    goal_ratio = DIET_GOAL_MULTIPLIER.get(goal, 1.0)
    effective_calories = round(calories * goal_ratio)

    base_total = chart["base_total"]
    ratio = effective_calories / base_total

    total_protein = 0
    total_carbs = 0
    total_fats = 0
    meals = []

    for m in chart["meals"]:
        r_cal = round(m["base_cal"] * ratio)
        r_protein = round(m["base_protein"] * ratio)
        r_carbs = round(m["base_carbs"] * ratio)
        r_fats = round(m["base_fats"] * ratio)

        total_protein += r_protein
        total_carbs += r_carbs
        total_fats += r_fats

        meals.append({
            "meal": m["meal"],
            "menu": m["menu"],
            "calories": r_cal,
            "protein": r_protein,
            "carbs": r_carbs,
            "fats": r_fats,
        })

    total_macro = total_protein + total_carbs + total_fats
    if total_macro > 0:
        protein_pct = round((total_protein / total_macro) * 100)
        carbs_pct = round((total_carbs / total_macro) * 100)
        fats_pct = round((total_fats / total_macro) * 100)
    else:
        protein_pct = carbs_pct = fats_pct = 0

    return {
        "diet_type": diet_type,
        "total_calories": effective_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fats": total_fats,
        "protein_percent": protein_pct,
        "carbs_percent": carbs_pct,
        "fats_percent": fats_pct,
        "meals": meals,
        "meal_notes": chart["meal_notes"],
    }


def calculate_bmi(height_cm: float, weight_kg: float) -> dict:
    """Calculate BMI from height (cm) and weight (kg)."""
    bmi = weight_kg / (height_cm / 100) ** 2
    bmi_rounded = round(bmi, 1)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal Weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    indicator_pct = max(0, min(100, ((bmi - 15) / 25) * 100))

    return {
        "bmi": bmi_rounded,
        "category": category,
        "indicator_percent": round(indicator_pct, 1),
    }
