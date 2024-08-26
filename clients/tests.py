from django.test import TestCase
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from blogger.forms import ToReplyForm, ReplyForm, CommentForm
from blogger import models
# Create your tests here.

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(models.BlogPost, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            mesg = "You left a commment"
            messages.add_message(request, messages.SUCCESS, mesg)
            return redirect('post_detail', pk=post.id)
        
    else:
        form = CommentForm()
        return render(request, 'blogger/post_detail.html', {'form':form})


@login_required
def add_reply(request, comment_id):
    comment = get_object_or_404(models.Comment, id=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.save()
            mesg = "You replied a commment"
            messages.add_message(request, messages.SUCCESS, mesg)
            return redirect('post_detail', pk=comment.post.id)
        
    else:
        form = ReplyForm()
        return render(request, 'blogger/post_detail.html', {'form':form})

def register(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            message = 'you signed in succcessfully'
            messages.add_message(request, messages.SUCCESS, message)
            return redirect('home')
    else:
        form = ClientForm()
        return render(request, 'store/register.html', {'form':form})

https://github.com/ashrafalmayah/ashrafalmayah.github.io/tree/main/interactive-comments-section-main

https://www.codehim.com/forms/html-code-for-comment-box-with-reply/

https://codepen.io/tahmid-hm-dev/pen/BaLBgjo

$("#registrationForm").submit(function(event){
                event.preventDefault();  // Prevent full page reload
            
                var formData = new FormData(this);  // Gather all form data
                
                $.ajax({
                    url: $(this).attr('action'),
                    type: $(this).attr('method'),
                    data: formData,
                    contentType: false,
                    processData: false,
                    success: function(data) {
                        // Handle successful form submission
                        // Optionally redirect or show a success message
                    },
                    error: function() {
                        alert("An error occurred while submitting the form.");
                    }
                });
            });

var coll = document.getElementsById("collapsible");
            var i;

            for (i = 0; i < coll.length; i++) {
                coll[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var content = this.nextElementSibling;
                    if (content.style.maxHeight){
                        content.style.maxHeight = null;
                    } else {
                        content.style.maxHeight = content.scrollHeight + "px";
                    }
                });
            }

body {
  --text-color: #222;
  --bkg-color: #fff;
}
body.dark-theme {
  --text-color: #eee;
  --bkg-color: #121212;
}

@media (prefers-color-scheme: dark) {
  /* defaults to dark theme */
  body {
    --text-color: #eee;
    --bkg-color: #121212;
  }
  body.light-theme {
    --text-color: #222;
    --bkg-color: #fff;
  }
}

* {
  font-family: Arial, Helvetica, sans-serif;
}

body {
  background: var(--bkg-color);
}

h1,
p {
  color: var(--text-color);
}

const btn = document.querySelector(".btn-toggle");
const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

const currentTheme = localStorage.getItem("theme");
if (currentTheme == "dark") {
  document.body.classList.toggle("dark-theme");
} else if (currentTheme == "light") {
  document.body.classList.toggle("light-theme");
}

btn.addEventListener("click", function () {
  if (prefersDarkScheme.matches) {
    document.body.classList.toggle("light-theme");
    var theme = document.body.classList.contains("light-theme")
      ? "light"
      : "dark";
  } else {
    document.body.classList.toggle("dark-theme");
    var theme = document.body.classList.contains("dark-theme")
      ? "dark"
      : "light";
  }
  localStorage.setItem("theme", theme);
});