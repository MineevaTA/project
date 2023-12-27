from django.db import models
from django.template.defaultfilters import truncatewords

# Create your models here.

from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from .managers import PostPublishedManager, PostManager, CommentManager

class Post(models.Model):

	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, verbose_name="Заголовок")
	text = models.TextField(verbose_name="Текст статьи")
	created_date = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
	published_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата публикации")

	objects = PostManager()
	published = PostPublishedManager()

	is_published = models.BooleanField(default=False, verbose_name="Запись опубликована?")


	def is_publish(self):
		return True if self.published_date else False

	def publish(self):
		self.published_date = timezone.now()
		self.is_published = True
		self.save()

	class Meta:
		verbose_name = 'Запись в блоге'
		verbose_name_plural = 'Записи в блоге'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post_detail', args=[str(self.id)])

	def get_text_preview(self):
		return truncatewords(self.text, 10)


class Comment(models.Model):
	post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
	author = models.CharField(max_length=200)
	text = models.TextField(verbose_name='Комментарий')
	created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
	approved_comment = models.BooleanField(default=False, verbose_name='Одобрен?')

	objects = CommentManager()
	# published = CommentPublishedManager()

	def approve(self):
		self.approved_comment = True
		self.save()

	def __str__(self):
		return self.text


	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'




