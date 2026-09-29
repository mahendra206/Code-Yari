"""Portfolio views"""
from django.shortcuts import render, get_object_or_404, redirect
from .models import PortfolioProject, PortfolioCategory


from django.db.models import Case, When, Value, IntegerField


def portfolio_list(request):
    category_slug = request.GET.get('category')
    
    # Priority ordering: TeachMANTRA (1), NEXPLAY (2), Houzez (3), ResumeAI (4), other real projects (5), demo projects (6)
    order_priority = Case(
        When(slug__icontains='teachmantra', then=Value(1)),
        When(slug__icontains='nexplay', then=Value(2)),
        When(slug__icontains='houzez', then=Value(3)),
        When(slug__icontains='resume', then=Value(4)),
        When(is_demo=False, then=Value(5)),
        default=Value(6),
        output_field=IntegerField()
    )

    projects = PortfolioProject.objects.filter(published=True).select_related('category').annotate(
        priority=order_priority
    ).order_by('priority', 'created_at')

    categories = PortfolioCategory.objects.all()
    active_category = None

    if category_slug:
        active_category = get_object_or_404(PortfolioCategory, slug=category_slug)
        projects = projects.filter(category=active_category)

    context = {
        'page_title': 'Our Portfolio — Code Yari',
        'meta_description': 'Explore Code Yari\'s portfolio of websites, apps, SEO projects and digital solutions we\'ve built for our clients.',
        'projects': projects,
        'categories': categories,
        'active_category': active_category,
    }
    return render(request, 'portfolio/list.html', context)


import urllib.parse

