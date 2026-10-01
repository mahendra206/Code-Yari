from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Ensures an admin superuser exists without modifying or wiping any data'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@codeyari.com')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" password ensured and updated.'))

        # Ensure permanent core team members exist in database
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
        self.stdout.write(self.style.SUCCESS('Permanent team member "Mahendra Pratap Singh" verified.'))
