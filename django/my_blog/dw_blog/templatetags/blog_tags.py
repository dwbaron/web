from ..models import Post, Cat, Tag
from django import template
from django.db.models.aggregates import Count
from users.models import User

register = template.Library()


# 注册为模板标签,可以在模板中调用{% get_recent_posts %}就相当于调用函数
@register.simple_tag
def get_recent_posts(user, num=5):
    user = User.objects.get(username=user)
    post_list = Post.objects.filter(author=user)
    return post_list.order_by('-created_time')[:num]


# 归档标签函数,返回年-月的列表
@register.simple_tag
def archives(user):
    user = User.objects.get(username=user)
    post_list = Post.objects.filter(author=user)
    return post_list.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories(user):
    res = []
    user = User.objects.get(username=user)
    post_list = Post.objects.filter(author=user)
    for p in post_list:
        res.append(p.category)
    return res


@register.simple_tag
def get_tags(user):
    res = []
    user = User.objects.get(username=user)
    post_list = Post.objects.filter(author=user)
    for p in post_list:
        for t in p.tags.all():
            res.append(t)
    return res


