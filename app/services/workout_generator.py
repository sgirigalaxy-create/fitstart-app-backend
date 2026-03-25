"""Workout plan generation engine supporting Beginner, Intermediate, and Expert levels."""

import random
import re
from app.services.exercises import EXERCISES


SPLIT_TEMPLATES: dict[int, list[dict]] = {
    3: [
        {"label": "Upper Body", "groups": ["chest", "back", "shoulders", "arms"]},
        {"label": "Lower Body & Core", "groups": ["legs", "core"]},
        {"label": "Full Body", "groups": ["chest", "back", "legs", "core"]},
    ],
    4: [
        {"label": "Chest & Triceps", "groups": ["chest", "arms"]},
        {"label": "Back & Biceps", "groups": ["back", "arms"]},
        {"label": "Legs", "groups": ["legs", "core"]},
        {"label": "Shoulders & Core", "groups": ["shoulders", "core"]},
    ],
    5: [
        {"label": "Chest", "groups": ["chest", "core"]},
        {"label": "Back", "groups": ["back"]},
        {"label": "Legs", "groups": ["legs"]},
        {"label": "Shoulders & Arms", "groups": ["shoulders", "arms"]},
        {"label": "Full Body / Weak Points", "groups": ["chest", "back", "legs", "core"]},
    ],
    6: [
        {"label": "Push (Chest/Shoulders/Tri)", "groups": ["chest", "shoulders", "arms"]},
        {"label": "Pull (Back/Biceps)", "groups": ["back", "arms"]},
        {"label": "Legs", "groups": ["legs", "core"]},
        {"label": "Push (Chest/Shoulders/Tri)", "groups": ["chest", "shoulders", "arms"]},
        {"label": "Pull (Back/Biceps)", "groups": ["back", "arms"]},
        {"label": "Legs & Core", "groups": ["legs", "core"]},
    ],
}

ALL_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _get_split_template(num_days: int) -> list[dict]:
    clamped = min(max(num_days, 3), 6)
    return SPLIT_TEMPLATES.get(clamped, SPLIT_TEMPLATES[3])


def _pick_exercises(
    group: str,
    equipment: str,
    count: int,
    goal: str,
    level: str,
) -> list[dict]:
    pool = EXERCISES.get(group, [])
    available = [ex for ex in pool if equipment in ex.get("equipment", [])]

    # Filter by difficulty level
    if level == "beginner":
        beginner_pool = [
            ex for ex in available
            if not ex.get("difficulty") or ex.get("difficulty") == "beginner"
        ]
        if len(beginner_pool) >= count:
            available = beginner_pool
    elif level == "expert":
        advanced_pool = [
            ex for ex in available
            if ex.get("difficulty") in ("expert", "intermediate", None)
        ]
        if len(advanced_pool) >= count:
            available = advanced_pool
    # Intermediate gets the full pool

    adjusted = []
    for ex in available:
        copy = dict(ex)
        is_timed = isinstance(ex.get("reps"), str) and "sec" in ex["reps"]

        # Goal-based adjustments
        if goal == "strength":
            copy["sets"] = 4
            if not is_timed:
                copy["reps"] = "5-8"
        elif goal == "weight-loss":
            copy["sets"] = 3
            if not is_timed:
                copy["reps"] = "12-15"
        elif goal == "general":
            copy["sets"] = 3
            if not is_timed:
                copy["reps"] = "10-15"

        # Level-based adjustments
        if level == "beginner":
            copy["sets"] = max(2, copy["sets"] - 1)
            if not is_timed and copy.get("reps"):
                nums = re.findall(r"\d+", copy["reps"])
                if len(nums) >= 2:
                    copy["reps"] = f"{max(5, int(nums[0]) - 2)}-{max(8, int(nums[1]) - 2)}"
            copy["rest_note"] = "Rest 90-120 seconds between sets"
        elif level == "expert":
            copy["sets"] = copy["sets"] + 1
            if not is_timed and copy.get("reps"):
                nums = re.findall(r"\d+", copy["reps"])
                if len(nums) >= 2:
                    copy["reps"] = f"{int(nums[0]) + 2}-{int(nums[1]) + 2}"
            copy["rest_note"] = "Rest 45-60 seconds between sets"
        else:
            copy["rest_note"] = "Rest 60-90 seconds between sets"

        adjusted.append(copy)

    random.shuffle(adjusted)
    return adjusted[:count]


def generate_plan(
    name: str,
    days: list[str],
    goal: str,
    equipment: str,
    level: str = "beginner",
) -> list[dict]:
    """Generate a full weekly workout plan."""
    user_level = level or "beginner"
    split = _get_split_template(len(days))
    plan = []
    split_index = 0

    level_multiplier = {"beginner": 0, "intermediate": 0, "expert": 1}
    extra_exercises = level_multiplier.get(user_level, 0)

    for day in ALL_DAYS:
        if day in days and split_index < len(split):
            template = split[split_index]
            exercises = []
            group_count = len(template["groups"])
            base_per_group = 3 if group_count <= 2 else 2
            exercises_per_group = base_per_group + extra_exercises
            day_label = template["label"].lower()

            for group in template["groups"]:
                count = exercises_per_group

                if group == "arms":
                    count = 2 + extra_exercises
                    if any(kw in day_label for kw in ["chest", "push", "tricep"]):
                        picked = [
                            ex for ex in _pick_exercises("arms", equipment, count + 2, goal, user_level)
                            if "Triceps" in ex.get("muscles", []) and "Biceps" not in ex.get("muscles", [])
                        ]
                        exercises.extend(picked[:count])
                        continue
                    elif any(kw in day_label for kw in ["back", "pull", "bicep"]):
                        picked = [
                            ex for ex in _pick_exercises("arms", equipment, count + 2, goal, user_level)
                            if "Biceps" in ex.get("muscles", [])
                        ]
                        exercises.extend(picked[:count])
                        continue

                if group == "core":
                    count = 2 + extra_exercises

                picked = _pick_exercises(group, equipment, count, goal, user_level)
                exercises.extend(picked)

            plan.append({
                "day": day,
                "label": template["label"],
                "exercises": exercises,
                "is_rest": False,
            })
            split_index += 1
        else:
            plan.append({
                "day": day,
                "label": "Rest Day",
                "exercises": [],
                "is_rest": True,
            })

    return plan


def estimate_calories(exercise_count: int, goal: str) -> int:
    base_per_exercise = {"weight-loss": 45, "strength": 35}.get(goal, 40)
    return exercise_count * base_per_exercise


def estimate_duration(exercise_count: int, goal: str) -> str:
    mins_per_exercise = {"strength": 10, "weight-loss": 7}.get(goal, 8)
    total = exercise_count * mins_per_exercise
    return f"{total}-{total + exercise_count * 2}"
