"""
Portfolio app — Models
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class PortfolioCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Portfolio Category'
        verbose_name_plural = 'Portfolio Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PortfolioProject(models.Model):
    """A portfolio project/case study."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        PortfolioCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='projects'
    )
    client_name = models.CharField(max_length=100, blank=True, help_text='Leave blank for demo/confidential projects')
    short_description = models.CharField(max_length=300)
    full_description = models.TextField()
    featured_image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    technologies = models.JSONField(
        default=list, blank=True,
        help_text='e.g. ["Django", "PostgreSQL", "Bootstrap"]'
    )
    project_url = models.URLField(blank=True, help_text='Live project URL')
    github_url = models.URLField(blank=True)
    completion_date = models.DateField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    # SEO
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)

    # Demo label
    is_demo = models.BooleanField(
        default=False,
        help_text='Mark as demo/sample project — displayed with a "Demo" badge'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-completion_date', '-created_at']
        verbose_name = 'Portfolio Project'
        verbose_name_plural = 'Portfolio Projects'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['published', 'featured']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio:detail', kwargs={'slug': self.slug})

    def get_seo_title(self):
        return self.seo_title or f'{self.name} — Code Yari Portfolio'

    def get_seo_description(self):
        return self.seo_description or self.short_description

    @property
    def title(self):
        return self.name

    @property
    def description(self):
        return self.full_description

    @property
    def get_image_url(self):
        if self.featured_image:
            return self.featured_image.url
        slug = self.slug or slugify(self.name)
        if 'teachmantra' in slug:
            return '/static/images/portfolio/teachmantra_cover.jpg'
        if 'nexplay' in slug:
            return '/static/images/portfolio/nexplay_cover.jpg'
        if 'houzez' in slug:
            return '/static/images/portfolio/houzez_cover.jpg'
        return None


class PortfolioImage(models.Model):
    """Gallery images for a portfolio project."""
    project = models.ForeignKey(
        PortfolioProject,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(upload_to='portfolio/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Portfolio Image'
        verbose_name_plural = 'Portfolio Images'

    def __str__(self):
        return f'{self.project.name} — Image {self.order}'
