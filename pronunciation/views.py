from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, F, ExpressionWrapper, IntegerField
from django.db.models.functions import TruncDate
from .models import PronunciationAttempt
from .serializers import PronunciationAttemptSerializer
import difflib

class PronunciationAttemptViewSet(viewsets.ModelViewSet):
    serializer_class = PronunciationAttemptSerializer
    permission_classes = []

    def get_queryset(self):
        return PronunciationAttempt.objects.filter(user=self.request.user).order_by('-timestamp')

    def perform_create(self, serializer):
        expected = serializer.validated_data['word'].lower()
        spoken = serializer.validated_data['spoken_text'].lower()
        ratio = difflib.SequenceMatcher(None, expected, spoken).ratio()
        score = round(ratio * 100, 2)
        is_correct = ratio >= 0.85

        serializer.save(user=self.request.user, score=score, is_correct=is_correct)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = request.user
        total = PronunciationAttempt.objects.filter(user=user).count()
        correct = PronunciationAttempt.objects.filter(user=user, is_correct=True).count()
        return Response({
            'total_attempts': total,
            'correct_attempts': correct,
            'accuracy': round((correct / total * 100), 2) if total else 0
        })

    @action(detail=False, methods=['get'])
    def history(self, request):
        user = request.user
        queryset = PronunciationAttempt.objects.filter(user=user).order_by('-timestamp')[:30]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
  
