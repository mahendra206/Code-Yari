"""
FAQ app — Models
"""
from django.db import models


class FAQCategory(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'FAQ Category'
        verbose_name_plural = 'FAQ Categories'

    def __str__(self):
        return self.name


class FAQ(models.Model):
    """Frequently Asked Question."""
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.ForeignKey(
        FAQCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='faqs'
    )
    published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question[:80]
