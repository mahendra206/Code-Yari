"""
Management command: seed_demo_data
Creates clearly-labeled demo content for development/testing.
Run: python manage.py seed_demo_data
Remove: python manage.py clear_demo_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from apps.core.models import SiteSettings, StatItem, TeamMember
from apps.services.models import Service
from apps.portfolio.models import PortfolioCategory, PortfolioProject
from apps.testimonials.models import Testimonial
from apps.blog.models import BlogCategory, BlogPost
from apps.faq.models import FAQCategory, FAQ


class Command(BaseCommand):
    help = 'Seed the database with demo data (clearly labeled as demo content)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding demo data...'))
        self._seed_site_settings()
        self._seed_stats()
        self._seed_team()
        self._seed_services()
        self._seed_portfolio()
        self._seed_testimonials()
        self._seed_blog()
        self._seed_faq()
        self.stdout.write(self.style.SUCCESS('\n[OK] Demo data seeded successfully!'))
        self.stdout.write(self.style.WARNING(
            '\nNOTE: All demo content is labeled as demo. '
            'Remove with: python manage.py clear_demo_data'
        ))

    def _seed_site_settings(self):
        settings, _ = SiteSettings.objects.get_or_create(pk=1)
        settings.site_name = 'Code Yari'
        settings.tagline = 'Code. Create. Grow.'
        settings.alt_tagline = 'Sirf code nahi, Yari ke saath solution.'
        settings.email = 'hello@codeyari.com'
        settings.phone = '+91 98765 43210'
        settings.whatsapp = '919876543210'
        settings.address = 'India'
        settings.business_hours = 'Mon–Sat, 10AM–7PM IST'
        settings.meta_description = 'Code Yari — A young digital technology team providing websites, apps, SEO, digital marketing, UI/UX, AI and automation solutions.'
        settings.save()
        self.stdout.write('  [OK] Site settings')

    def _seed_stats(self):
        StatItem.objects.all().delete()
        stats = [
            ('Projects Delivered', '20+', 'bi-check-circle', '(Demo Data)', 1),
            ('Happy Clients', '15+', 'bi-people', '(Demo Data)', 2),
            ('Technologies', '10+', 'bi-code-slash', '', 3),
            ('Years Building', '2+', 'bi-calendar', '(Demo Data)', 4),
        ]
        for label, value, icon, note, order in stats:
            StatItem.objects.create(label=label, value=value, icon=icon, note=note, order=order)
        self.stdout.write('  [OK] Stats')

    def _seed_team(self):
        TeamMember.objects.all().delete()
        members = [
            ('Alex Kumar', 'Full Stack Developer', 'Django & React specialist with a passion for clean code.', 1),
            ('Priya Sharma', 'UI/UX Designer', 'Creates beautiful, user-centered digital experiences.', 2),
            ('Rahul Singh', 'SEO & Digital Marketing', 'Helps businesses grow their online presence organically.', 3),
            ('Neha Patel', 'Mobile App Developer', 'Flutter and React Native developer building cross-platform apps.', 4),
        ]
        for name, role, bio, order in members:
            TeamMember.objects.create(name=name, role=role, bio=bio, order=order)
        self.stdout.write('  [OK] Team members (demo)')

    def _seed_services(self):
        Service.objects.all().delete()
        services_data = [
            {
                'name': 'Web Development',
                'icon': 'bi-code-slash',
                'short_description': 'Custom, responsive websites built with modern technologies for performance and user experience.',
                'full_description': '<p>We build fully custom websites tailored to your business needs. From landing pages to complex web applications, we use the latest technologies to deliver fast, secure, and scalable solutions.</p><p>Our web development process starts with understanding your goals, then designing and building a solution that drives results.</p>',
                'features': ['Responsive Design', 'SEO-Optimized', 'Fast Loading', 'Secure & Scalable', 'CMS Integration', 'Custom Admin Panel'],
                'technologies': ['Django', 'Python', 'HTML5', 'CSS3', 'JavaScript', 'Bootstrap', 'PostgreSQL'],
                'is_featured': True, 'order': 1,
            },
            {
                'name': 'App Development',
                'icon': 'bi-phone',
                'short_description': 'Cross-platform mobile apps for iOS and Android using Flutter and React Native.',
                'full_description': '<p>We develop high-quality mobile applications that work beautifully on both iOS and Android. Our apps are built with performance and user experience as top priorities.</p>',
                'features': ['iOS & Android', 'Offline Support', 'Push Notifications', 'API Integration', 'App Store Deployment'],
                'technologies': ['Flutter', 'React Native', 'Firebase', 'REST API'],
                'is_featured': True, 'order': 2,
            },
            {
                'name': 'SEO & Google Ranking',
                'icon': 'bi-search',
                'short_description': 'Data-driven SEO strategies to improve your Google rankings and drive organic traffic.',
                'full_description': '<p>We help businesses rank higher on Google through comprehensive SEO audits, on-page optimization, content strategy, link building, and technical SEO improvements.</p>',
                'features': ['Technical SEO Audit', 'On-Page Optimization', 'Keyword Research', 'Content Strategy', 'Link Building', 'Monthly Reports'],
                'technologies': ['Google Search Console', 'Google Analytics', 'SEMrush', 'Ahrefs'],
                'is_featured': True, 'order': 3,
            },
            {
                'name': 'Digital Marketing',
                'icon': 'bi-megaphone',
                'short_description': 'Result-driven digital marketing campaigns across Google Ads, social media, and email.',
                'full_description': '<p>We create and manage digital marketing campaigns that deliver measurable results. From Google Ads to social media marketing, we help you reach your target audience and convert them into customers.</p>',
                'features': ['Google Ads Management', 'Social Media Marketing', 'Email Campaigns', 'Analytics & Reporting', 'Conversion Optimization'],
                'technologies': ['Google Ads', 'Meta Ads', 'Mailchimp', 'Google Analytics'],
                'is_featured': True, 'order': 4,
            },
            {
                'name': 'UI/UX Design',
                'icon': 'bi-palette',
                'short_description': 'Beautiful, intuitive designs that delight users and drive business results.',
                'full_description': '<p>We design user interfaces that are not just visually appealing but also highly functional and intuitive. Our UX research and design process ensures your users love using your product.</p>',
                'features': ['User Research', 'Wireframing', 'Prototyping', 'UI Design', 'Design Systems', 'Figma Handoff'],
                'technologies': ['Figma', 'Adobe XD', 'Illustrator', 'Photoshop'],
                'is_featured': True, 'order': 5,
            },
            {
                'name': 'AI & Automation',
                'icon': 'bi-robot',
                'short_description': 'AI-powered tools and automation solutions to save time and scale your business.',
                'full_description': '<p>We integrate AI capabilities and automation workflows into your business processes. From chatbots to data analysis to workflow automation, we help you work smarter.</p>',
                'features': ['AI Chatbots', 'Process Automation', 'Data Analysis', 'API Integrations', 'Custom AI Solutions'],
                'technologies': ['Python', 'OpenAI API', 'LangChain', 'n8n', 'Zapier'],
                'is_featured': True, 'order': 6,
            },
            {
                'name': 'E-Commerce Development',
                'icon': 'bi-bag',
                'short_description': 'Feature-rich online stores with payment integration, inventory management, and more.',
                'full_description': '<p>We build powerful e-commerce platforms that help you sell online effectively. From product management to payment gateways, we handle everything you need to run a successful online store.</p>',
                'features': ['Product Management', 'Payment Gateways', 'Inventory System', 'Order Management', 'Mobile Shopping'],
                'technologies': ['Django', 'Razorpay', 'Stripe', 'WooCommerce'],
                'is_featured': False, 'order': 7,
            },
            {
                'name': 'Website Maintenance',
                'icon': 'bi-tools',
                'short_description': 'Ongoing support, updates, security patches, and performance monitoring for your website.',
                'full_description': '<p>Keep your website running smoothly with our maintenance services. We handle updates, security monitoring, backups, performance optimization, and content updates.</p>',
                'features': ['Regular Backups', 'Security Monitoring', 'Performance Checks', 'Content Updates', 'Bug Fixes', 'Monthly Reports'],
                'technologies': ['Linux', 'Nginx', 'Python', 'Django'],
                'is_featured': False, 'order': 8,
            },
            {
                'name': 'Hosting & Deployment',
                'icon': 'bi-cloud-upload',
                'short_description': 'Reliable hosting setup and deployment on cloud platforms for maximum uptime.',
                'full_description': '<p>We set up and configure hosting environments optimized for your application. From shared hosting to dedicated cloud servers, we ensure your website is fast, secure, and always online.</p>',
                'features': ['Cloud Setup', 'SSL Certificate', 'Domain Configuration', 'CI/CD Pipeline', '99.9% Uptime'],
                'technologies': ['AWS', 'Google Cloud', 'DigitalOcean', 'Nginx', 'Docker'],
                'is_featured': False, 'order': 9,
            },
            {
                'name': 'Custom Software Development',
                'icon': 'bi-gear',
                'short_description': 'Bespoke software solutions tailored to your unique business requirements.',
                'full_description': '<p>When off-the-shelf software doesn\'t cut it, we build custom solutions designed specifically for your business. We analyze your requirements and build exactly what you need.</p>',
                'features': ['Custom Development', 'API Development', 'Database Design', 'Third-party Integrations', 'Documentation'],
                'technologies': ['Python', 'Django', 'REST API', 'PostgreSQL', 'Redis'],
                'is_featured': False, 'order': 10,
            },
            {
                'name': 'Website Speed Optimization',
                'icon': 'bi-lightning',
                'short_description': 'Boost your website performance, Core Web Vitals, and PageSpeed scores significantly.',
                'full_description': '<p>A slow website loses visitors and rankings. We audit and optimize your website to load fast on all devices, improving user experience and search engine rankings.</p>',
                'features': ['Performance Audit', 'Image Optimization', 'Caching Setup', 'Code Minification', 'CDN Integration', 'Core Web Vitals'],
                'technologies': ['Google PageSpeed', 'GTmetrix', 'Cloudflare', 'WebP'],
                'is_featured': False, 'order': 11,
            },
            {
                'name': 'Content & SEO Writing',
                'icon': 'bi-pencil',
                'short_description': 'SEO-optimized content that engages your audience and ranks on search engines.',
                'full_description': '<p>Quality content is the foundation of good SEO. We create engaging, well-researched, SEO-optimized content that connects with your audience and drives organic traffic.</p>',
                'features': ['Keyword Research', 'Blog Articles', 'Website Copy', 'Meta Descriptions', 'Content Calendar'],
                'technologies': ['Surfer SEO', 'SEMrush', 'Google Search Console'],
                'is_featured': False, 'order': 12,
            },
        ]
        for data in services_data:
            Service.objects.create(is_active=True, **data)
        self.stdout.write('  [OK] Services (12)')

    def _seed_portfolio(self):
        PortfolioProject.objects.all().delete()
        PortfolioCategory.objects.all().delete()

        cats = {}
        for name, slug in [('Web Development', 'web'), ('Mobile App', 'app'), ('SEO', 'seo'), ('UI/UX Design', 'design'), ('E-Commerce', 'ecommerce')]:
            cat = PortfolioCategory.objects.create(name=name, slug=slug)
            cats[slug] = cat

        projects = [
            {
                'name': 'TeachMANTRA — Student Academy & Test Portal',
                'category': cats['web'],
                'short_description': 'A comprehensive online learning academy portal featuring course syllabus downloads, live mock tests, student registration, and certificate verification.',
                'full_description': '<p><strong>TeachMANTRA</strong> is a premier student academy web platform engineered to empower learners with structured exam preparation, course catalogs, and interactive assessment tools.</p><h4>Project Highlights:</h4><ul><li><strong>Digital Course & Syllabus Repository:</strong> Direct access to syllabus PDFs, curriculum modules, and revision notes.</li><li><strong>Live Online Mock Test Portal:</strong> Timed practice tests with real-time score calculation, answer keys, and All-India performance benchmarking.</li><li><strong>Certificate Verification Engine:</strong> Fast, verifiable credential lookup system for student academy certificates.</li><li><strong>Adaptive Theme & UI:</strong> Dark and light mode toggle with smooth transition and mobile-first responsiveness.</li></ul>',
                'technologies': ['Python', 'Django', 'JavaScript', 'HTML5', 'CSS3', 'FontAwesome', 'Bootstrap'],
                'project_url': 'https://www.theteachmantra.com/',
                'featured': True, 'is_demo': False, 'published': True,
            },
            {
                'name': 'NEXPLAY — Gaming Ecosystem & Setup Builder',
                'category': cats['web'],
                'short_description': 'An interactive gaming ecosystem and custom PC setup builder featuring personalized playstyle recommendations, hardware configurations, and esports peripherals.',
                'full_description': '<p><strong>NEXPLAY</strong> is a high-performance web platform and gaming ecosystem engineered for gamers, streamers, and esports enthusiasts to design, configure, and customize their dream battle stations.</p><h4>Project Highlights:</h4><ul><li><strong>Interactive Setup Builder:</strong> Modular hardware selector for custom PC rigs, high-refresh displays, and ergonomic gaming furniture.</li><li><strong>Personalized Playstyle Engine:</strong> Dynamic gear recommendations based on game genres (FPS, MOBA, RPG, Simulator) and competitive requirements.</li><li><strong>Esports Peripheral Catalog:</strong> Filterable catalog of pro-grade mechanical keyboards, mice, audio gear, and streaming equipment.</li><li><strong>Cyberpunk Modern UI:</strong> Sleek dark-mode aesthetic with reactive animations, neon accents, and smooth scroll navigation.</li></ul>',
                'technologies': ['React', 'Vite', 'TailwindCSS', 'JavaScript', 'Netlify', 'HTML5', 'CSS3'],
                'project_url': 'https://nexplay-hub.netlify.app/',
                'featured': True, 'is_demo': False, 'published': True,
            },
            {
                'name': 'Houzez — Luxury Real Estate & Property Marketplace',
                'category': cats['web'],
                'short_description': 'A modern real estate marketplace platform featuring luxury property listings for sale & rent, interactive filter search, realtor directories, and listing inquiries.',
                'full_description': '<p><strong>Houzez</strong> is a premium real estate and property marketplace application designed for luxury homebuyers, investors, and licensed realtors to browse, list, and connect effortlessly.</p><h4>Project Highlights:</h4><ul><li><strong>Advanced Property Search & Filter:</strong> Filter luxury homes, villas, apartments by status (For Sale / For Rent), price range, bedrooms, and location.</li><li><strong>Detailed Property Showcase:</strong> High-resolution media galleries, floor plans, amenity checklists, and neighborhood mapping.</li><li><strong>Realtor & Agent Directory:</strong> Verified broker profiles, direct contact channels, and portfolio showcase.</li><li><strong>Inquiry & Lead Capture:</strong> Streamlined scheduling for property walkthroughs and automated seller inquiry forms.</li></ul>',
                'technologies': ['React', 'JavaScript', 'TailwindCSS', 'HTML5', 'CSS3', 'Netlify'],
                'project_url': 'https://houzez-1.netlify.app/',
                'featured': True, 'is_demo': False, 'published': True,
            },
            {
                'name': 'Restaurant Landing Page (Demo)',
                'category': cats['web'],
                'short_description': 'Modern restaurant website with online menu, reservation system, and Google Maps integration.',
                'full_description': '<p><strong>⚠️ Demo project.</strong></p><p>Beautiful restaurant website with animated menu, table booking form, gallery, and social media integration.</p>',
                'technologies': ['HTML5', 'CSS3', 'JavaScript', 'Google Maps API'],
                'featured': False, 'is_demo': True, 'published': True,
            },
            {
                'name': 'Local Business SEO Campaign (Demo)',
                'category': cats['seo'],
                'short_description': 'SEO strategy and implementation for a local service business.',
                'full_description': '<p><strong>⚠️ Demo project showing our SEO process.</strong></p><p>Comprehensive SEO audit, on-page optimization, local citations, and content strategy implementation.</p>',
                'technologies': ['Google Search Console', 'Ahrefs', 'SEMrush'],
                'featured': False, 'is_demo': True, 'published': True,
            },
            {
                'name': 'SaaS Dashboard Design (Demo)',
                'category': cats['design'],
                'short_description': 'Clean, data-rich dashboard UI for a SaaS analytics platform.',
                'full_description': '<p><strong>⚠️ Demo project.</strong></p><p>Figma-based dashboard design with data visualization components, dark mode, and component library.</p>',
                'technologies': ['Figma', 'Adobe Illustrator'],
                'featured': False, 'is_demo': True, 'published': True,
            },
        ]
        for p in projects:
            PortfolioProject.objects.create(**p)
        self.stdout.write('  [OK] Portfolio projects (demo, clearly labeled)')

    def _seed_testimonials(self):
        Testimonial.objects.all().delete()
        items = [
            ('Amit Verma', 'StartupX', 'Founder', 'Code Yari built our MVP in record time. The team was professional, communicative, and delivered exactly what we needed. Highly recommended!', 5),
            ('Pooja Mehta', 'Bloom Boutique', 'Owner', 'Our e-commerce site looks amazing and sales have improved since launch. The team understood our vision perfectly.', 5),
            ('Ravi Sharma', 'TechConsult India', 'CEO', 'Their SEO work has significantly improved our search rankings. We\'re getting more qualified leads every month.', 4),
            ('Deepika Nair', 'Fresh Foods Co.', 'Marketing Head', 'The digital marketing campaigns they set up have been a game-changer for our brand awareness and online sales.', 5),
            ('Karan Patel', 'EduReach NGO', 'Director', 'Professional, affordable, and reliable. They\'re our go-to team for all things digital.', 5),
            ('Sunita Joshi', 'Wellness Studio', 'Founder', 'The app they designed is beautiful and my clients love using it to book sessions. 10/10 experience!', 5),
        ]
        for i, (name, company, role, text, rating) in enumerate(items):
            Testimonial.objects.create(
                client_name=name, company=company, role=role,
                testimonial=text, rating=rating,
                featured=(i < 3), published=True, is_demo=True, order=i
            )
        self.stdout.write('  [OK] Testimonials (demo, clearly labeled)')

    def _seed_blog(self):
        BlogPost.objects.all().delete()
        BlogCategory.objects.all().delete()

        # Get or create a superuser for author
        author = User.objects.filter(is_superuser=True).first()

        cats = {}
        for name, slug in [('Web Development', 'web-development'), ('SEO & Marketing', 'seo-marketing'), ('Tech Tips', 'tech-tips')]:
            cat = BlogCategory.objects.create(name=name, slug=slug)
            cats[slug] = cat

        posts = [
            {
                'title': '10 Reasons Why Your Business Needs a Professional Website in 2025',
                'slug': '10-reasons-business-needs-professional-website-2025',
                'excerpt': 'In today\'s digital-first world, a professional website isn\'t optional — it\'s essential. Here\'s why your business can\'t afford to go without one.',
                'content': '<p>In today\'s competitive digital landscape, having a professional website is no longer a luxury — it\'s a business necessity.</p><h2>1. First Impressions Matter</h2><p>Your website is often the first point of contact between your business and potential customers. A professionally designed website builds instant trust and credibility.</p><h2>2. Available 24/7</h2><p>Unlike a physical store, your website works for you around the clock, allowing customers to learn about your products and services at any time.</p><h2>3. Reach a Wider Audience</h2><p>A website removes geographical barriers, allowing you to reach customers beyond your local area.</p><h2>4. Build Credibility</h2><p>Studies show that 75% of people judge a company\'s credibility based on their website design.</p><h2>5. Cost-Effective Marketing</h2><p>Compared to traditional advertising, a website is one of the most cost-effective marketing tools available.</p><p>Ready to get your professional website? <a href="/get-a-quote/">Get a free quote from Code Yari today!</a></p>',
                'category': cats['web-development'],
                'tags': 'Web Development, Business, Digital Presence',
                'published': True,
                'seo_title': '10 Reasons Your Business Needs a Website — Code Yari Blog',
                'seo_description': 'Discover the top 10 reasons why every business needs a professional website in 2025. Build credibility, reach more customers, and grow online.',
            },
            {
                'title': 'Beginner\'s Guide to SEO: How to Rank Higher on Google',
                'slug': 'beginners-guide-seo-rank-higher-google',
                'excerpt': 'A step-by-step guide to understanding SEO fundamentals and improving your website\'s Google rankings organically.',
                'content': '<p>Search Engine Optimization (SEO) is the practice of improving your website to increase visibility in search engine results. Here\'s everything you need to know to get started.</p><h2>What is SEO?</h2><p>SEO is the process of optimizing your website and content so that search engines like Google can find it, understand it, and rank it for relevant search queries.</p><h2>On-Page SEO</h2><p>On-page SEO involves optimizing individual web pages, including title tags, meta descriptions, headings, content, and image alt text.</p><h2>Technical SEO</h2><p>Technical SEO ensures your website meets the technical requirements of search engines — fast loading, mobile-friendly, secure (HTTPS), and properly structured.</p><h2>Off-Page SEO</h2><p>Off-page SEO refers to actions taken outside your own website to impact your rankings, primarily through building backlinks from other reputable sites.</p><h2>Getting Started</h2><p>Start with keyword research to understand what your audience is searching for, then create high-quality content that answers their questions.</p>',
                'category': cats['seo-marketing'],
                'tags': 'SEO, Google, Digital Marketing, Organic Traffic',
                'published': True,
                'seo_title': 'Beginner\'s Guide to SEO — Rank Higher on Google | Code Yari',
                'seo_description': 'Learn the fundamentals of SEO with this beginner-friendly guide. Understand on-page, technical, and off-page SEO to improve your Google rankings.',
            },
            {
                'title': 'Why Django is the Best Framework for Building Your Business Website',
                'slug': 'why-django-best-framework-business-website',
                'excerpt': 'Django\'s "batteries included" philosophy, security features, and scalability make it an excellent choice for building production-ready business websites.',
                'content': '<p>Choosing the right web framework for your business website is crucial. Django, a Python-based web framework, has been powering some of the world\'s largest websites for good reason.</p><h2>What is Django?</h2><p>Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the "batteries included" philosophy.</p><h2>Security</h2><p>Django provides built-in protection against common security vulnerabilities including SQL injection, XSS, CSRF, and clickjacking.</p><h2>Scalability</h2><p>Django has been proven to scale — Instagram, Pinterest, and Disqus all use Django to handle millions of users.</p><h2>Admin Panel</h2><p>Django comes with a powerful, customizable admin panel that allows you to manage your website content without writing code.</p><h2>SEO-Friendly</h2><p>Django\'s clean URL structure and templating system make it easy to build SEO-optimized websites.</p>',
                'category': cats['web-development'],
                'tags': 'Django, Python, Web Development, Backend',
                'published': True,
                'seo_title': 'Why Django is Best for Business Websites — Code Yari Blog',
                'seo_description': 'Learn why Django is the best Python framework for building secure, scalable, and SEO-friendly business websites.',
            },
        ]
        for p_data in posts:
            post = BlogPost(**p_data)
            post.author = author
            post.published_date = timezone.now()
            post.save()
        self.stdout.write('  [OK] Blog posts (3 demo articles)')

    def _seed_faq(self):
        FAQ.objects.all().delete()
        FAQCategory.objects.all().delete()

        cats = {}
        for name in ['General', 'Pricing', 'Process', 'Technical']:
            cat = FAQCategory.objects.create(name=name, order=list('General Pricing Process Technical'.split()).index(name))
            cats[name] = cat

        faqs = [
            ('General', 'What services does Code Yari offer?', 'Code Yari offers a wide range of digital services including web development, mobile app development, SEO, digital marketing, UI/UX design, AI & automation, e-commerce development, website maintenance, hosting & deployment, custom software, website speed optimization, and content writing.', 1),
            ('General', 'How do I get started with Code Yari?', 'Simply fill out our "Get a Quote" form or send us an email at hello@codeyari.com. Tell us about your project and we\'ll get back to you within 24 hours to discuss your requirements.', 2),
            ('General', 'Do you work with clients outside India?', 'Yes! We work with clients globally. Our team communicates effectively in English and can schedule meetings across different time zones.', 3),
            ('Pricing', 'How much does a website cost?', 'Website costs vary based on complexity, features, and requirements. A simple landing page might start from ₹10,000, while a complex web application could be ₹1,00,000+. Contact us for a free quote tailored to your specific needs.', 1),
            ('Pricing', 'Do you offer payment plans?', 'Yes, we typically work with a payment structure of 50% upfront and 50% on delivery. For larger projects, we can discuss milestone-based payment plans.', 2),
            ('Pricing', 'What is included in your website maintenance packages?', 'Our maintenance packages typically include regular backups, security updates, performance monitoring, minor content updates, and monthly progress reports. Contact us for specific package details.', 3),
            ('Process', 'How long does it take to build a website?', 'Timeline varies by project complexity. A simple website might take 1–2 weeks, while a complex web application could take 2–3 months. We\'ll give you a clear timeline during our initial consultation.', 1),
            ('Process', 'Will I be able to update my website myself?', 'Absolutely! We build websites with easy-to-use content management systems (CMS) and provide training so you can manage your content independently.', 2),
            ('Process', 'What information do you need to start a project?', 'We typically need: your business goals, target audience, design preferences (examples you like), content (text, images), and budget. Don\'t worry if you don\'t have everything — we can guide you.', 3),
            ('Technical', 'What technologies do you use?', 'We use modern, proven technologies: Django (Python) for web backends, Flutter/React Native for mobile apps, Bootstrap + custom CSS for frontend, PostgreSQL/MySQL for databases, and cloud platforms like AWS/GCP for hosting.', 1),
            ('Technical', 'Will my website be mobile-friendly?', 'Yes, absolutely. All websites we build are fully responsive and work beautifully on desktop, tablet, and mobile devices.', 2),
            ('Technical', 'Do you provide SEO with every website?', 'We implement basic SEO best practices (proper HTML structure, meta tags, fast loading, etc.) for all websites. Advanced SEO campaigns are offered as a separate service.', 3),
        ]
        for cat_name, question, answer, order in faqs:
            FAQ.objects.create(
                question=question, answer=answer,
                category=cats[cat_name], order=order, published=True
            )
        self.stdout.write('  [OK] FAQs (12 items)')
