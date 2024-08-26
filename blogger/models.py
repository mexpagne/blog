from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
from PIL import Image
from taggit.managers import TaggableManager
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'


class BlogPost(models.Model):
    title = models.CharField(max_length=300, unique=True)   
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_avatar = models.ImageField(upload_to='uploads/avatars', default='images/logo3.png', blank=True)
    image = models.ImageField(upload_to='uploads/post_images', default='images/logo5.PNG', blank=True)
    article = RichTextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    posted_on = models.DateTimeField(auto_now_add=True)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)  
    tags = TaggableManager(blank=True)
   # comments = models.ManyToManyField() 


    def __str__(self):
        return self.title
    
    @property
    def get_comments(self):
        return self.comments.all()

    def get_read_time(self):
        from html import unescape
        from django.utils.html import strip_tags

        string = self.title + unescape(strip_tags(self.article))
        total_words = len((string).split())
        return round(total_words / 200)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        pit = Image.open(self.image.path)

        if pit.height > 250 or pit.width > 250:
            output_size = (250, 250)
            pit.thumbnail(output_size)
            pit.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        tit = Image.open(self.author_avatar.path)

        if tit.height > 150 or tit.width > 150:
            output_size = (150, 150)
            tit.thumbnail(output_size)
            tit.save(self.author_avatar.path)        
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = RichTextField()
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.content} by {self.user}'
    
    @property
    def get_replies(self):
        return self.replies.all()    
    

class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    reply = RichTextField(null=True, blank=True)

    def __str__(self):
        return f'Reply: {self.reply} by {self.user}'

    
    class Meta:
        verbose_name_plural = 'replies'


class ToReply(models.Model):
    reply = models.ForeignKey(Reply, related_name='replies', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    reply_content = RichTextField(null=True, blank=True)

    def __str__(self):
        return f'Reply: {self.reply_content} to {self.reply}'

    
    class Meta:
        verbose_name_plural = 'toreplies'

class Quote(models.Model):
    author = models.CharField(max_length=300, default="Unknown Author")
    content = RichTextField(blank=True, null=True)
    year = models.DateField(blank=True, null=True)
    quote_pic = models.ImageField(upload_to='quote/pics', default='images/logo2.png', blank=True)
    display = models.BooleanField(default=False)
    
    def __str__(self):
        return self.author

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        pit = Image.open(self.quote_pic.path)

        if pit.height > 250 or pit.width > 250:
            output_size = (200, 200)
            pit.thumbnail(output_size)
            pit.save(self.quote_pic.path)