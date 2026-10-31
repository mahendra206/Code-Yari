"""
Data migration to seed initial Code Yari data (Services, Team, Projects, Blogs, Testimonials, Settings)
"""
from django.db import migrations
from django.core.management import call_command


def seed_data(apps, schema_editor):
    try:
        call_command('seed_demo_data')
    except Exception as e:
        print(f"Data migration notice: {e}")


def unseed_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('services', '0001_initial'),
        ('portfolio', '0001_initial'),
        ('testimonials', '0001_initial'),
        ('blog', '0001_initial'),
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_code=unseed_data),
    ]
