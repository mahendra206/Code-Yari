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

        # 2. Ensure Core Team Members
        from apps.core.models import TeamMember
        # Remove old demo dummy records if any
        TeamMember.objects.filter(name__in=['Alex Kumar', 'Priya Sharma', 'Rahul Singh', 'Neha Patel']).delete()

        team_data = [
            {
                "name": "Mahendra Pratap Singh",
                "role": "Python Full Stack Developer",
                "bio": "Founder & Full Stack Developer at Code Yari. Passionate about building high performance web architectures, modern apps, and innovative tech solutions.",
                "photo": "team/mahendraaa.png",
                "order": 1,
            },
            {
                "name": "Ayaz Khan",
                "role": "Full Stack Developer",
                "bio": "Full Stack Developer specializing in robust backend systems, REST APIs, and scalable architectures.",
                "photo": "team/ayaz.png",
                "order": 2,
            },
            {
                "name": "Lakshman Sharma",
                "role": "Full Stack Developer",
                "bio": "Full Stack Engineer crafting seamless digital experiences and clean code solutions.",
                "photo": "team/laki.png",
                "order": 3,
            },
            {
                "name": "Aditya Sharma",
                "role": "Full Stack Mern Developer",
                "bio": "Specialist in MongoDB, Express, React, and Node.js creating modern, responsive web apps.",
                "photo": "team/adityaa.png",
                "order": 4,
            },
            {
                "name": "Atul Sharma",
                "role": "Full Stack Developer",
                "bio": "Full Stack Developer focusing on scalable code, performance, and clean design.",
                "photo": "team/atul.png",
                "order": 5,
            },
            {
                "name": "Anurag bajpai",
                "role": "Seo Expert",
                "bio": "SEO and Google ranking strategist driving high organic growth and top search visibility.",
                "photo": "team/anurag.png",
                "order": 6,
            },
            {
                "name": "Abhay shukla",
                "role": "Marketing & AI Specialist",
                "bio": "AI automation and growth marketing expert helping brands scale rapidly.",
                "photo": "team/abhayy.png",
                "order": 7,
            },
            {
                "name": "Iqra",
                "role": "Frontend Developer",
                "bio": "Frontend designer & developer passionate about pixel-perfect, responsive user interfaces.",
                "photo": "team/iqraa.png",
                "order": 8,
            },
        ]

        for item in team_data:
            m, created = TeamMember.objects.get_or_create(
                name=item["name"],
                defaults={
                    "role": item["role"],
                    "bio": item["bio"],
                    "photo": item.get("photo", ""),
                    "order": item["order"],
                    "is_active": True,
                }
            )
            if not created:
                m.role = item["role"]
                m.order = item["order"]
                m.is_active = True
                if item.get("photo") and not m.photo:
                    m.photo = item["photo"]
                m.save()
        self.stdout.write(self.style.SUCCESS(f'[OK] Ensured {len(team_data)} team members.'))

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

        # 6. Ensure SiteSettings with WhatsApp, Phone & Email
        from apps.core.models import SiteSettings
        settings = SiteSettings.get_settings()
        settings.whatsapp = '919305287312'
        settings.phone = '+919305287312'
        settings.phone_display = '+91 93052-87312'
        settings.email = 'codeyari7307@gmail.com'
        settings.save()
        self.stdout.write(self.style.SUCCESS('[OK] SiteSettings WhatsApp, Phone & Email configured.'))

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

