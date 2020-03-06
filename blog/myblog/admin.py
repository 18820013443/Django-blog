from django.contrib import admin

# Register your models here.
from .models import Category,SubCategory,Article,Tag,Course,FriendLink,Slides

# class BlogsAdmin(admin.ModelAdmin):
#     list_display = ('blog_id', 'types')

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'blog_type_id')

# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'content','author','update_date','visitors','comment','like','category')

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Course)
admin.site.register(FriendLink)
admin.site.register(Slides)




