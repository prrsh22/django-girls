from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
    
    def create(self, validated_data):
        if 'category' in self.context['request'].data:
            validated_data['title'] = '[' + self.context['request'].data['category']+'] ' + validated_data['title']
        return super().create(validated_data)