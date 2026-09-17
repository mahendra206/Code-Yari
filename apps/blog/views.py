"""Blog views with pagination and category filtering"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import BlogPost, BlogCategory


def blog_list(request):
    category_slug = request.GET.get('category')
    posts = BlogPost.objects.filter(published=True).select_related('category', 'author')
    categories = BlogCategory.objects.all()
    active_category = None

    if category_slug:
        active_category = get_object_or_404(BlogCategory, slug=category_slug)
        posts = posts.filter(category=active_category)

    paginator = Paginator(posts, getattr(settings, 'BLOG_POSTS_PER_PAGE', 9))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_title': 'Blog — Code Yari',
        'meta_description': 'Read the Code Yari blog for insights on web development, SEO, digital marketing, app development, and technology trends.',
        'page_obj': page_obj,
        'categories': categories,
        'active_category': active_category,
    }
    return render(request, 'blog/list.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    related_posts = post.get_related_posts(count=3)

    context = {
        'page_title': post.get_seo_title(),
        'meta_description': post.get_seo_description(),
        'post': post,
        'related_posts': related_posts,
        'tags': post.get_tags_list(),
    }
    return render(request, 'blog/detail.html', context)
