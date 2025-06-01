# utils/adaptive_test.py
LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

def next_level(level):
    try:
        return LEVELS[min(LEVELS.index(level) + 1, len(LEVELS) - 1)]
    except ValueError:
        return level

def prev_level(level):
    try:
        return LEVELS[max(LEVELS.index(level) - 1, 0)]
    except ValueError:
        return level
