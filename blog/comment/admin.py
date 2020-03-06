from django.contrib import admin
from .models import ArticleComment, CommentUser

# Register your models here.
@admin.register(ArticleComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'create_date', 'parent','rep_to')

@admin.register(CommentUser)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'email', 'address')
