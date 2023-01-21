from django.db import models
from django.contrib.auth.models import User #user-authentication
from django.utils import timezone
# Create your models here.
from django.urls import reverse	#new-lib
from taggit.managers import TaggableManager
# Create your models here.
class CustomManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status='published')

class Post(models.Model):
	STATUS_CHOICES=(('draft', 'Draft'), ('published', 'Published'));
	title=models.CharField(max_length=264)
	slug=models.SlugField(max_length=264,unique_for_date='publish')
	author=models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
	body=models.TextField()
	publish=models.DateField(default=timezone.now)
	created=models.DateField(auto_now_add=True) #datetime of create() action
	updated=models.DateField(auto_now_add=True)  #datetime of save() action
	status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
	objects=CustomManager();
	tags=TaggableManager()
	class Meta:
		ordering=('-publish',)
		def __str__(self):
			return self.title

	def get_absolute_url(self):
			return reverse('post_detail', args=[self.publish.year,self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug])


#comments for post

class Comment(models.Model):
	post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
	name = models.CharField(max_length=64)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateField(auto_now_add=True)
	updated = models.DateField(auto_now=True)
	active = models.BinaryField(default=True)
	class Meta:
		ordering=('created',)
	def __str__(self):
		return "Commented By {} on {}".format(self.name,self.post);