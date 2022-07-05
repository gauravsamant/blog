from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.contrib.auth import get_user_model, login
from django.forms import ValidationError
from rest_framework.views import APIView
from knox.models import AuthToken as Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from knox.views import LoginView
from .serializers import SiteUserSerializer, RegisterSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = SiteUserSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        if not pk:
            raise ValidationError("User Primary key is not provided")
        try:
            user = User.object.get(pk=pk)
            serializer = self.get_serializer(data=user)
            if serializer.is_valid(raise_exception=True):
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise e


class LoginAPIView(LoginView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        data = {}
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("Serializer :", serializer.data)
        user = serializer.validated_data['user']
        print("User :", user.first_name)
        request.user = user
        # username = request.data['username']
        # password = request.data['password']
        # try:
        #     user = User.objects.get(Q(email=username) | Q(username=username))
        # except BaseException as e:
            # raise ValidationError({"400": f'{str(e)}'})
        # serializer = SiteUserSerializer(data=user)
        # if serializer.is_valid():
        #     user = serializer.validated_data[user]
        return super(LoginAPIView, self).post(request, format=None)
# ************************************************************************************
        # token = Token.objects.get_or_create(user=user)[0].key
        # if not check_password(password, user.password):
        #     raise ValidationError({"message": "Incorrect Login credentials"})

        # if user:
        #     if user.is_active:
        #         login(request, user)
        #         data["message"] = "user logged in"
        #         data["email_address"] = user.email
        #         Res = {"data": data, "token": token}
        #         return Response(Res)
        #     else:
        #         raise ValidationError({"400": f'user not active'})
        # else:
        #     raise ValidationError({"400": f'user doesnt exist'})
# *************************************************************************************
        # import base64
        # print(request.data)
        # print(str(base64.b64decode(request.headers['Authorization'].split(" ")[1])).split(":")[0])
        # print(kwargs)
        # username = request.data.get('username')
        # password = request.data.get('password')
        # if not username or not password:
        #     return Response("Username / Email or Password is invalid.")
            # raise ValidationError("Username / Email or Password is invalid.")
        # return Response('foo')
        # try:
        #     user = User.objects.get(Q(email=username) | Q(username=username))
        #     serializer = self.serializer_class(data=user)
        #     if serializer.is_valid(raise_exception=True):
        #         print("Inside serializer.isvalid")
        #         data = {}
        #         token = Token.objects.get_or_create(user=user)[0].key
        #         if check_password(password, user.password):

        #             print("inside check password")
        #             if user:
        #                 if user.is_active:
        #                     print("inside user.isactive")
        #                     login(request, user)
        #                     data["message"] = "user logged in"
        #                     data["email_address"] = user.email

        #                     Res = {"data": data, "token": token}
        #                     return Response(data=Res, status=status.HTTP_200_OK)

        #                 else:
        #                     return Response(status=status.HTTP_400_BAD_REQUEST)
                            # raise ValidationError({"400": f'Account not active'})
            #         return Response(status=status.HTTP_400_BAD_REQUEST)
            # else:
            #     print(serializer.errors)
            #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # raise ValidationError({"message": "Incorrect Login credentials"})
        # except BaseException as e:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
            # raise ValidationError({"400": f'{str(e)}'})



class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    http_method_names = ['POST']

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                data = {}
                user = serializer.save()
                user.is_active = True
                user.save()
                token = Token.objects.create(user=user)[0].key
                data['username'] = user.username
                data['email'] = user.email
                data['message'] = f"{user.username.capitalize} created successfully."
                data['token'] = token
                return Response(data=data, status=status.HTTP_201_CREATED)
            else:
                data = serializer.errors
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            print(e)
            raise ValidationError({"400": f'Field {str(e)} missing'})
        except Exception as e:
            raise e
