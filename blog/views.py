from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.http import Http404

from .forms import PostForm, CommentForm
from .models import Post, Comment
from .core.views import ActionSerializedViewSet
from .serializers import BlogPostListSerializer
from .serializers import BlogPostDetailSerializer
from .serializers import BlogPostCreateUpdateSerializer
from rest_framework.decorators import action

@login_required
def post_edit(request, id=None):
	post = get_object_or_404(Post, id=id) if id else None

	if post and post.author != request.user:
		return redirect('post_list')

	
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			if post.is_published:
				post.published_date = timezone.now()
			else:
				post.published_date = None
			post.save()
			return redirect('post_detail', id=post.id)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_publish(request, id):
	post = get_object_or_404(Post, id=id)
	post.publish()
	return redirect('post_detail', id=id)

def add_comment(request, id):
	post = get_object_or_404(Post, id=id)
	#comment = get_object_or_404(Comment, id=id) if id else None
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.author = request.user
			comment.post = post
			comment.created_date = timezone.now()
			comment.save()
			return redirect('post_detail', id=post.id)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment.html', {'form': form, 'post': post})




def post_list(request):
	posts = Post.objects.for_user(user=request.user)
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, id):
	post = get_object_or_404(Post, id=id)
	if not post.is_publish() and not request.user.is_staff:
		raise Http404("Запись в блоге не найдена")
	return render(request, 'blog/post_detail.html', {'post': post})

def handler404(request, exception, template_name="404.html"):
	response = render(request, "404.html")
	response.status_code = 404
	return response

from rest_framework import viewsets
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	queryset = Comment.objects.all()

class BlogPostViewSet(ActionSerializedViewSet):
	serializer_class = BlogPostListSerializer
	queryset = Post.objects.all()

	action_serializers = {
		'list': BlogPostListSerializer,
		'retrieve': BlogPostDetailSerializer,
		'create': BlogPostCreateUpdateSerializer,
		'update': BlogPostCreateUpdateSerializer,
	}

	def get_queryset(self):
		queryset = self.queryset
		author = self.request.query_params.get('author', None)
		if author:
			queryset = queryset.filter(author__username = author)
		return queryset

	# @action(detail=True, method=['post'], permission_classes=[IsAuthenticated])
	# def publish(self, request, pk=None):
	# 	post = self.get_object()
	# 	if request.user == post.author:
	# 		return Response({'message': 'blog post was bublished'}, status=status.HTTP_200_OK)
	# 	else:
	# 		return Response({'error':'You dont have permissions'}, status=status.HTTP_403_FORBIDDEN)

	@action(detail=False)
	def published_posts(self, request):
		published_posts = Post.published.all()
		page = self.paginate_queryset(published_posts)
		if page is not None:
			serializer = self.get_serializer(page, many = True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(published_posts, many=True)
		return Response(serializer.data)
