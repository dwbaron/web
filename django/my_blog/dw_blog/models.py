import markdown
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your models here.
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags


class Cat(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=64)

    body = RichTextField(blank=True, null=True, verbose_name="Body")

    created_time = models.DateTimeField(auto_now_add=True)

    modified_time = models.DateTimeField(auto_now=True)

    excerpt = models.CharField(max_length=200, blank=True)

    category = models.ForeignKey(Cat)

    tags = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(User)

    # 浏览数
    view_counts = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.view_counts += 1
        # 指定更新保存的字段
        self.save(update_fields=['view_counts'])

    # def save(self, *args, **kwargs):
    #     if not self.excerpt:
    #         md = markdown.Markdown(extensions=[
    #             'markdown.extensions.extra',
    #             'markdown.extensions.codehilite',
    #         ])
    #         self.excerpt = md.convert(self.body)[:64]
    #
    #     super(Post, self).save(*args, **kwargs)


class ImageStore(models.Model):
    name = models.CharField(max_length=64, null=True)
    article = models.ForeignKey(Post)

    img_url = models.ImageField(upload_to='img')

    def __str__(self):
        return self.name
