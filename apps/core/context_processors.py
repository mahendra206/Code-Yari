"""
Core app — context processors
Injects site settings and global data into all templates.
"""
from .models import SiteSettings


_data_checked = False

def site_settings(request):
    """Make SiteSettings available in all templates as `site_settings`."""
    global _data_checked
    if not _data_checked:
        try:
            from .auto_seed import ensure_initial_data
            ensure_initial_data()
            _data_checked = True
        except Exception:
            pass
    return {'site_settings': SiteSettings.get_settings()}


def global_context(request):
    """Inject global template context (active nav, etc.)."""
    return {
        'current_path': request.path,
    }
