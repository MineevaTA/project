from rest_framework import serializers


from .models import Comment, Post

# class CommentSerializer(serializers.Serializer):
# 	text = serializers.CharField(max_length=200)
# 	created_date = serializers.DateTimeField()


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ('id','created_date', 'text','approved_comment')

class BlogPostListSerializer(serializers.ModelSerializer):
	preview_text = serializers.SerializerMethodField()

	def get_preview_text(self, post):
		return post.get_text_preview()

	class Meta:
		model = Post 
		fields = ('title','author','created_date','preview_text')


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		exclude = {}

class BlogPostDetailSerializer(serializers.ModelSerializer):
	comments = CommentSerializer(many=True, read_only=True)
	comments.count = serializers.SerializerMethodField()

	def get_comments_count(self, obj):
		return obj.comments.count()

	class Meta:
		model = Post
		fields = ('author', 'title','text','published_date','comments_count')


