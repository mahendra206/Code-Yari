"""
Auto-seed utility for Code Yari
Automatically populates database with initial content (Team, Services,
Projects, Blogs, FAQs, Testimonials, Settings) if tables are empty.
Runs zero-touch without needing manual terminal commands on live servers.
"""
import sys
from pathlib import Path
from django.conf import settings

def ensure_initial_data():
    """
    Checks if initial content is missing, and if so, safely loads seed_data.json.
    """
    try:
        from apps.core.models import TeamMember
        # If team members don't exist, database is fresh/empty
        if not TeamMember.objects.exists():
            from django.core.management import call_command
            fixture_file = settings.BASE_DIR / 'seed_data.json'
            if fixture_file.exists():
                call_command('loaddata', str(fixture_file))
                print("[AutoSeed] Successfully populated database from seed_data.json.")
    except Exception as e:
        # Ignore errors during table creation or migration phases
        pass


def auto_seed_on_migrate(sender, **kwargs):
    """Signal handler for post_migrate."""
    ensure_initial_data()
