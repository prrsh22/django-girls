from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    title_with_category = serializers.SerializerMethodField('get_title_with_category')

    class Meta:
        model = Post
        fields = ("id", "author", "title", "text", "created_date", "published_date", "title_with_category", "category")
        extra_kwargs = {
            'category': {'write_only': True}
        }
    
    def validate(self, attrs):
        return super().validate(attrs)
    
    def validate_title(self, value):
        if (len(value) < 5):
            raise serializers.ValidationError("The title should have more than 5 letters.")
        return value
        
    def get_title_with_category(self, post):
        return f'[{post.category}] {post.title}'