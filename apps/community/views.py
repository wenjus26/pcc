from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.citizens.models import Category
from .models import Thread, Comment

@login_required
def forum_home(request):
    """List categories as entry points to the forum."""
    categories = Category.objects.all()
    recent_threads = Thread.objects.order_by('-created_at')[:5]
    return render(request, 'community/forum_home.html', {
        'categories': categories,
        'recent_threads': recent_threads
    })

@login_required
def thread_list(request, category_id):
    """List threads for a specific category."""
    category = get_object_or_404(Category, id=category_id)
    threads = category.threads.all().order_by('-created_at')
    return render(request, 'community/thread_list.html', {
        'category': category,
        'threads': threads
    })

@login_required
def thread_detail(request, pk):
    """View a single thread and its comments."""
    thread = get_object_or_404(Thread, pk=pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                thread=thread,
                content=content,
                author=request.user
            )
            return redirect('community:thread_detail', pk=pk)
            
    return render(request, 'community/thread_detail.html', {'thread': thread})

@login_required
def create_thread(request, category_id):
    """Create a new thread in a category."""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            thread = Thread.objects.create(
                category=category,
                title=title,
                content=content,
                author=request.user
            )
            return redirect('community:thread_detail', pk=thread.pk)
            
    return render(request, 'community/thread_form.html', {'category': category})
