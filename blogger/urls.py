from django.urls import path
from . import views
from clients.views import TestimonyView

urlpatterns = [
    path('', views.QuoteListView.as_view(), name='home'),
    path('quotes/<int:pk>/', views.QuoteView.as_view(), name='quote_detail'),
    path('blog/', views.BlogPostView.as_view(), name='blog'),
    path('post_detail/<int:pk>/', views.BlogPostDetailView.as_view(), name='post_detail'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('add_reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('add_to_reply/<int:reply_id>/', views.add_to_reply, name='add_to_reply'),
    path('about/', TestimonyView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]