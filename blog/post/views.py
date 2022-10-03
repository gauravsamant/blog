from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from services.events.events import EventManager

from .models import Post
from .serializers import PostSerializer

# Create your views here.


class PostViewSet(ModelViewSet):
    authentication_classes = []
    permission_classes = []

    def get_serializer_class(self):
        return PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def list(self, request):
        pass

    def create(self, request):
        event_mgr = EventManager(
            request=request,
            event_name="post_created",
            event_type="dispatch",
            event_queue="post_created",
            event_body="new_post",
        )
        print("postcreated")

        event_mgr.dispatch()
        return Response("post recieved")

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
