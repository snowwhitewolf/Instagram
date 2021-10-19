from django.shortcuts import render, redirect, get_object_or_404
from .models import Feed
from .forms import FeedForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_safe

@login_required
@require_http_methods(['GET','POST'])
def index(request):
    feeds = Feed.objects.order_by('-pk')
    context = {
        'feeds': feeds
    }
    return render(request, 'feeds/index.html', context)

@login_required
@require_http_methods(['GET','POST'])
def create(request):
    if request.method == "POST":
        form = FeedForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('feeds:index')
    else:
        form = FeedForm()
    context = {
        'form': form
    }
    return render(request, 'feeds/forms.html', context)

@login_required
@require_POST
def delete(request,pk):
    if request.method == "POST":
        review = get_object_or_404(Feed,pk=pk)
        review.delete()
    return redirect('feeds:index')

@require_safe
def detail(request,pk):
    feed = get_object_or_404(Feed,pk=pk)
    context = {
        'feed':feed,
    }
    return render(request,'feeds/detail.html',context)