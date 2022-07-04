from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super.get_queryset().filter(status='published').order_by('-published')

class Post(models.Model):
    POST_STATUS = (
        ('published', 'Published'),
        ('draft', 'Draft')
    )
    title = models.CharField(max_length=150)
    sub_title = models.CharField(max_length=250, null=True, blank=True, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    published_on = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=POST_STATUS, default='draft')
    # media = models.ImageField()


    def __str__(self):
        return f'{self.title} by {self.author}'
    class Meta:
        ordering = ['-published_on']
        constraints = [
            models.UniqueConstraint(fields=['title', 'published_on'], name='post_title_date_unique_constraint')
        ]        
    
    objects = models.Manager()
    published = PublishedManager()