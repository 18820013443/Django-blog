from django.urls import path, re_path
# from . import views
from .views import (IndexView, DetailView, MessageView, AboutView, DonateView, ExchangeView, ProjectView, QuestionView, LoveView, LinkView, MySearchView)

app_name = 'myblog'
urlpatterns = [
    path('index/', IndexView.as_view(template_name='index.html'), name='index'),
    path('link/', LinkView, name='link'),     # 申请友情链接
    path('category/message/', MessageView, name='message'),
    path('category/about/', AboutView, name='about'),
    path('category/donate/', DonateView, name='donate'),
    path('category/exchange/', ExchangeView, name='exchange'),
    path('category/project/', ProjectView, name='project'),
    path('category/question/', QuestionView, name='question'),
    # 分类页面
    re_path(r'^category/(?P<bigslug>.*?)/(?P<slug>.*?)', IndexView.as_view(template_name='content.html'), name='category'),
    # 归档页面
    re_path(r'^date/(?P<year>\d+)/(?P<month>\d+)/$', IndexView.as_view(template_name='archive.html'), name='date'),
    # 标签页面
    re_path(r'^tag/(?P<tag>.*?)/$', IndexView.as_view(template_name='content.html'), name='tag'),
    # 文章详情页面
    re_path(r'^article/(?P<pk>.*?)/$', DetailView.as_view(), name='article'),
    # 全文搜索
    # path('search/', MySearchView.as_view(), name='search'),
    # 喜欢
    path('love/', LoveView, name='love'),
    re_path(r'^search/$', MySearchView.as_view(), name='search_view'),
]