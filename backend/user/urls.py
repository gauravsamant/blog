from unicodedata import name
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginAPIView, RegisterAPIView
router = DefaultRouter()
router.register('user', UserViewSet, basename='user')

app_name = 'user_management'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view, name='register'),
]

urlpatterns += router.urls