PROJECT_EXTRAS = {
    'teachmantra-student-academy-test-portal': {
        'badge_text': '✦ Live Production EdTech Platform',
        'tagline': 'A high-speed student academy web portal featuring digital curriculum repositories, live mock tests, and real-time student analytics.',
        'highlight_chips': ['Live Online Mock Tests', 'Downloadable PDF Syllabus', 'Student Analytics', 'Mobile-First Speed 98+'],
        'metrics': [
            {'val': '10,000+', 'label': 'Students Benefited', 'icon': 'bi-people-fill'},
            {'val': '100+', 'label': 'Live Test Series', 'icon': 'bi-journal-check'},
            {'val': '< 1.1s', 'label': 'Page Load Speed', 'icon': 'bi-lightning-charge-fill'},
            {'val': '99.9%', 'label': 'Platform Uptime', 'icon': 'bi-shield-check'},
        ],
        'highlights': [
            {'icon': 'bi-journal-code', 'title': 'Course & Syllabus Repository', 'desc': 'Categorized study modules, exam patterns, and downloadable syllabus PDFs accessible across all devices.'},
            {'icon': 'bi-stopwatch-fill', 'title': 'Live Mock Test Engine', 'desc': 'Timed online examination interface with instant automated result scoring and question-by-question breakdown.'},
            {'icon': 'bi-graph-up-arrow', 'title': 'Performance Analytics', 'desc': 'Visual tracking of student accuracy, time per question, and subject-wise percentile rankings.'},
            {'icon': 'bi-phone-fill', 'title': '100% Mobile Optimized', 'desc': 'Engineered to load in under a second even on 3G/4G connections across rural and urban student networks.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I loved your TeachMANTRA project. I want to build a similar educational platform for my academy.',
    },
    'nexplay-gaming-ecosystem-setup-builder': {
        'badge_text': '✦ Interactive 3D Gaming Hub & Setup Builder',
        'tagline': 'A futuristic, dark-mode gaming ecosystem allowing esports players and PC enthusiasts to configure custom setups with real-time specs.',
        'highlight_chips': ['60 FPS Buttery Animations', 'Custom PC Setup Configurator', 'Dark Gaming Aesthetics', 'Zero Latency Filters'],
        'metrics': [
            {'val': '60 FPS', 'label': 'Fluid Framerate', 'icon': 'bi-speedometer2'},
            {'val': '1,000+', 'label': 'Rig Configurations', 'icon': 'bi-cpu-fill'},
            {'val': '100%', 'label': 'Responsive UI', 'icon': 'bi-controller'},
            {'val': '0-Lag', 'label': 'Instant State Sync', 'icon': 'bi-lightning-fill'},
        ],
        'highlights': [
            {'icon': 'bi-pc-display', 'title': 'Interactive Setup Builder', 'desc': 'Real-time component compatibility checker, wattage calculation, and price estimator for custom gaming rigs.'},
            {'icon': 'bi-palette-fill', 'title': 'Neon Cyberpunk UI Design', 'desc': 'Tailored with glowing purple/cyan accents, glassmorphic cards, and fluid CSS transitions for gamers.'},
            {'icon': 'bi-cart-check-fill', 'title': 'Seamless Checkout Flows', 'desc': 'Frictionless component bundling with one-click cart transfer and instant hardware specs comparison.'},
            {'icon': 'bi-phone', 'title': 'Optimized for Mobile Gamers', 'desc': 'Touch-optimized gestures, swipeable carousels, and responsive card grids for smartphone browsing.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I checked out your NEXPLAY project and want to build a custom interactive web application for my brand.',
    },
    'houzez-luxury-real-estate-property-marketplace': {
        'badge_text': '✦ Luxury Real Estate & Property Portal',
        'tagline': 'A premier property marketplace showcasing prime residential and commercial real estate with interactive filters and virtual tours.',
        'highlight_chips': ['Instant Multi-Filter Search', 'Virtual Tour Ready', 'Direct WhatsApp Inquiries', 'High-Converting Property Cards'],
        'metrics': [
            {'val': '500+', 'label': 'Luxury Listings', 'icon': 'bi-building'},
            {'val': '3.2x', 'label': 'Higher Lead Conversions', 'icon': 'bi-graph-up'},
            {'val': '100%', 'label': 'Verified Properties', 'icon': 'bi-patch-check-fill'},
            {'val': '< 1.2s', 'label': 'High-Res Asset Loading', 'icon': 'bi-lightning-charge-fill'},
        ],
        'highlights': [
            {'icon': 'bi-search-heart-fill', 'title': 'Multi-Parametric Filter Engine', 'desc': 'Filter by budget, BHK configuration, furnishing status, and verified possession dates with 0 latency.'},
            {'icon': 'bi-images', 'title': 'High-Definition Visual Showcase', 'desc': '4K gallery views, floor plan blueprints, and neighborhood amenity maps with interactive icons.'},
            {'icon': 'bi-whatsapp', 'title': 'Instant Agent Connect', 'desc': 'Direct one-tap WhatsApp call and schedule visit flows that turn property browsers into confirmed buyers.'},
            {'icon': 'bi-geo-alt-fill', 'title': 'Interactive Location Mapping', 'desc': 'Distance calculation to schools, metro stations, and hospitals integrated into property details.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I saw your Houzez Real Estate project. I want to build a modern property portal for my real estate firm.',
    },
    'resumeai-ai-resume-builder-ats-studio': {
        'badge_text': '✦ Next-Gen AI Resume & ATS Studio',
        'tagline': 'An intelligent, browser-based resume builder powered by AI suggestions that guarantees 95+ ATS pass rates and one-click PDF export.',
        'highlight_chips': ['ATS 95+ Score Target', 'Instant Vector PDF Export', 'Smart Keyword Matching', 'Modern Clean Templates'],
        'metrics': [
            {'val': '95%+', 'label': 'ATS Pass Rate Target', 'icon': 'bi-award-fill'},
            {'val': '1-Click', 'label': 'Crisp Vector PDF Export', 'icon': 'bi-file-earmark-pdf-fill'},
            {'val': '10x', 'label': 'Faster Resume Creation', 'icon': 'bi-lightning-fill'},
            {'val': '100%', 'label': 'Browser Privacy First', 'icon': 'bi-shield-lock-fill'},
        ],
        'highlights': [
            {'icon': 'bi-robot', 'title': 'AI Role-Specific Bullet Suggestions', 'desc': 'Generates tailored accomplishment statements for software engineers, product managers, marketers, and more.'},
            {'icon': 'bi-file-earmark-pdf', 'title': 'Zero-Lag PDF Generation', 'desc': 'Client-side vector PDF rendering with html2pdf.js ensuring pixel-perfect printable typography without server latency.'},
            {'icon': 'bi-layout-text-window', 'title': 'Recruiter-Approved Formats', 'desc': 'Single-column and two-column clean architectures designed specifically to parse seamlessly through Taleo & Workday.'},
            {'icon': 'bi-device-ssd', 'title': 'Local Storage Autosave', 'desc': 'Your resume data is automatically preserved in your browser cache so you never lose work between sessions.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I checked out your ResumeAI project and want to build an AI tool or web app for my business.',
    },
    'saas-dashboard-design-demo': {
        'badge_text': '✦ Enterprise SaaS Analytics & CRM Dashboard',
        'tagline': 'A high-converting B2B SaaS dashboard interface built with modular design systems, dark/light themes, and real-time telemetry metrics.',
        'highlight_chips': ['Interactive Data Visualizations', 'Role-Based Access Control', 'Multi-Tenant Architecture', 'REST & GraphQL APIs'],
        'metrics': [
            {'val': '99.99%', 'label': 'SLA Guaranteed', 'icon': 'bi-shield-check'},
            {'val': '10x', 'label': 'Data Rendering Speed', 'icon': 'bi-lightning-charge-fill'},
            {'val': '50+', 'label': 'Reusable Components', 'icon': 'bi-grid-1x2-fill'},
            {'val': '256-bit', 'label': 'End-to-End Encryption', 'icon': 'bi-lock-fill'},
        ],
        'highlights': [
            {'icon': 'bi-bar-chart-line-fill', 'title': 'Real-Time Telemetry & Charts', 'desc': 'Interactive analytics widgets powered by Chart.js & D3 with customizable date ranges and CSV export.'},
            {'icon': 'bi-sliders', 'title': 'Design Token Architecture', 'desc': 'Built on scalable CSS design tokens allowing 1-click white-label theming for enterprise clients.'},
            {'icon': 'bi-people-fill', 'title': 'Multi-Tenant Team Workspaces', 'desc': 'Granular permissions, invite flows, and audit logs structured for SOC-2 compliance readiness.'},
            {'icon': 'bi-phone', 'title': 'Cross-Platform Responsive', 'desc': 'Seamless navigation across tablet, mobile executive views, and ultra-wide monitoring dashboards.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I checked out your SaaS Dashboard demo and want to develop a custom SaaS web app.',
    },
    'local-business-seo-campaign-demo': {
        'badge_text': '✦ High-Impact Local SEO & Growth Strategy',
        'tagline': 'An end-to-end local SEO blueprint that drove 340% increase in qualified inbound leads, #1 Google Map Pack rankings, and 5-star review velocity.',
        'highlight_chips': ['Top 3 Map Pack Rankings', '340% Organic Traffic Surge', 'Hyperlocal Schema Markup', 'Core Web Vitals 99+'],
        'metrics': [
            {'val': '#1', 'label': 'Google Map Pack Rank', 'icon': 'bi-geo-alt-fill'},
            {'val': '+340%', 'label': 'Inbound Calls & Leads', 'icon': 'bi-telephone-fill'},
            {'val': '99/100', 'label': 'Google PageSpeed Score', 'icon': 'bi-lightning-fill'},
            {'val': '4.9★', 'label': 'Review Rating Velocity', 'icon': 'bi-star-fill'},
        ],
        'highlights': [
            {'icon': 'bi-google', 'title': 'Google Business Profile Domination', 'desc': 'Complete profile optimization, geotagged media uploads, and high-converting service listing architecture.'},
            {'icon': 'bi-diagram-3-fill', 'title': 'Hyperlocal Schema & Citations', 'desc': 'LocalBusiness JSON-LD markup and 100+ consistent citations across major directories and aggregators.'},
            {'icon': 'bi-speedometer', 'title': 'Core Web Vitals Overhaul', 'desc': 'Speed optimization reducing Time to First Byte (TTFB) to under 200ms and eliminating layout shifts.'},
            {'icon': 'bi-funnel-fill', 'title': 'Conversion Rate Optimization (CRO)', 'desc': 'Direct click-to-call buttons and localized landing page copy that turns searchers into paying clients.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I saw your Local SEO Case Study and want to rank my local business on Google #1.',
    },
}


def _get_fallback_project_extras(project):
    """Dynamic extras for any project."""
    cat_name = project.category.name if project.category else 'Digital Solution'
    return {
        'badge_text': f'✦ Verified {cat_name} Project',
        'tagline': project.short_description or f'A bespoke {cat_name} engineered by Code Yari with clean architecture and high performance.',
        'highlight_chips': [cat_name, '100% Responsive', 'Clean Architecture', 'Tailor-Made UI'],
        'metrics': [
            {'val': '100%', 'label': 'Custom Codebase', 'icon': 'bi-code-slash'},
            {'val': 'Fast', 'label': 'High-Speed Stack', 'icon': 'bi-lightning-charge-fill'},
            {'val': '4.9★', 'label': 'Quality Rating', 'icon': 'bi-star-fill'},
            {'val': '24/7', 'label': 'Ongoing Support', 'icon': 'bi-shield-check'},
        ],
        'highlights': [
            {'icon': 'bi-layers-fill', 'title': 'Bespoke Architecture', 'desc': 'Clean, modular, and maintainable codebase engineered for long-term scalability.'},
            {'icon': 'bi-speedometer2', 'title': 'Blazing Fast Performance', 'desc': 'Optimized Core Web Vitals, compressed assets, and instantaneous page load times.'},
            {'icon': 'bi-shield-check', 'title': 'Secure & Tested', 'desc': 'Thorough cross-device quality assurance, browser compatibility, and security auditing.'},
            {'icon': 'bi-phone', 'title': 'Mobile-First Excellence', 'desc': 'Fluid responsive layouts that look breath-taking on smartphones, tablets, and 4K displays.'},
        ],
        'whatsapp_msg': f'Hi Code Yari! I saw your {project.name} project and want to discuss a similar solution for my business.',
    }


def portfolio_detail(request, slug):
    project = get_object_or_404(PortfolioProject, slug=slug, published=True)
    gallery = project.gallery_images.all()
    related = PortfolioProject.objects.filter(
        published=True
    ).exclude(pk=project.pk).order_by('?')[:3]

    extras = PROJECT_EXTRAS.get(project.slug, _get_fallback_project_extras(project))
    whatsapp_encoded = urllib.parse.quote(extras.get('whatsapp_msg', f'Hi Code Yari! I want to discuss {project.name}.'))

    context = {
        'page_title': project.get_seo_title(),
        'meta_description': project.get_seo_description(),
        'project': project,
        'gallery': gallery,
        'related_projects': related,
        'technologies': project.technologies if isinstance(project.technologies, list) else [],
        'extras': extras,
        'whatsapp_encoded': whatsapp_encoded,
    }
    return render(request, 'portfolio/detail.html', context)


def case_studies_view(request):
    """Case Studies page is now merged into portfolio showcase. Redirect to unified portfolio list."""
    return redirect('portfolio:list', permanent=True)


