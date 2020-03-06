from django.db import models
from django.conf import settings
from django.shortcuts import reverse
import markdown

# Create your models here.
class Category(models.Model):
    # blog_id = models.IntegerField()
    key_types = models.CharField(max_length=15)
    description = models.CharField(max_length=50, default = 'desc')

    class Meta:
        ordering = ['id']
    #     db_table = 'blogs'
    def __str__(self):
        return '%s' %(self.key_types)


class SubCategory(models.Model):
    name = models.CharField(max_length= 20)
    blog_type = models.ForeignKey('Category', on_delete = models.CASCADE)

    def __str__(self):
        return '%s-%s' %(self.name, self.blog_type)

    def get_absolute_url(self):
        return reverse('myblog:category', kwargs={'slug': self.name, 'bigslug': self.blog_type.description})

    def get_article_list(self):
        return Article.objects.filter(category=self)

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'blog_type_id')

class Tag(models.Model):
    name = models.CharField(max_length= 30)
    total_num = models.IntegerField(default=0)

    def __str__(self):
        return '%s'%self.name

class Course(models.Model):
    name = models.CharField(max_length= 90)
    def __str__(self):
        return '%s'%self.name

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length=200, unique = True)
    summary = models.TextField(max_length=230)
    content = models.TextField()
    img_link = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add= True)
    revise_date = models.DateTimeField(auto_now= True)
    visitors = models.IntegerField(default=0)
    # comments = models.CharField(max_length=250)
    like = models.IntegerField(default=0)
    category = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
    tags = models.ManyToManyField(Tag)
    courses = models.ManyToManyField(Course)

    def get_absolute_url(self):
        return reverse('myblog:article', kwargs={'pk':self.id})

    def body_to_markdown(self):
        return markdown.markdown(self.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    def update_views(self):
        self.visitors += 1
        self.save(update_fields=['visitors'])

    def __str__(self):
        return '%s-%s-%s' %(self.title, self.author, self.category)

# class Comment(models.Model):
#     content = models.TextField()
#     pub_date = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, blank=True, null=True)
#     article = models.ForeignKey(Article, blank=True, null=True)
#     pid = models.ForeignKey('self', blank=True, null=True)

#     class Meta:
#         ordering = ['-pub_date']

#     def __str__(self):
#         return str(self.id)

class Slides(models.Model):
    squence = models.IntegerField()
    title = models.CharField(max_length=120)
    # description = models.CharField(max_length=80)
    img_url = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    is_big = models.BooleanField(default= True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return '%s'%self.title


class FriendLink(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank = True)
    link = models.URLField()
    create_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default= True)
    is_show = models.BooleanField(default=False)

    def __str__(self):
        return '%s-%s'%(self.name, self.description)

