from django.contrib import admin
from .models import Comment, BlogPost, Category, Reply, ToReply, Quote


# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Quote)
