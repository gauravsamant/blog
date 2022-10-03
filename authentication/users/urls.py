from django.urls import path
from .views import UserApiView, UserCreateApiView

app_name = "authentication.users"
urlpatterns = [
    path("user/me", UserApiView.as_view(), name="user_details"),
    path("user/create", UserCreateApiView.as_view(), name="user_create"),
]
