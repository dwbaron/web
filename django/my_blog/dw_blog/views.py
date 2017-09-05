from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from dw_blog.models import Post, ImageStore, Cat, Tag
import markdown
from comments.forms import CommentForm
from django.core.paginator import Paginator
# Create your views here.
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

class IndexView(ListView):
    model = Post
    template_name = 'dw_blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5


    def get_queryset(self, *args,**kwargs):
        name = self.request.user.username
        if name:
            queryset = Post.objects.filter(author__username=name)
            if not queryset:
                queryset = []
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。

        for p in page:
            p.comments = p.comment_set.count()
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3):page_number if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data



class CategoryView(ListView):
    model = Post
    template_name = 'dw_blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):

        cate = get_object_or_404(Cat, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'dw_blog/detail.html'
    context_object_name = 'post'


    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        p = Post.objects.get(pk=self.kwargs['pk'])

        if p:
            if p.author.username == self.request.user.username:
                response = super(PostDetailView, self).get(request, *args, **kwargs)
                # 将文章阅读量 +1
                # 注意 self.object 的值就是被访问的文章 post
                self.object.increase_views()

                # 视图必须返回一个 HttpResponse 对象
                return response
            else:
                raise PermissionDenied

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])

        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)

        try:
            img_list = ImageStore.objects.filter(article_id=self.object.pk)
        except Exception as e:
            img_list = None
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        print(comment_list)
        if img_list:
            # 用的是update方法
            context.update({
                'form': form,
                'img_list': img_list,
                'comment_list': comment_list
            })
        else:
            context.update({
                'form': form,
                'comment_list': comment_list
            })
        return context


def index(request):
    pindex = request.GET.get('pindex') if request.GET.get('pindex') is not None else '1'
    post_list = Post.objects.all().order_by('-created_time')
    # img = ImageStore.objects.get(name='mm1')

    paginator = Paginator(post_list, 2)
    num_pages = paginator.num_pages
    # 当前页的数据
    post_list = paginator.page(int(pindex))
    current_page = int(pindex)

    if num_pages <= 5:
        pages = range(1, num_pages+1)
    elif current_page <= 3:
        pages = range(1, 6)
    elif num_pages - current_page <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(current_page-2, current_page+3)

    for p in post_list:
        p.comments = p.comment_set.count()
    return render(request, 'dw_blog/index.html', context={'post_list': post_list, 'pages': pages})


# 文章详情页
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 阅读量更新
    post.increase_views()

    # markdown 支持
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    # 图片
    try:
        img_list = ImageStore.objects.filter(article_id=post.pk)
    except Exception as e:
        img_list = None

    form = CommentForm()

    comment_list = post.comment_set.all()
    if img_list:
        context = {'post': post,
                   'form': form,
                   'img_list': img_list,
                   'comment_list': comment_list}
    else:
        context = {'post': post,
                   'form': form,
                   'comment_list': comment_list}
    return render(request, 'dw_blog/detail.html', context=context)


def archives(request, year, month):

    post_list = Post.objects.filter(created_time__year=int(year),
                                    created_time__month=int(month)).order_by('-created_time')

    for p in post_list:
        p.comments = p.comment_set.count()
    return render(request, 'dw_blog/index.html',
                  context={'post_list': post_list})


def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Cat, pk=pk)
    img = ImageStore.objects.get(name='mm1')
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    for p in post_list:
        p.comments = p.comment_set.count()
    return render(request, 'dw_blog/index.html', context={'post_list': post_list, 'img': img.img_url.name})


class TagView(ListView):
    model = Post
    template_name = 'dw_blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)