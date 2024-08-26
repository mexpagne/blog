from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comment, Reply, Quote
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from .forms import CommentForm, ReplyForm, ToReplyForm

# Create your views here.
def home(request):
    
    return render(request, 'blogger/home.html', {})

class BlogPostView(ListView):
    queryset = BlogPost.objects.filter(published=True)
    context_object_name = 'blogposts'
    template_name = 'blogger/posts.html'
    paginate_by = 6
    ordering = ['-posted_on']


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogger/post_detail.html'

class QuoteListView(ListView):
    queryset = Quote.objects.filter(display=True)
    context_object_name = 'quotes'
    template_name = 'blogger/home.html'
    paginate_by = 6
    ordering = ['-pk']

class QuoteView(DetailView):
    model = Quote
    template_name = 'blogger/quote.html'

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            msg = "Your Comment was added successfully"
            messages.add_message(request, messages.SUCCESS, msg)
            return redirect('post_detail', pk=post.id)
    else:
        form = CommentForm()
        return render(request, 'blogger/post_detail.html', {'form':form})

@login_required
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.save()
            message = "You replied to a comment now"
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('post_detail', pk=comment.post.id)
    else:
        reply_form = ReplyForm()
        return render(request, 'blogger/post_detail.html', {'reply_form':reply_form})

@login_required
def add_to_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if request.method == 'POST':
        form = ToReplyForm(request.POST)
        if form.is_valid():
            to_reply = form.save(commit=False)
            to_reply.user = request.user
            to_reply.reply = reply
            to_reply.save()
            message = 'Your contribution was added'
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('post_detail', pk=reply.comment.post.id)
    else:
        to_form = ToReplyForm()
        return render(request, 'blogger/post_detail.html', {'to_form':to_form})


class ContactView(TemplateView):
    template_name = 'blogger/contact.html'

"""
class AddComment(DetailView):
    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment')
        user = request.user
        post_id = request.POST.get('post_id')
        post = get_object_or_404(BlogPost, id=post_id)

        comment_instance = Comment(content=comment, user=user, post=post)
        comment_instance.save()
        messages.success(request, "Your Comment was added Successfully!!")

        return redirect('post_detail', pk=post.id)  

    def get(self, request, *args, **kwargs):
        messages.error(request, "An Error occurred while adding your comment, please try again!")
        return redirect('home')     
    
"""