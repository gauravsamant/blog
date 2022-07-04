from django.urls import path, include

urlpatterns = [
    path('blog/', include('post.urls'))
]
