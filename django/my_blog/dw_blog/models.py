import markdown
from django.db import models
from users.models import User
from django.core.urlresolvers import reverse
# Create your models here.
from ckeditor.fields import RichTextField
# from django.utils.html import strip_tags


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

    body = models.TextField(blank=True, null=True, verbose_name="Body")

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
    #     # 如果没有填写摘要
    #     if not self.excerpt:
    #         # 首先实例化一个 Markdown 类，用于渲染 body 的文本
    #         md = markdown.Markdown(extensions=[
    #             'markdown.extensions.extra',
    #             'markdown.extensions.codehilite',
    #         ])
    #         # 先将 Markdown 文本渲染成 HTML 文本
    #         # strip_tags 去掉 HTML 文本的全部 HTML 标签
    #         # 从文本摘取前 128 个字符赋给 excerpt
    #         self.excerpt = md.convert(self.body)[:64]
    #         print(self.excerpt)
    #
    #     # 调用父类的 save 方法将数据保存到数据库中
    #     super(Post, self).save(*args, **kwargs)


class ImageStore(models.Model):
    name = models.CharField(max_length=64, null=True)
    article = models.ForeignKey(Post)

    img_url = models.ImageField(upload_to='img')

    def __str__(self):
        return self.name
