from django.urls import path
from .views import RegisterView, LoginView, profile_view, UserProfileView, DeleteUserView



urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', profile_view),
    path('my_profile/', UserProfileView.as_view(), name='my_profile'),
    path('delete-account/', DeleteUserView.as_view(), name='delete-account'),
]
