
# # # utils/determine_level.py

# # LEVEL_ORDER = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

# # def determine_user_level(level_percent):
# #     # Всі рівні з ≥ 70%
# #     passed = [lvl for lvl, pct in level_percent.items() if pct >= 70]
# #     if not passed:
# #         return 'A1'

# #     # Обрати найвищий з пройдених
# #     return max(passed, key=lambda l: LEVEL_ORDER.index(l))

# def determine_user_level(level_percent: dict) -> str:
#     """
#     Визначає найвищий рівень, на якому користувач має ≥60%,
#     і всі попередні рівні також ≥60%
#     """
#     order = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
#     final_level = 'A1'

#     for i, lvl in enumerate(order):
#         current_score = level_percent.get(lvl, 0)
#         if current_score >= 60:
#             all_previous_passed = all(level_percent.get(prev, 0) >= 60 for prev in order[:i])
#             if all_previous_passed:
#                 final_level = lvl

#     return final_level
# def determine_user_level(level_percent):
#     levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
#     weights = {lvl: i+1 for i, lvl in enumerate(levels)}
    
#     total_weight = 0
#     total_score = 0
    
#     for lvl, pct in level_percent.items():
#         score = pct / 100
#         total_weight += score
#         total_score += score * weights[lvl]
    
#     if total_weight == 0:
#         return 'A1'
    
#     average = total_score / total_weight
#     index = round(average) - 1
#     return levels[max(0, min(index, len(levels) - 1))]

# def determine_user_level(level_percent):
#     levels = ['C2', 'C1', 'B2', 'B1', 'A2', 'A1']
    
#     for level in levels:
#         if level_percent.get(level, 0) >= 60:
#             # перевірити, чи всі нижчі рівні ≥ 60
#             lower_ok = all(level_percent.get(lvl, 0) >= 60 for lvl in levels[levels.index(level)+1:])
#             if lower_ok:
#                 return level
#     return 'A1'



# def determine_user_level(level_percent):
#     levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
#     numeric_levels = []

#     for lvl in levels:
#         if lvl in level_percent:
#             numeric_levels.append((levels.index(lvl) + 1) * (level_percent[lvl] / 100))

#     if not numeric_levels:
#         return 'A1'

#     avg = sum(numeric_levels) / len(numeric_levels)
#     return levels[int(round(avg)) - 1]


level_percent = {
    'A1': 100,
    'A2': 80,
    'B1': 50,
    'B2': 30,
    'C1': 0,
    'C2': 0
}

# def determine_user_level(level_percent):
# #     level_percent = {
# #     'A1': 100,
# #     'A2': 80,
# #     'B1': 50,
# #     'B2': 30,
# #     'C1': 0,
# #     'C2': 0
# # }
#     levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
#     weights = {lvl: i + 1 for i, lvl in enumerate(levels)}

#     total_weight = 0
#     total_score = 0

#     for lvl in levels:
#         pct = level_percent.get(lvl, 0)
#         if not isinstance(pct, (int, float)) or pct < 0 or pct > 100:
#             continue  # пропускаємо некоректні значення

#         score = pct / 100
#         total_weight += score
#         total_score += score * weights[lvl]

#     if total_weight == 0:
#         return 'A1'

#     average = total_score / total_weight
#     index = int(round(average)) - 1
#     index = max(0, min(index, len(levels) - 1))

#     return levels[index]
def determine_user_level(level_percent):
    levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    weights = {lvl: i + 1 for i, lvl in enumerate(levels)}
    
    def get_pct(level):
        return level_percent.get(level, 0)

    # 1. Перевірка фундаменту
    max_allowed_level = 'A1'
    if get_pct('A1') < 35:
        return 'A1'
    max_allowed_level = 'A2'
    if get_pct('A1') >= 40 and get_pct('A2') >= 60:
        max_allowed_level = 'B1'
        if get_pct('B1') >= 60:
            max_allowed_level = 'B2'
            if get_pct('B2') >= 60:
                max_allowed_level = 'C1'
                if get_pct('C1') >= 60:
                    max_allowed_level = 'C2'

    # 2. Обчислення середньозваженого рівня
    total_weight = 0
    total_score = 0
    for lvl in levels:
        pct = get_pct(lvl)
        if not isinstance(pct, (int, float)) or not (0 <= pct <= 100):
            continue
        score = pct / 100
        total_weight += score
        total_score += score * weights[lvl]

    if total_weight == 0:
        return 'A1'

    average = total_score / total_weight
    index = int(round(average)) - 1
    index = max(0, min(index, len(levels) - 1))
    computed_level = levels[index]

    # 3. Повертаємо не вищий, ніж дозволяє фундамент
    if levels.index(computed_level) > levels.index(max_allowed_level):
        return max_allowed_level
    return computed_level
