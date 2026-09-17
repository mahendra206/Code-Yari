"""
Management command: clear_demo_data
Removes demo data created by seed_demo_data.
Run: python manage.py clear_demo_data
"""
from django.core.management.base import BaseCommand
from apps.core.models import StatItem, TeamMember
from apps.services.models import Service
from apps.portfolio.models import PortfolioCategory, PortfolioProject
from apps.testimonials.models import Testimonial
from apps.blog.models import BlogCategory, BlogPost
from apps.faq.models import FAQCategory, FAQ


class Command(BaseCommand):
    help = 'Clear all demo data from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force delete without asking for confirmation',
        )

    def handle(self, *args, **options):
        force = options.get('force')
        if not force:
            confirm = input('Are you sure you want to delete all demo data? (y/N): ')
            if confirm.lower() != 'y':
                self.stdout.write(self.style.WARNING('Aborted.'))
                return

        self.stdout.write(self.style.NOTICE('Clearing demo data...'))

        StatItem.objects.all().delete()
        TeamMember.objects.all().delete()
        Service.objects.all().delete()
        PortfolioProject.objects.all().delete()
        PortfolioCategory.objects.all().delete()
        Testimonial.objects.all().delete()
        BlogPost.objects.all().delete()
        BlogCategory.objects.all().delete()
        FAQ.objects.all().delete()
        FAQCategory.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('[OK] All demo data cleared successfully.'))
