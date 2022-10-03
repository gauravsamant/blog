from django.db.models import Q, F
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import (
    UserLoginSerializer,
    UserCreateSerializer,
    EmailSerializer,
    ContactNumberSerializer,
)
from .models import User, Email, ContactNumber


class UserApiView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    lookup_field = "username"

    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def get(self, request, *args, **kwargs):
        username = request.user.username
        try:
            data = User.objects.annotate(
                email=F("user_email__email"), contact=F("user_contact__contact_number")
            ).get(username=username)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)

        self.serializer = UserLoginSerializer(data)
        return Response(self.serializer.data, status=status.HTTP_200_OK)


class UserCreateApiView(CreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        print(request.body)
        data_list = ["username", "email", "password", "password2"]

        data_dict = {}

        for key in data_list:
            data_dict[key] = self.extract_data(request, key)

        username, email, password, password2 = data_dict.values()

        if (username and email and password and password2) and (password == password2):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("error", status=status.HTTP_403_FORBIDDEN)

        return Response(
            {"error": "invalid data", "data": request.body},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def extract_data(self, request, keyword):
        return request.data.get(keyword)
