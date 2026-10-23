"""Portfolio views"""
from django.shortcuts import render, get_object_or_404, redirect
from .models import PortfolioProject, PortfolioCategory


from django.db.models import Case, When, Value, IntegerField


def portfolio_list(request):
    category_slug = request.GET.get('category')
    
    # Priority ordering: TeachMANTRA (1), NEXPLAY (2), Houzez (3), MediCare Plus (4), Royal Grand (5), Royal Bites (6), Bright Future Academy (7), other real projects (8), demo projects (9)
    order_priority = Case(
        When(slug__icontains='teachmantra', then=Value(1)),
        When(slug__icontains='nexplay', then=Value(2)),
        When(slug__icontains='houzez', then=Value(3)),
        When(slug__icontains='medicare', then=Value(4)),
        When(slug__icontains='royal-grand', then=Value(5)),
        When(slug__icontains='royal-bites', then=Value(6)),
        When(slug__icontains='bright-future', then=Value(7)),
        When(is_demo=False, then=Value(8)),
        default=Value(9),
        output_field=IntegerField()
    )

    projects = PortfolioProject.objects.filter(published=True).select_related('category').annotate(
        priority=order_priority
    ).order_by('priority', 'created_at')

    if not projects.exists():
        from apps.core.auto_seed import ensure_initial_data
        ensure_initial_data()
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
    'medicare-plus-healthcare-hospital-portal': {
        'badge_text': '✦ NABH Accredited Healthcare & Hospital Platform',
        'tagline': 'A modern, responsive healthcare and hospital digital portal featuring 24/7 emergency response, specialist doctor directories, departmental services, and instant appointment booking.',
        'highlight_chips': ['24/7 Emergency Care', 'Specialist Doctor Directory', 'One-Click Appointment Booking', 'NABH Quality Standards'],
        'metrics': [
            {'val': '50+', 'label': 'Expert Doctors & Specialists', 'icon': 'bi-person-badge-fill'},
            {'val': '24/7', 'label': 'Emergency Response', 'icon': 'bi-heart-pulse-fill'},
            {'val': '99.8%', 'label': 'Patient Satisfaction', 'icon': 'bi-patch-check-fill'},
            {'val': '< 0.9s', 'label': 'Mobile Booking Speed', 'icon': 'bi-lightning-charge-fill'},
        ],
        'highlights': [
            {'icon': 'bi-calendar2-plus-fill', 'title': 'Streamlined Doctor Appointments', 'desc': 'Select consultation specialty, date, and preferred time slot with instant digital confirmation.'},
            {'icon': 'bi-hospital-fill', 'title': 'Multi-Specialty Clinical Departments', 'desc': 'Comprehensive guides for Cardiology, Pediatrics, Neurology, Orthopedics, and Diagnostics.'},
            {'icon': 'bi-telephone-inbound-fill', 'title': 'Immediate Emergency Helpline', 'desc': 'Direct one-tap ambulance dispatch and emergency triage desk connect for acute patient care.'},
            {'icon': 'bi-geo-alt-fill', 'title': 'Kanpur Healthcare Accessibility', 'desc': 'Integrated campus navigation, OPD timings, visiting hours, and cashless insurance panels.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I saw your MediCare Plus Hospital project. I want to build a modern healthcare website/portal for my clinic or hospital.',
    },
    'royal-grand-luxury-hotel-suites': {
        'badge_text': '✦ 5-Star Luxury Hospitality Platform',
        'tagline': 'An opulent, high-converting digital portal for Royal Grand Luxury Hotel & Suites featuring virtual room tours, fine dining showcases, and seamless concierge reservations.',
        'highlight_chips': ['Direct Suite Booking Flow', '360° Luxury Walkthrough', 'Michelin-Grade Dining Menu', 'Bespoke Concierge Chat'],
        'metrics': [
            {'val': '5-Star', 'label': 'Luxury Standard', 'icon': 'bi-award-fill'},
            {'val': '+240%', 'label': 'Direct Bookings Surge', 'icon': 'bi-graph-up-arrow'},
            {'val': '< 1.0s', 'label': 'Instant Page Load', 'icon': 'bi-lightning-charge-fill'},
            {'val': '100%', 'label': 'Mobile-First Experience', 'icon': 'bi-phone-fill'},
        ],
        'highlights': [
            {'icon': 'bi-building', 'title': 'Luxury Suites & Amenities Showcase', 'desc': 'Interactive 4K photo galleries, room dimension blueprints, and real-time amenity availability.'},
            {'icon': 'bi-calendar2-check-fill', 'title': 'Frictionless Reservation Engine', 'desc': 'Instant dates selection, guest management, and direct check-in booking assistance.'},
            {'icon': 'bi-cup-hot-fill', 'title': 'Dining & Banquet Experiences', 'desc': 'Digital menus for rooftop lounges, poolside bars, and private grand ballroom banquet reservations.'},
            {'icon': 'bi-whatsapp', 'title': 'VIP Concierge WhatsApp Connect', 'desc': 'One-tap direct access to the hotel front desk and travel concierge for personalized guest itineraries.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I saw your Royal Grand Hotel project. I want to build a luxury website/portal for my hotel or resort.',
    },
    'royal-bites-luxury-fine-dining-restaurant': {
        'badge_text': '✦ Premium Gourmet & Fine Dining Portal',
        'tagline': 'A mouthwatering, mobile-first culinary website for Royal Bites Restaurant featuring interactive menus, chef specials, table reservations, and instant WhatsApp ordering.',
        'highlight_chips': ['Interactive Digital Food Menu', 'Instant Table Reservation', 'Chef Signature Specials', 'High Footfall Inbound Flow'],
        'metrics': [
            {'val': '4.9★', 'label': 'Customer Rating', 'icon': 'bi-star-fill'},
            {'val': '3.5x', 'label': 'More Table Bookings', 'icon': 'bi-people-fill'},
            {'val': '100%', 'label': 'Menu Browsing Speed', 'icon': 'bi-lightning-fill'},
            {'val': '0-Wait', 'label': 'Instant WhatsApp Connect', 'icon': 'bi-whatsapp'},
        ],
        'highlights': [
            {'icon': 'bi-egg-fried', 'title': 'Interactive Gourmet Digital Menu', 'desc': 'Appetizing visual food catalog with pricing, spicy levels, dietary indicators, and chef recommendations.'},
            {'icon': 'bi-calendar-event-fill', 'title': 'One-Tap Table Reservations', 'desc': 'Streamlined booking form allowing guests to reserve party tables, family dinners, and corporate banquets.'},
            {'icon': 'bi-geo-alt-fill', 'title': 'Kanpur Local Dining Integration', 'desc': 'Direct Google Maps directions, parking guidelines, and operating hours for local foodies.'},
            {'icon': 'bi-chat-left-dots-fill', 'title': 'Direct Order & Catering Inquiries', 'desc': 'Frictionless lead routing to restaurant manager for bulk orders, catering, and birthday celebrations.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I checked out your Royal Bites Restaurant project and want to build a website for my restaurant/cafe.',
    },
    'bright-future-academy-coaching-institute': {
        'badge_text': '✦ Premier Educational Coaching & Foundation Portal',
        'tagline': 'A modern, student-centric academic coaching portal for Bright Future Academy featuring foundational curriculum pathways, faculty directories, coding & science programs, and online admission desk.',
        'highlight_chips': ['Interactive Course Curriculum', 'Expert Faculty Mentorship', 'Online Admission & Scholarships', 'Comprehensive Test Prep'],
        'metrics': [
            {'val': '1,500+', 'label': 'Students Trained', 'icon': 'bi-mortarboard-fill'},
            {'val': '98.5%', 'label': 'Exam Pass Rate', 'icon': 'bi-award-fill'},
            {'val': '15+', 'label': 'Expert Mentors', 'icon': 'bi-people-fill'},
            {'val': '< 0.8s', 'label': 'Course Catalog Speed', 'icon': 'bi-lightning-charge-fill'},
        ],
        'highlights': [
            {'icon': 'bi-book-half', 'title': 'Foundation & Competitive Syllabi', 'desc': 'Comprehensive modules for Classes 6th–12th, Mathematics, Science, and STEM coding labs.'},
            {'icon': 'bi-person-check-fill', 'title': 'Faculty Excellence Showcase', 'desc': 'Detailed teacher profiles, subject expertise, and personalized doubt-clearing sessions.'},
            {'icon': 'bi-ticket-detailed-fill', 'title': 'Automated Admission Desk', 'desc': 'Frictionless student registration, fee structure transparency, and scholarship tests.'},
            {'icon': 'bi-whatsapp', 'title': 'Parent & Counselor Support', 'desc': 'Direct WhatsApp advisory for parents seeking academic counseling and batch timings.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I saw your Bright Future Academy project. I want to build an educational coaching website for my institute.',
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


