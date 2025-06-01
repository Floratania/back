# utils/final_level.py

def next_level(current):
    levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    try:
        idx = levels.index(current)
        return levels[min(idx + 1, len(levels) - 1)]
    except ValueError:
        return current

def prev_level(current):
    levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    try:
        idx = levels.index(current)
        return levels[max(idx - 1, 0)]
    except ValueError:
        return current

def determine_user_level(level_percent):
    levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    for i in reversed(range(len(levels))):
        lvl = levels[i]
        if level_percent.get(lvl, 0) >= 60:
            if all(level_percent.get(prev, 0) >= 60 for prev in levels[:i]):
                return lvl
    for i in reversed(range(len(levels))):
        lvl = levels[i]
        if level_percent.get(lvl, 0) >= 50:
            return lvl
    return 'A1'

def calculate_final_level(level_percent, type_errors=None, ai_score=None):
    type_errors = type_errors or {}
    result = {
        'base_level': None,
        'adjusted_level': None,
        'ai_score': ai_score,
        'reason': ''
    }

    base_level = determine_user_level(level_percent)
    result['base_level'] = base_level
    final_level = base_level

    # 🧠 1. AI Score adjustment
    if ai_score is not None:
        if ai_score >= 85:
            final_level = next_level(base_level)
            result['reason'] += f'AI-тест точність {ai_score}%, рівень підвищено. '
        elif ai_score < 60:
            final_level = prev_level(base_level)
            result['reason'] += f'AI-тест точність {ai_score}%, рівень знижено. '
        else:
            result['reason'] += f'AI-тест підтвердив рівень. '

    # 🧠 2. Помилки за типами (якщо один тип має >50% помилок — залишаємо поточний або знижуємо)
    total_errors = sum(type_errors.values())
    if total_errors > 0:
        for typ, count in type_errors.items():
            share = count / total_errors
            if share > 0.5:
                final_level = min(final_level, base_level)
                result['reason'] += f'Багато помилок у типі: {typ}. '
                break

    result['adjusted_level'] = final_level
    return result
