"""
Code Yari Core Middleware
"""
from apps.core.auto_seed import ensure_initial_data


class AutoSeedMiddleware:
    """
    Ensures that when Code Yari runs on any server for the first time,
    the initial services, team members, projects, and site settings
    are automatically seeded without requiring manual SSH commands.
    """
    _seeded = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not AutoSeedMiddleware._seeded:
            AutoSeedMiddleware._seeded = True
            try:
                ensure_initial_data()
            except Exception:
                pass
        return self.get_response(request)
