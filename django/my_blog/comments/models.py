from django.db import models
from django.utils.six import python_2_unicode_compatible
from dw_blog.models import Post
# Create your models here.


@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=64)

    email = models.EmailField(max_length=255)

    url = models.URLField(blank=False)

    text = models.TextField()

    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post)

    def __str__(self):
        return self.text[:15]


