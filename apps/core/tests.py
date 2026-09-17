"""
Core and full-site integration tests
Validates all routes, status codes, templates, and form submissions.
"""
from django.test import TestCase, Client
from django.urls import reverse
from apps.services.models import Service
from apps.portfolio.models import PortfolioCategory, PortfolioProject
from apps.blog.models import BlogCategory, BlogPost
from apps.faq.models import FAQCategory, FAQ
from apps.testimonials.models import Testimonial
from apps.core.models import SiteSettings, ContactMessage
from apps.leads.models import Lead


class FullSiteSmokeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.site_settings = SiteSettings.objects.create(
            site_name='Code Yari',
            tagline='Code. Create. Grow.',
            email='hello@codeyari.com',
            phone='+91 98765 43210',
            whatsapp='919876543210',
            address='India',
        )

        self.service = Service.objects.create(
            name='Web Development',
            slug='web-development',
            short_description='Custom websites.',
            full_description='<p>Full web details.</p>',
            features=['Responsive', 'SEO Ready'],
            technologies=['Django', 'Python'],
            is_featured=True,
            is_active=True,
        )

        self.port_cat = PortfolioCategory.objects.create(name='Web App', slug='web-app')
        self.project = PortfolioProject.objects.create(
            name='SaaS Dashboard',
            slug='saas-dashboard',
            category=self.port_cat,
            short_description='Enterprise SaaS.',
            full_description='<p>Full project description.</p>',
            technologies=['Django', 'PostgreSQL'],
            published=True,
            featured=True,
            is_demo=True,
        )

        self.blog_cat = BlogCategory.objects.create(name='Tech', slug='tech')
        self.blog_post = BlogPost.objects.create(
            title='Building High-Performing Django Apps',
            slug='building-high-performing-django-apps',
            category=self.blog_cat,
            excerpt='Learn how to build performant Django websites.',
            content='<p>Article content here.</p>',
            published=True,
        )

        self.faq_cat = FAQCategory.objects.create(name='General')
        self.faq = FAQ.objects.create(
            question='How fast can you start?',
            answer='<p>Usually within 24 to 48 hours.</p>',
            category=self.faq_cat,
            published=True,
        )

        self.testimonial = Testimonial.objects.create(
            client_name='Aarav Mehta',
            role='CTO',
            company='NextGen Solutions',
            testimonial='Code Yari delivered our project ahead of schedule.',
            rating=5,
            published=True,
            featured=True,
        )

    def test_homepage(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Code Yari')
        self.assertContains(response, 'Web Development')

    def test_about_page(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About Us')

    def test_contact_get_and_post(self):
        # GET
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)

        # POST valid
        post_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+91 9999999999',
            'subject': 'Project Inquiry',
            'message': 'We want to build an e-commerce platform.',
        }
        post_res = self.client.post(reverse('core:contact'), data=post_data, follow=True)
        self.assertEqual(post_res.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email='john@example.com').exists())

    def test_privacy_and_terms(self):
        res1 = self.client.get(reverse('core:privacy_policy'))
        self.assertEqual(res1.status_code, 200)
        res2 = self.client.get(reverse('core:terms'))
        self.assertEqual(res2.status_code, 200)

    def test_services_views(self):
        # List
        res1 = self.client.get(reverse('services:list'))
        self.assertEqual(res1.status_code, 200)
        self.assertContains(res1, 'Web Development')

        # Detail
        res2 = self.client.get(reverse('services:detail', kwargs={'slug': 'web-development'}))
        self.assertEqual(res2.status_code, 200)
        self.assertContains(res2, 'Web Development')

    def test_portfolio_views(self):
        # List
        res1 = self.client.get(reverse('portfolio:list'))
        self.assertEqual(res1.status_code, 200)
        self.assertContains(res1, 'SaaS Dashboard')

        # Detail
        res2 = self.client.get(reverse('portfolio:detail', kwargs={'slug': 'saas-dashboard'}))
        self.assertEqual(res2.status_code, 200)
        self.assertContains(res2, 'SaaS Dashboard')

    def test_blog_views(self):
        # List
        res1 = self.client.get(reverse('blog:list'))
        self.assertEqual(res1.status_code, 200)
        self.assertContains(res1, 'Building High-Performing Django Apps')

        # Detail
        res2 = self.client.get(reverse('blog:detail', kwargs={'slug': 'building-high-performing-django-apps'}))
        self.assertEqual(res2.status_code, 200)
        self.assertContains(res2, 'Building High-Performing Django Apps')

    def test_faq_views(self):
        res = self.client.get(reverse('faq:list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'How fast can you start?')

    def test_testimonials_views(self):
        res = self.client.get(reverse('testimonials:list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Aarav Mehta')

    def test_quote_get_and_post(self):
        # GET
        res = self.client.get(reverse('leads:get_quote'))
        self.assertEqual(res.status_code, 200)

        # POST valid
        post_data = {
            'name': 'Client User',
            'email': 'client@example.com',
            'phone': '+91 8888888888',
            'company': 'Tech Corp',
            'service': 'Web Development',
            'budget': '50k-100k',
            'project_type': 'new_build',
            'project_description': 'We need a high-performance custom Django web application for our enterprise.',
            'deadline': 'Next month',
            'preferred_contact': 'whatsapp',
        }
        post_res = self.client.post(reverse('leads:get_quote'), data=post_data, follow=True)
        self.assertEqual(post_res.status_code, 200)
        self.assertTrue(Lead.objects.filter(email='client@example.com').exists())

    def test_sitemap_and_robots(self):
        res1 = self.client.get('/sitemap.xml')
        self.assertEqual(res1.status_code, 200)

        res2 = self.client.get('/robots.txt')
        self.assertEqual(res2.status_code, 200)
        self.assertIn(b'User-agent', res2.content)
