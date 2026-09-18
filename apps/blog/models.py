"""
Blog app — Models
"""
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Blog article managed via Django admin."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=220)
    excerpt = models.CharField(max_length=300, help_text='Short summary shown in listings')
    content = models.TextField(help_text='Full article content (HTML supported)')
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='posts'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='blog_posts'
    )
    tags = models.CharField(
        max_length=300, blank=True,
        help_text='Comma-separated tags, e.g. Django, SEO, Web Development'
    )

    # Publishing
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)

    # SEO
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to='blog/og/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['published', 'published_date']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        if self.published and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def get_seo_title(self):
        return self.seo_title or f'{self.title} — Code Yari Blog'

    def get_seo_description(self):
        return self.seo_description or self.excerpt

    def get_tags_list(self):
        if self.tags:
            return [t.strip() for t in self.tags.split(',') if t.strip()]
        return []

    def get_related_posts(self, count=3):
        """Return related posts from the same category."""
        qs = BlogPost.objects.filter(published=True).exclude(pk=self.pk)
        if self.category:
            qs = qs.filter(category=self.category)
        return qs.order_by('-published_date')[:count]

    @property
    def read_time(self):
        """Estimate read time in minutes."""
        words = len(self.content.split())
        minutes = max(1, words // 200)
        return minutes

    @property
    def get_image_url(self):
        if self.featured_image:
            return self.featured_image.url
        slug = self.slug or slugify(self.title)
        if 'django' in slug:
            return '/static/images/blog/cover_django.jpg'
        elif 'seo' in slug or 'google' in slug:
            return '/static/images/blog/cover_seo.jpg'
        elif '2025' in slug or 'website' in slug or 'business' in slug:
            return '/static/images/blog/cover_website2025.jpg'
        return None

    def get_theme(self):
        """Returns visual theme for the blog card."""
        if not self.category:
            return 'blog-theme-blue'
        cat_slug = self.category.slug
        if 'web' in cat_slug or 'django' in self.slug:
            return 'blog-theme-blue'
        elif 'seo' in cat_slug or 'marketing' in cat_slug or 'rank' in self.slug:
            return 'blog-theme-orange'
        elif 'ui' in cat_slug or 'design' in cat_slug:
            return 'blog-theme-pink'
        elif 'ai' in cat_slug or 'automation' in cat_slug:
            return 'blog-theme-cyan'
        elif 'business' in cat_slug or 'strategy' in cat_slug or '2025' in self.slug:
            return 'blog-theme-purple'
        return 'blog-theme-blue'

    def get_badge_icon(self):
        """Returns Bootstrap icon for category badge."""
        if not self.category:
            return 'bi-journal-text'
        cat_slug = self.category.slug
        if 'web' in cat_slug or 'django' in self.slug:
            return 'bi-code-slash'
        elif 'seo' in cat_slug or 'marketing' in cat_slug:
            return 'bi-graph-up-arrow'
        elif 'ui' in cat_slug or 'design' in cat_slug:
            return 'bi-palette'
        elif 'ai' in cat_slug or 'automation' in cat_slug:
            return 'bi-cpu'
        return 'bi-lightbulb'
