"""
Core robots.txt URL — separate include to avoid namespace conflict
"""
from django.urls import path
from apps.core.views import robots_txt

urlpatterns = [
    path('', robots_txt, name='robots_txt'),
]
