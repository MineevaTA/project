from django.urls import path, include
from rest_framework import routers

from . import views

from .views import CommentViewSet, BlogPostViewSet

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'posts', BlogPostViewSet)

#app_name = 'blog'
urlpatterns = [
	path('API/', include(router.urls)),
	path('', views.post_list, name='post_list'),
	path('posts/<int:id>/', views.post_detail, name='post_detail'),
	path('posts/<int:id>/edit/', views.post_edit, name='post_edit'),
	path('posts/<int:id>/publish/', views.post_publish, name='post_publish'),
	path('posts/<int:id>/comment/', views.add_comment, name='add_comment'),
	path('posts/add/', views.post_edit, name='post_add'),
]

