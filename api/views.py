from django.utils import timezone
from datetime import datetime
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework import generics, permissions
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"detail": "User deleted successfully."})



class RegisterView(APIView):
    def post(self, request):
        data = request.data

        # 🔹 Перевірка обов'язкових полів
        required_fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'gender']
        for field in required_fields:
            if not data.get(field):
                return Response({'error': f"Поле '{field}' є обов’язковим"}, status=400)

        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        phone = data['phone']
        gender = data['gender']
        birth_date_str = data['birth_date']

        # 🔸 Перевірка унікальності користувача
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Користувач з таким імʼям вже існує'}, status=400)

        # 🔸 Обробка формату дати народження
        parsed_birth = None
        for fmt in ('%Y-%m-%d', '%d.%m.%Y'):
            try:
                parsed_birth = datetime.strptime(birth_date_str, fmt).date()
                break
            except ValueError:
                continue

        if not parsed_birth:
            return Response({
                'error': "Невірний формат дати. Використовуйте YYYY-MM-DD або DD.MM.YYYY"
            }, status=400)

        # 🔞 Перевірка віку
        today = timezone.now().date()
        age = (today - parsed_birth).days // 365
        if age < 13:
            return Response({'error': 'Вам має бути щонайменше 13 років'}, status=400)

        # ☎️ Валідація телефону
        if not re.fullmatch(r'^\d{10,15}$', phone):
            return Response({'error': 'Телефон має містити лише цифри (10–15 символів)'}, status=400)

        # 🔐 Валідація паролю
        if len(password) < 8 \
            or not re.search(r'[A-Za-z]', password) \
            or not re.search(r'\d', password) \
            or not re.search(r'[^\w\s]', password):
            return Response({
                'error': 'Пароль має бути мінімум 8 символів, містити букви, цифри та спецсимволи'
            }, status=400)

        # ✅ Створення користувача
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        # 📌 Запис у профіль, якщо існує
        if hasattr(user, 'profile'):
            user.profile.phone = phone
            user.profile.birth_date = parsed_birth
            user.profile.gender = gender
            user.profile.save()

        return Response({'message': 'Користувач успішно зареєстрований'}, status=201)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Невірні облікові дані'}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    return Response({
        'username': request.user.username
    })
