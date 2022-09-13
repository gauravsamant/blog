from django.urls import path
from .views import UserApiView

app_name = "authentication.users"
urlpatterns = [
    path("user/<str:username>", UserApiView.as_view(), name="user_details"),
]
