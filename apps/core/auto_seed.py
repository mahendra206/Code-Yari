"""
Auto-seed utility for Code Yari
Automatically populates database with initial content (Team, Services,
Projects, Blogs, FAQs, Testimonials, Settings) if tables are empty.
Runs zero-touch without needing manual terminal commands on live servers.
"""
import logging
from django.conf import settings
from django.core.management import call_command

logger = logging.getLogger(__name__)

def ensure_initial_data():
    """
    Checks if initial content is missing, and if so, safely runs seed_demo_data.
    """
    try:
        from apps.services.models import Service
        from apps.core.models import TeamMember
        from apps.portfolio.models import PortfolioProject

        # If any core content is missing, automatically seed the database
        if not Service.objects.exists() or not TeamMember.objects.exists() or not PortfolioProject.objects.exists():
            print("[AutoSeed] Missing content detected in database. Seeding initial data...")
            call_command('seed_demo_data')
            print("[AutoSeed] Initial content seeded successfully!")
    except Exception as e:
        logger.warning(f"[AutoSeed] Notice during auto-seed: {e}")


def auto_seed_on_migrate(sender, **kwargs):
    """Signal handler for post_migrate."""
    ensure_initial_data()
