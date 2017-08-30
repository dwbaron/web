from django.conf.urls import url
from django.conf.urls.static import static

from my_blog import settings
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',
        views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^notebook/$', views.notebook)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # media文件路径配置 重点

