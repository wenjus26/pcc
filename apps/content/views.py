from django.shortcuts import render, get_object_or_404
from .models import Post, Event

def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'content/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'content/post_detail.html', {'post': post})

def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('date')
    return render(request, 'content/event_list.html', {'events': events})
