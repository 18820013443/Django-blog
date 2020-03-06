from django import template
from ..models import Category,SubCategory,Article,Tag,Course,FriendLink,Slides
from django.db.models.aggregates import Count
from django.utils.html import mark_safe
import re

register = template.Library()

# 获取导航条大分类查询集
@register.simple_tag
def get_category_list():
    """返回大分类列表"""
    return Category.objects.all()

# 返回文章分类查询集
# 查询外键的值
@register.simple_tag
def get_subcategory_list(id):
    """返回小分类列表"""
    return SubCategory.objects.filter(blog_type=id)

#获取左侧图片滑动数据
@register.simple_tag
def get_slides_list_left():
    return Slides.objects.filter(is_big = True)

#获取右侧图片滑动数据
@register.simple_tag
def get_slides_list():
    return Slides.objects.filter(is_big = False)

#获取标签云数据
@register.simple_tag
def get_data_date():
    """获取文章发表的不同月份"""
    article_dates = Article.objects.datetimes('pub_date', 'month', order='DESC')
    return article_dates

# 获取热门排行数据查询集，参数：sort 文章类型， num 数量
@register.simple_tag
def get_article_list(sort=None, num=None):
    """
    获取指定排序方式和指定数量的文章
        sort是排序的关键字, 如按照likes来排序
        num是取多少篇文章排序
    """
    if sort:
        if num:
            return Article.objects.order_by(sort)[:num]
        return Article.objects.order_by(sort)
    if num:
        return Article.objects.all()[:num]
    return Article.objects.all()


# 返回活跃的友情链接查询集
@register.simple_tag
def get_friends():
    """获取活跃的友情链接"""
    return FriendLink.objects.filter(is_show=True, is_active=True)

# 返回标签查询集
@register.simple_tag
def get_tag_list():
    """返回标签列表"""
    return Tag.objects.annotate(total_article=Count('article')).filter(total_article__gt=0)

# 获取文章标签信息，参数文章ID
@register.simple_tag
def get_article_tag(article_id):
    return Tag.objects.filter(article__id=article_id)

# 获取前一篇文章，参数当前文章 ID
@register.simple_tag
def get_article_previous(article_id):
    has_previous = False
    id_previous = int(article_id)
    while not has_previous and id_previous >= 1:
        article_previous = Article.objects.filter(id=id_previous - 1).first()
        if not article_previous:
            id_previous -= 1
        else:
            has_previous = True
    if has_previous:
        article = Article.objects.filter(id=id_previous).first()
        return article
    else:
        return


# 获取下一篇文章，参数当前文章 ID
@register.simple_tag
def get_article_next(article_id):
    has_next = False
    id_next = int(article_id)
    article_id_max = Article.objects.all().order_by('-id').first()
    id_max = article_id_max.id
    while not has_next and id_next <= id_max:
        article_next = Article.objects.filter(id=id_next + 1).first()
        if not article_next:
            id_next += 1
        else:
            has_next = True
    if has_next:
        article = Article.objects.filter(id=id_next).first()
        return article
    else:
        return


# 获取文章详情页下方的推荐阅读文章
@register.simple_tag
def get_category_article():
    article_4 = get_article_list('visitors', 4)
    article_8 = get_article_list('visitors', 8)
    return {'article_4': article_4, 'article_8': article_8}

# 获取文章大分类
@register.simple_tag
def get_title(category):
    cat = Category.objects.filter(description=category)
    if cat:
        return cat[0]

@register.simple_tag
def my_highlight(text, q):
    """自定义标题搜索词高亮函数，忽略大小写"""
    if len(q) > 1:
        try:
            text = re.sub(q, lambda a: '<span class="highlighted">{}</span>'.format(a.group()),
                          text, flags=re.IGNORECASE)
            text = mark_safe(text)
        except:
            pass
    return text