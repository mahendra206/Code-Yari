from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os
import datetime

class Command(BaseCommand):
    help = 'Safely ensures superuser, services, portfolio, and core team exist without wiping anything'

    def handle(self, *args, **options):
        # 1. Ensure Superuser
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@codeyari.com')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f'[OK] Superuser "{username}" ensured.'))

        # 2. Ensure Mahendra Pratap Singh
        from apps.core.models import TeamMember
        member, m_created = TeamMember.objects.get_or_create(
            name="Mahendra Pratap Singh",
            defaults={
                'role': "Full Stack Developer",
                'bio': "Founder & Full Stack Developer at Code Yari. Passionate about building high performance web architectures, modern apps, and innovative tech solutions.",
                'order': 1,
                'is_active': True,
            }
        )
        if not m_created:
            member.role = "Full Stack Developer"
            member.order = 1
            member.is_active = True
            member.save()
        self.stdout.write(self.style.SUCCESS('[OK] Team Member "Mahendra Pratap Singh" ensured.'))

        # 3. Ensure Services if empty
        from apps.services.models import Service
        if not Service.objects.exists():
            from apps.core.management.commands.seed_demo_data import Command as SeedCommand
            seed_cmd = SeedCommand()
            seed_cmd._seed_services()
            self.stdout.write(self.style.SUCCESS('[OK] Services populated.'))
        else:
            self.stdout.write('[OK] Services already exist.')

        # 4. Ensure Portfolio if empty
        from apps.portfolio.models import PortfolioProject
        if not PortfolioProject.objects.exists():
            from apps.core.management.commands.seed_demo_data import Command as SeedCommand
            seed_cmd = SeedCommand()
            seed_cmd._seed_portfolio()
            self.stdout.write(self.style.SUCCESS('[OK] Portfolio populated.'))
        else:
            self.stdout.write('[OK] Portfolio already exists.')

        # 5. Ensure Stats if empty
        from apps.core.models import StatItem
        if not StatItem.objects.exists():
            from apps.core.management.commands.seed_demo_data import Command as SeedCommand
            seed_cmd = SeedCommand()
            seed_cmd._seed_stats()
            self.stdout.write(self.style.SUCCESS('[OK] Stats populated.'))

        # 6. Ensure SiteSettings with WhatsApp
        from apps.core.models import SiteSettings
        settings = SiteSettings.get_settings()
        settings.whatsapp = '919305287312'
        settings.save()
        self.stdout.write(self.style.SUCCESS('[OK] SiteSettings WhatsApp number configured to 919305287312.'))

        # 7. Ensure Blog Posts if empty
        from apps.blog.models import BlogPost
        if not BlogPost.objects.exists():
            from apps.core.management.commands.seed_demo_data import Command as SeedCommand
            seed_cmd = SeedCommand()
            seed_cmd._seed_blog()
            self.stdout.write(self.style.SUCCESS('[OK] Blog posts populated.'))
        else:
            self.stdout.write('[OK] Blog posts already exist.')

        # 8. Ensure Testimonials if empty
        from apps.testimonials.models import Testimonial
        if not Testimonial.objects.exists():
            from apps.core.management.commands.seed_demo_data import Command as SeedCommand
            seed_cmd = SeedCommand()
            seed_cmd._seed_testimonials()
            self.stdout.write(self.style.SUCCESS('[OK] Testimonials populated.'))
        else:
            self.stdout.write('[OK] Testimonials already exist.')

        # 9. Ensure FAQs if empty
        from apps.faq.models import FAQ
        if not FAQ.objects.exists():
            from apps.core.management.commands.seed_demo_data import Command as SeedCommand
            seed_cmd = SeedCommand()
            seed_cmd._seed_faq()
            self.stdout.write(self.style.SUCCESS('[OK] FAQs populated.'))
        else:
            self.stdout.write('[OK] FAQs already exist.')

