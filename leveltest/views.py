from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from collections import defaultdict

from leveltest.models import LevelQuestion, UserAnswer, LevelTestResult
from leveltest.serializers import LevelQuestionSerializer
from .utils.ai_generator import generate_ai_questions
from .utils.determine_level import determine_user_level
from api.models import UserProfile

import random

class LevelTestView(APIView):
    permission_classes = []

    def get(self, request):
        """Отримання питань різних типів"""
        question_types = ['grammar', 'idiom', 'phrasal', 'listening']
        questions = []

        for t in question_types:
            questions.extend(LevelQuestion.objects.filter(type=t).order_by('?')[:3])

        random.shuffle(questions)
        return Response(LevelQuestionSerializer(questions, many=True).data)

    def post(self, request):
        return Response({'message': 'Використовуйте кінцеву точку /final/'}, status=400)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from leveltest.models import LevelQuestion, UserAnswer, LevelTestResult
from collections import defaultdict

class FinalLevelTestView(APIView):
    permission_classes = []

    def post(self, request):
        user = request.user
        data = request.data 
        level_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
        answered_ids = set()

        for item in data:
            qid = item.get('question_id')
            selected = item.get('selected')
            if not qid or not selected:
                continue

            if str(qid).isdigit():
                try:
                    q = LevelQuestion.objects.get(id=qid)
                except LevelQuestion.DoesNotExist:
                    continue

                if qid in answered_ids:
                    continue
                answered_ids.add(qid)

                is_correct = q.correct.lower() == selected.lower()
                level = q.level

                UserAnswer.objects.update_or_create(
                    user=user,
                    question=q,
                    defaults={'selected': selected, 'is_correct': is_correct, 'level': level}
                )
            else:
                q_text = qid
                correct = item.get('correct')
                level = item.get('level')

                if not correct or not level:
                    continue

                is_correct = correct.lower() == selected.lower()

            level_stats[level]['total'] += 1
            if is_correct:
                level_stats[level]['correct'] += 1

     
        level_percent = {
            level: round((s['correct'] / s['total']) * 100, 2) if s['total'] else 0
            for level, s in level_stats.items()
        }

        final_level = determine_user_level(level_percent)

        avg_score = round(
            sum(s['correct'] for s in level_stats.values()) /
            sum(s['total'] for s in level_stats.values()) * 100, 2
        ) if level_stats else 0.0

        LevelTestResult.objects.create(
            user=user,
            level=final_level,
            score=avg_score
        )
        
        try:
            profile = UserProfile.objects.get(user=user)
            profile.english_level = final_level
            profile.save()
        except UserProfile.DoesNotExist:
            pass  

        return Response({
            'level': final_level,
            'score': avg_score,
            'details': level_percent
        })


@api_view(['GET'])
def generate_ai(request):
    """Генерація AI питань на основі рівня"""
    level = request.GET.get('level', 'B1')
    try:
        questions = generate_ai_questions(level)
        return Response({'questions': questions})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

