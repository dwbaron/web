from django.shortcuts import render, get_object_or_404, redirect
from dw_blog.models import Post

from comments.models import Comment
from comments.forms import CommentForm

# Create your views here.


def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        # 提交的表单在request.POST里面
        form = CommentForm(request.POST)

        if form.is_valid():
            # 用表单数据生成Comment类的实例，不保存到数据库
            # 因为只有form定义的字段
            comment = form.save(commit=False)

            comment.post = post

            comment.save()

            return redirect(post)

        else:
            # 反向查找所有评论
            comment_list = post.comment_set.all()

            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list}

            return render(request, 'dw_blog/detail.html', context=context)
    # 不是post请求, 没有提交数据
    # 如果只返回模型实例，那么这个模型必须实现get_absolute_url方法
    return redirect(post)
