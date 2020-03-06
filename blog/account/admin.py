from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Ouser)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username','email','link', 'avatar')