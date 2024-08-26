from django import forms
from .models import Comment, Reply, ToReply 

# Create your views here.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content','active']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields['content'].widget.attrs.update({'placeholder':'Leave a comment on the post'})


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply']

    def __init__(self, *args, **kwargs):
        super(ReplyForm, self).__init__(*args, **kwargs)

        self.fields['reply'].widget.attrs.update({'placeholder':'Leave a reply to this comment'})


class ToReplyForm(forms.ModelForm):
    class Meta:
        model = ToReply
        fields = ['reply_content']

    def __init__(self, *args, **kwargs):
        super(ToReplyForm, self).__init__(*args, **kwargs)

        self.fields['reply_content'].widget.attrs.update({'placeholder': 'Add to this comment thread🧵'})