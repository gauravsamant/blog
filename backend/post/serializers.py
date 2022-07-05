from datetime import datetime
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        if validated_data.get('status') == 'published':
            validated_data['published_on'] = datetime.now()
        return super().create(validated_data)
