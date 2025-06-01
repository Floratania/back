
# utils/determine_level.py

LEVEL_ORDER = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

def determine_user_level(level_percent):
    # Всі рівні з ≥ 70%
    passed = [lvl for lvl, pct in level_percent.items() if pct >= 70]
    if not passed:
        return 'A1'

    # Обрати найвищий з пройдених
    return max(passed, key=lambda l: LEVEL_ORDER.index(l))
