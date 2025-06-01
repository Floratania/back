# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view, permission_classes

# from leveltest.models import LevelQuestion, UserAnswer, LevelTestResult
# from leveltest.serializers import LevelQuestionSerializer

# from collections import defaultdict
# from .utils.ai_generator import generate_ai_questions
# from .utils.final_level import calculate_final_level
# from .utils.adaptive_test import next_level, prev_level

# import random
# import json


# class LevelTestView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """Повертає 12 випадкових питань різних типів"""
#         question_types = ['grammar', 'idiom', 'phrasal', 'listening']
#         questions = []

#         for t in question_types:
#             questions.extend(LevelQuestion.objects.filter(type=t).order_by('?')[:3])

#         random.shuffle(questions)
#         return Response(LevelQuestionSerializer(questions, many=True).data)

#     def post(self, request):
#         """Обробляє відповіді користувача та розраховує рівень"""
#         user = request.user
#         data = request.data

#         level_scores = defaultdict(lambda: {'correct': 0, 'total': 0})
#         type_errors = defaultdict(int)

#         for item in data:
#             q = LevelQuestion.objects.get(id=item['question_id'])
#             is_correct = q.correct.lower() == item['selected'].lower()

#             level_scores[q.level]['total'] += 1
#             if is_correct:
#                 level_scores[q.level]['correct'] += 1
#             else:
#                 type_errors[q.type] += 1

#             UserAnswer.objects.create(
#                 user=user,
#                 question=q,
#                 selected=item['selected'],
#                 is_correct=is_correct
#             )

#         level_percent = {
#             lvl: round((s['correct'] / s['total']) * 100, 2)
#             for lvl, s in level_scores.items()
#         }

#         avg_score = round(
#             sum(s['correct'] for s in level_scores.values()) /
#             sum(s['total'] for s in level_scores.values()) * 100, 2
#         )

#         level_info = calculate_final_level(level_percent, type_errors)
#         result_level = level_info['adjusted_level']

#         LevelTestResult.objects.create(
#             user=user,
#             level=result_level,
#             score=avg_score
#         )

#         return Response({
#             'level': result_level,
#             'score': avg_score,
#             'details': level_percent,
#             'type_errors': type_errors,
#             'base_level': level_info['base_level'],
#             'ai_score': None,
#             'explanation': level_info['reason']
#         })


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def generate_ai(request):
#     """Генерує питання з AI (Gemini / інший LLM)"""
#     level = request.GET.get('level', 'B1')
#     try:
#         raw_response = generate_ai_questions(level, count=10)

#         try:
#             questions = json.loads(raw_response)
#         except json.JSONDecodeError:
#             return Response({
#                 'error': '❌ AI відповів у невірному форматі',
#                 'raw': raw_response[:1000]
#             }, status=500)

#         return Response({'questions': questions})
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_adaptive_questions(request):
#     """Адаптивні питання для заданого рівня"""
#     level = request.GET.get('level', 'B1')
#     count = int(request.GET.get('count', 5))

#     qs = LevelQuestion.objects.filter(level=level).order_by('?')[:count]
#     return Response(LevelQuestionSerializer(qs, many=True).data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def adjust_level(request):
#     """Коригування рівня на основі AI, типових помилок та відсотків"""
#     user = request.user
#     data = request.data

#     level_info = calculate_final_level(
#         level_percent=data.get('level_percent', {}),
#         type_errors=data.get('type_errors', {}),
#         ai_score=data.get('ai_score')
#     )

#     LevelTestResult.objects.create(
#         user=user,
#         level=level_info['adjusted_level'],
#         score=data.get('ai_score', 0)
#     )

#     return Response({
#         'level': level_info['adjusted_level'],
#         'base_level': level_info['base_level'],
#         'ai_score': level_info['ai_score'],
#         'explanation': level_info['reason']
#     })
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from leveltest.models import LevelQuestion, UserAnswer, LevelTestResult
from leveltest.serializers import LevelQuestionSerializer
from django.db.models import Q
from collections import defaultdict
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils.ai_generator import generate_ai_questions
from .utils.determine_level import determine_user_level

class LevelTestView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request):
        questions = []
        for t in ['grammar', 'idiom', 'phrasal', 'listening']:
            sample = LevelQuestion.objects.filter(type=t).order_by('?')[:3]
            questions.extend(sample)
            random.shuffle(questions)
        return Response(LevelQuestionSerializer(questions, many=True).data) 
    
    def post(self, request):
        data = request.data  # [{question_id, selected}]
        user = request.user
        level_scores = defaultdict(lambda: {'correct': 0, 'total': 0})
        for item in data:
            q = LevelQuestion.objects.get(id=item['question_id'])
            is_correct = q.correct.lower() == item['selected'].lower()
            level_scores[q.level]['total'] += 1
            if is_correct:
                level_scores[q.level]['correct'] += 1

            UserAnswer.objects.create(
                user=user,
                question=q,
                selected=item['selected'],
                is_correct=is_correct
            )

        # Розрахунок відсотків
        level_percent = {}
        for lvl, score in level_scores.items():
            percent = round((score['correct'] / score['total']) * 100, 2)
            level_percent[lvl] = percent

        # Визначення максимального рівня за логікою
        ordered = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        # result_level = 'A1'
        # for i, lvl in enumerate(ordered):
        #     if level_percent.get(lvl, 0) >= 60:
        #         # всі попередні також ≥ 60%
        #         if all(level_percent.get(prev, 0) >= 60 for prev in ordered[:i]):
        #             result_level = lvl

        result_level = determine_user_level(level_percent)
        avg_score = round(
            sum(s['correct'] for s in level_scores.values()) /
            sum(s['total'] for s in level_scores.values()) * 100, 2
        )

        LevelTestResult.objects.create(
            user=user,
            level=result_level,
            score=avg_score
        )

        return Response({'level': result_level,
            'score': avg_score,
            'details': level_percent
        })


# @api_view(['GET'])
# def generate_ai(request):

#     level = request.GET.get('level', 'B1')
#     print("🔍 Generating AI questions for level:", level)
#     try:
#         questions = generate_ai_questions(level)
#         return Response({'questions': questions})
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def generate_ai(request):
    level = request.GET.get('level', 'B1')
    try:
        print("🔍 Generating AI questions for level:", level)
        questions = generate_ai_questions(level)
        return Response({'questions': questions})
    except Exception as e:
        return Response({'error': str(e)}, status=500)