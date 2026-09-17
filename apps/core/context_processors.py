"""
Core app — context processors
Injects site settings and global data into all templates.
"""
from .models import SiteSettings


def site_settings(request):
    """Make SiteSettings available in all templates as `site_settings`."""
    return {'site_settings': SiteSettings.get_settings()}


def global_context(request):
    """Inject global template context (active nav, etc.)."""
    return {
        'current_path': request.path,
    }
