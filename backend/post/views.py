import datetime
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from knox.auth import TokenAuthentication
from .serializers import PostSerializer
from .models import Post

class PostViewSet(viewsets.ModelViewSet):

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        return Post.objects.all()

    # def list(self, request):
    #     pass    

    def create(self, request):
        if request.data.get('status') == 'published':
            request.data['publishted_on'] = datetime.datetime.now()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # print(post)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass