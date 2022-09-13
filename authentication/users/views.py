from django.db.models import Q, F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .serializers import UserLoginSerializer, EmailSerializer, ContactNumberSerializer
from .models import User, Email, ContactNumber


class UserApiView(ListCreateAPIView):

    authentication_classes = []
    permission_classes = []

    lookup_field = "username"

    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        data = User.objects.annotate(
            email=F("user_email__email"), contact=F("user_contact__contact_number")
        ).filter(username=username)

        self.serializer = UserLoginSerializer(data, many=True)
        print(self.serializer.data)
        return Response(self.serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        pass


# class UserViewSet(ModelViewSet):

#     def get_permissions(self, request):
#         if request.method == 'GET':
#             return permissions.IsAuthenticatedOrReadOnly

#     permission_classes = []

#     def get_serializer_class(self, request, *args, **kwargs):
#         if request.method == 'GET':
#             return UserLoginSerializer

#     def list(self, request):
#         pass

#     def create(self, request):
#         pass

#     def retrieve(self, request, pk=None):
#         pass

#     def update(self, request, pk=None):
#         pass

#     def partial_update(self, request, pk=None):
#         pass

#     def destroy(self, request, pk=None):
#         pass
