"""
main.py - Fitness Tracker CLI Application
Използва WorkoutSession от models.py
"""

from models import WorkoutSession
from datetime import date


def print_header():
    print("\n" + "=" * 50)
    print("       💪  ФИТНЕС ТРАКЕР  💪")
    print("=" * 50)


def print_menu():
    print("\n📋 МЕНЮ:")
    print("  1. Нова тренировъчна сесия")
    print("  2. Добави упражнение")
    print("  3. Задай продължителност")
    print("  4. Виж обобщение")
    print("  5. Най-тежко упражнение")
    print("  6. Сортирай по калории")
    print("  7. Филтрирай по минимален брой серии")
    print("  0. Изход")
    print("-" * 50)


def get_int(prompt: str) -> int:
    """Помощна функция — чете цяло число от потребителя."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  ✘ Моля въведи цяло число.")


def main():
    print_header()
    session = None

    while True:
        print_menu()
        choice = input("Избор: ").strip()

        # ── 1. Нова сесия ─────────────────────────────────────
        if choice == "1":
            name = input("  Въведи име на тренировката: ").strip()
            if not name:
                name = "Тренировка"
            session = WorkoutSession(name, date.today())
            print(f"\n  ✔ Сесия '{name}' създадена за {date.today()}!")

        # ── 2. Добави упражнение ───────────────────────────────
        elif choice == "2":
            if not session:
                print("  ✘ Първо създай сесия (опция 1).")
                continue
            ex_name = input("  Упражнение: ").strip()
            sets    = get_int("  Серии: ")
            reps    = get_int("  Повторения: ")
            cals    = get_int("  Калории: ")
            session.add_exercise(ex_name, sets, reps, cals)

        # ── 3. Продължителност ─────────────────────────────────
        elif choice == "3":
            if not session:
                print("  ✘ Първо създай сесия (опция 1).")
                continue
            mins = get_int("  Продължителност (минути): ")
            session.set_duration(mins)

        # ── 4. Обобщение ───────────────────────────────────────
        elif choice == "4":
            if not session:
                print("  ✘ Няма активна сесия.")
                continue
            summary = session.get_summary()
            cpm     = session.get_calories_per_minute()
            print("\n  📊 ОБОБЩЕНИЕ:")
            print(f"    Тренировка  : {summary['name']}")
            print(f"    Дата        : {summary['date']}")
            print(f"    Упражнения  : {summary['exercises_count']}")
            print(f"    Калории     : {summary['total_calories']} ккал")
            print(f"    Продължит.  : {summary['duration_minutes']} мин")
            print(f"    Интензивност: {cpm} ккал/мин")
            if summary["exercises"]:
                print("\n    Упражнения:")
                for i, e in enumerate(summary["exercises"], 1):
                    print(f"      {i}. {e['name']} — {e['sets']}x{e['reps']} ({e['calories']} ккал)")

        # ── 5. Най-тежко упражнение ────────────────────────────
        elif choice == "5":
            if not session:
                print("  ✘ Няма активна сесия.")
                continue
            hardest = session.find_hardest_exercise()
            if hardest:
                print(f"\n  🔥 Най-тежко: {hardest['name']} — "
                      f"{hardest['sets']}x{hardest['reps']} ({hardest['calories']} ккал)")
            else:
                print("  ℹ Няма добавени упражнения.")

        # ── 6. Сортирай по калории ─────────────────────────────
        elif choice == "6":
            if not session:
                print("  ✘ Няма активна сесия.")
                continue
            order = input("  Сортиране: (1) Низходящо  (2) Възходящо → ").strip()
            desc  = order != "2"
            sorted_ex = session.sort_exercises_by_calories(descending=desc)
            label = "↓ Низходящо" if desc else "↑ Възходящо"
            print(f"\n  📈 Упражнения ({label}):")
            for i, e in enumerate(sorted_ex, 1):
                print(f"    {i}. {e['name']} — {e['calories']} ккал")

        # ── 7. Филтрирай по серии ──────────────────────────────
        elif choice == "7":
            if not session:
                print("  ✘ Няма активна сесия.")
                continue
            min_s = get_int("  Минимален брой серии: ")
            filtered = session.filter_by_min_sets(min_s)
            if filtered:
                print(f"\n  🔎 Упражнения с поне {min_s} серии:")
                for e in filtered:
                    print(f"    • {e['name']} — {e['sets']} серии")
            else:
                print(f"  ℹ Няма упражнения с поне {min_s} серии.")

        # ── 0. Изход ───────────────────────────────────────────
        elif choice == "0":
            print("\n  👋 Довиждане! Продължавай да тренираш!\n")
            break

        else:
            print("  ✘ Невалиден избор. Опитай пак.")


if __name__ == "__main__":
    main()
