from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PronunciationAttemptViewSet

router = DefaultRouter()
router.register(r'', PronunciationAttemptViewSet, basename='pronunciation')

urlpatterns = [
    path('', include(router.urls)),
]