from ..models import Post, Cat
from django import template

register = template.Library()


# 注册为模板标签,可以在模板中调用{% get_recent_posts %}就相当于调用函数
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


# 归档标签函数,返回年-月的列表
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    # 别忘了在顶部引入 Category 类
    return Cat.objects.all()