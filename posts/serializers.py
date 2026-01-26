from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    read_time = serializers.ReadOnlyField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'content', 'cover_image', 'user', 
            'created_at', 'updated_at', 'read_time', 
            'like_count'
        ]
        read_only_fields = ['user']

    def get_like_count(self, obj):
        return obj.likes.count()