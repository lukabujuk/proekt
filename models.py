"""
models.py - Fitness Tracker Data Models
"""

from datetime import date


class WorkoutSession:
    """Представлява една тренировъчна сесия."""

    def __init__(self, name: str, workout_date: date = None):
        self.name = name
        self.workout_date = workout_date or date.today()
        self.exercises = []       # списък с упражнения
        self.total_calories = 0   # общо изгорени калории
        self.duration_minutes = 0 # продължителност в минути

    def add_exercise(self, exercise_name: str, sets: int, reps: int, calories: int):
        """Добавя упражнение към сесията."""
        exercise = {
            "name": exercise_name,
            "sets": sets,
            "reps": reps,
            "calories": calories
        }
        self.exercises.append(exercise)
        self.total_calories += calories
        print(f"  ✔ Добавено: {exercise_name} — {sets} серии x {reps} повторения ({calories} ккал)")

    def set_duration(self, minutes: int):
        """Задава продължителността на тренировката в минути."""
        if minutes <= 0:
            print("  ✘ Продължителността трябва да е положително число.")
            return
        self.duration_minutes = minutes
        print(f"  ✔ Продължителност: {minutes} минути")

    def get_summary(self) -> dict:
        """Връща обобщение на тренировъчната сесия."""
        return {
            "name": self.name,
            "date": str(self.workout_date),
            "exercises_count": len(self.exercises),
            "total_calories": self.total_calories,
            "duration_minutes": self.duration_minutes,
            "exercises": self.exercises
        }

    def get_calories_per_minute(self) -> float:
        """Изчислява калории на минута (интензивност)."""
        if self.duration_minutes == 0:
            return 0.0
        return round(self.total_calories / self.duration_minutes, 2)

    def find_hardest_exercise(self) -> dict | None:
        """Връща упражнението с най-много калории."""
        if not self.exercises:
            return None
        return max(self.exercises, key=lambda e: e["calories"])

    def filter_by_min_sets(self, min_sets: int) -> list:
        """Филтрира упражненията с поне min_sets серии."""
        return [e for e in self.exercises if e["sets"] >= min_sets]

    def sort_exercises_by_calories(self, descending: bool = True) -> list:
        """Сортира упражненията по калории."""
        return sorted(self.exercises, key=lambda e: e["calories"], reverse=descending)

    def __str__(self):
        return (
            f"WorkoutSession('{self.name}', {self.workout_date}, "
            f"{len(self.exercises)} упражнения, {self.total_calories} ккал)"
        )
