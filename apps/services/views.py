import urllib.parse
from django.shortcuts import render, get_object_or_404
from .models import Service


SERVICE_EXTRAS = {
    'web-development': {
        'badge_text': '✦ Modern & High-Speed Web Architecture',
        'tagline': 'High-performance, beautifully designed & SEO-first websites that turn visitors into loyal paying customers.',
        'highlight_chips': ['Ultra-Fast < 1.2s Load', '100% Mobile Responsive', 'SEO Core Web Vitals 95+', 'Full Source Code Rights'],
        'metrics': [
            {'val': '99.9%', 'label': 'Uptime & Reliability', 'icon': 'bi-shield-check'},
            {'val': '< 1.2s', 'label': 'Average Page Load', 'icon': 'bi-lightning-charge-fill'},
            {'val': '100%', 'label': 'Custom Clean Code', 'icon': 'bi-code-slash'},
            {'val': '24/7', 'label': 'Direct Tech Support', 'icon': 'bi-headset'},
        ],
        'why_choose': [
            {'icon': 'bi-lightning-charge-fill', 'title': 'Blazing Fast Speed', 'desc': 'Engineered to score 90+ on Google PageSpeed with optimized assets, smart caching, and minified bundles.'},
            {'icon': 'bi-shield-lock-fill', 'title': 'Bank-Grade Security', 'desc': 'Hardened against CSRF, XSS, and SQL injection with automated SSL, daily backups, and strict data safeguards.'},
            {'icon': 'bi-phone-fill', 'title': 'Pixel-Perfect on All Screens', 'desc': 'Fluid responsive layouts that look breath-taking on smartphones, tablets, laptops, and ultra-wide screens.'},
            {'icon': 'bi-github', 'title': '100% Code Ownership', 'desc': 'You receive complete Git repository ownership, clean documentation, and deployment guides. Zero vendor lock-in.'},
        ],
        'process': [
            {'num': '01', 'title': 'Discovery & Tech Architecture', 'desc': 'We study your business goals, target audience, and select the optimal stack (Django, React, Next.js, or PostgreSQL).'},
            {'num': '02', 'title': 'Figma UI/UX & Interactive Prototype', 'desc': 'We craft modern, visually stunning designs with full client approval before any code is written.'},
            {'num': '03', 'title': 'Clean Sprint Development', 'desc': 'Modular, clean code built in transparent weekly sprints with live staging demo links for your feedback.'},
            {'num': '04', 'title': 'Rigorous QA, SEO & Live Launch', 'desc': 'Cross-device testing, lighthouse speed audit, search engine indexing, domain linking, and launch celebration.'},
        ],
        'faqs': [
            {'q': 'How long does a web development project take?', 'a': 'Standard high-converting business websites take 1 to 2 weeks, while custom SaaS platforms or e-commerce web applications typically take 3 to 6 weeks depending on feature scope.'},
            {'q': 'Do I get 100% full ownership of the source code?', 'a': 'Yes, absolutely! Upon final delivery, 100% of the Git repository, code files, database schemas, and intellectual property are handed over to you.'},
            {'q': 'Will our website be SEO-friendly and Google-ready?', 'a': 'Every website we build is structured according to Google Schema.org standards, has semantic HTML5, fast Core Web Vitals, and automated sitemaps out of the box.'},
            {'q': 'What happens after the website is launched?', 'a': 'We provide 30 days of complimentary post-launch support and bug fixes, along with training on how to manage your content effortlessly.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I want to discuss a new Web Development project for my business.',
    },
    'app-development': {
        'badge_text': '✦ Cross-Platform iOS & Android Apps',
        'tagline': 'Smooth, native-feel mobile applications built for viral retention, high speed, and effortless scalability.',
        'highlight_chips': ['Single Codebase iOS & Android', 'Buttery 60 FPS Fluid UI', 'Offline-First Ready', 'App Store Guaranteed Launch'],
        'metrics': [
            {'val': '60 FPS', 'label': 'Smooth Fluid Animations', 'icon': 'bi-speedometer2'},
            {'val': '2-in-1', 'label': 'iOS & Android Sync', 'icon': 'bi-phone-fill'},
            {'val': '4.9★', 'label': 'App Store Grade UX', 'icon': 'bi-star-fill'},
            {'val': '100%', 'label': 'Offline Database Sync', 'icon': 'bi-cloud-check-fill'},
        ],
        'why_choose': [
            {'icon': 'bi-phone-landscape-fill', 'title': 'Native Experience', 'desc': 'Built with Flutter and React Native delivering instantaneous load times and platform-specific haptic interactions.'},
            {'icon': 'bi-bell-fill', 'title': 'Smart Push Notifications', 'desc': 'Targeted segmentation, automated engagement triggers, and transactional push alerts with Firebase Cloud Messaging.'},
            {'icon': 'bi-cloud-arrow-down-fill', 'title': 'Offline-First Architecture', 'desc': 'Local SQLite/Hive caching lets users navigate and use key features seamlessly even without an internet connection.'},
            {'icon': 'bi-patch-check-fill', 'title': 'Guaranteed Store Approval', 'desc': 'Full compliance handling, signing certificates, and policy adherence for Google Play Store and Apple App Store.'},
        ],
        'process': [
            {'num': '01', 'title': 'User Flow & Wireframing', 'desc': 'Mapping user personas, screen sequences, intuitive gesture interactions, and technical API requirements.'},
            {'num': '02', 'title': 'High-Fidelity App UI in Figma', 'desc': 'Designing according to Apple iOS Human Interface and Google Material Design guidelines for a premium feel.'},
            {'num': '03', 'title': 'Cross-Platform App Development', 'desc': 'Writing clean, test-driven Flutter / React Native code integrated with secure cloud backend APIs.'},
            {'num': '04', 'title': 'Device Lab QA & App Store Launch', 'desc': 'Testing on real Android and iOS devices, beta release via TestFlight/Internal Track, and public publishing.'},
        ],
        'faqs': [
            {'q': 'Will the app work on both iPhone and Android?', 'a': 'Yes! By using industry-standard cross-platform frameworks (Flutter & React Native), you get native iOS and Android apps with 50% lower maintenance cost.'},
            {'q': 'Do you assist with publishing to Apple App Store & Google Play Store?', 'a': 'Yes, we take care of the entire store deployment workflow including store screenshots, metadata, privacy terms, and review approvals.'},
            {'q': 'Can the mobile app work offline?', 'a': 'Yes, we implement smart local caching so users can access core content and queue actions that sync automatically once online.'},
            {'q': 'Do you offer ongoing app maintenance & updates?', 'a': 'Yes, we provide ongoing updates for new OS releases (iOS & Android version upgrades), library patches, and feature additions.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I am looking to develop a Mobile App for iOS and Android. Let\'s connect!',
    },
    'seo-google-ranking': {
        'badge_text': '✦ #1 Google Organic Traffic Acceleration',
        'tagline': 'Scientific, 100% white-hat SEO strategies that conquer Google Page #1 and deliver high-intent organic leads.',
        'highlight_chips': ['Page #1 Google Target', 'High-Intent Buyer Keywords', '0% Blackhat Penalty Risk', 'Weekly Live ROI Reports'],
        'metrics': [
            {'val': '+320%', 'label': 'Avg Organic Traffic Surge', 'icon': 'bi-graph-up-arrow'},
            {'val': '#1 Rank', 'label': 'Google Target Positions', 'icon': 'bi-trophy-fill'},
            {'val': '0%', 'label': 'Spam / Penalty Risk', 'icon': 'bi-shield-check'},
            {'val': 'Weekly', 'label': 'Transparent Keyword Reports', 'icon': 'bi-bar-chart-fill'},
        ],
        'why_choose': [
            {'icon': 'bi-bullseye', 'title': 'High-Intent Buyer Keywords', 'desc': 'We don\'t chase vanity traffic; we rank your business for keywords that actual prospective clients use to buy.'},
            {'icon': 'bi-cpu-fill', 'title': 'Deep Technical SEO Audits', 'desc': 'Resolving indexation issues, site speed, structured data schemas, canonicals, and Core Web Vitals hurdles.'},
            {'icon': 'bi-award-fill', 'title': 'Authoritative White-Hat Backlinks', 'desc': 'Handcrafted digital PR and high-domain authority editorial backlinks that build long-lasting Google trust.'},
            {'icon': 'bi-geo-alt-fill', 'title': 'Google Maps Local Dominance', 'desc': 'Dominate local 3-pack search results to capture nearby customers actively searching for your service.'},
        ],
        'process': [
            {'num': '01', 'title': 'Deep Site & Competitor Audit', 'desc': 'Uncovering technical blockers, backlink deficits, and keyword opportunities your competitors are winning.'},
            {'num': '02', 'title': 'On-Page Optimization & Schema', 'desc': 'Restructuring title tags, meta descriptions, H1/H2 tags, semantic content, and JSON-LD rich snippets.'},
            {'num': '03', 'title': 'High-Value Content & Link Building', 'desc': 'Publishing comprehensive search-intent content and securing authentic niche authority backlinks.'},
            {'num': '04', 'title': 'Rank Tracking & Conversion Lift', 'desc': 'Weekly rank position tracking, Google Search Console audits, and conversion rate optimizations.'},
        ],
        'faqs': [
            {'q': 'How quickly will we see our Google ranking improve?', 'a': 'Most businesses start witnessing keyword movement within 30 to 45 days, with dramatic organic traffic and lead surges typically compounding between months 3 to 6.'},
            {'q': 'Are your SEO methods 100% white-hat and safe?', 'a': 'Absolutely 100%! We strictly abide by Google Webmaster Guidelines and never use risky link-schemes or automation that could harm your domain reputation.'},
            {'q': 'Will SEO help my local business get nearby customers?', 'a': 'Yes! Our local SEO package optimizes your Google Business Profile (Maps) so you appear in top local searches and voice queries.'},
            {'q': 'How do you measure and report SEO success?', 'a': 'We provide weekly live dashboard reports tracking keyword rankings, organic impressions, clicks, bounce rate, and lead conversions.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I want to rank my website on Google Page 1 with your SEO services.',
    },
    'digital-marketing': {
        'badge_text': '✦ High-ROAS Performance Marketing',
        'tagline': 'Laser-targeted paid ads, social campaigns, and sales funnels engineered to maximize your return on ad spend.',
        'highlight_chips': ['4.5x+ Average ROAS', 'Meta & Google Ads Masters', 'Automated Lead Funnels', 'Zero Ad Spend Waste'],
        'metrics': [
            {'val': '4.8x', 'label': 'Average ROAS on Ad Spend', 'icon': 'bi-cash-coin'},
            {'val': '-38%', 'label': 'Lower Cost Per Lead', 'icon': 'bi-arrow-down-circle-fill'},
            {'val': '360°', 'label': 'Omnichannel Retargeting', 'icon': 'bi-arrow-repeat'},
            {'val': '24/7', 'label': 'Live Campaign Monitoring', 'icon': 'bi-eye-fill'},
        ],
        'why_choose': [
            {'icon': 'bi-crosshair', 'title': 'Laser-Focused Audience Targeting', 'desc': 'We segment high-converting buyers by demographics, search intent, and interest profiles on Meta and Google.'},
            {'icon': 'bi-funnel-fill', 'title': 'High-Converting Sales Funnels', 'desc': 'Custom landing pages and automated follow-up sequences engineered to turn curious clicks into paying customers.'},
            {'icon': 'bi-palette-fill', 'title': 'Compelling Ad Creatives & Copy', 'desc': 'High-CTR video scripts, thumb-stopping graphic hooks, and emotional ad copy that drives direct action.'},
            {'icon': 'bi-graph-up', 'title': 'Transparent ROI Attribution', 'desc': 'Every single rupee spent is tied directly to generated leads and sales with Google Tag Manager & Conversion API.'},
        ],
        'process': [
            {'num': '01', 'title': 'Audience & Offer Strategy', 'desc': 'Defining your high-converting irresistible offer, customer avatar, and competitor advertising intelligence.'},
            {'num': '02', 'title': 'Creative Production & Funnel Setup', 'desc': 'Crafting high-impact banners, video hooks, and ultra-fast landing pages with conversion tracking.'},
            {'num': '03', 'title': 'Campaign Launch & Multi-Variant Testing', 'desc': 'Launching A/B tests across audiences, creatives, and placements to identify winning combinations.'},
            {'num': '04', 'title': 'Profitable Scaling & Retargeting', 'desc': 'Scaling winning ads profitably while cutting underperforming ad sets to consistently lower CPA.'},
        ],
        'faqs': [
            {'q': 'What ad platforms do you specialize in?', 'a': 'We specialize in Meta Ads (Facebook & Instagram), Google Search & Display Ads, YouTube Video Ads, and LinkedIn B2B campaigns.'},
            {'q': 'What is the minimum recommended ad budget?', 'a': 'You can start with flexible budgets starting from ₹15,000 to ₹30,000/month, and we scale up strategically as profitability is proven.'},
            {'q': 'How do you prevent ad spend wastage?', 'a': 'We implement negative keyword exclusions, laser audience whitelisting, and strict daily budget caps with automated stop-loss rules.'},
            {'q': 'How often do we get performance updates?', 'a': 'You get access to a 24/7 real-time analytics dashboard along with weekly performance check-in calls with our senior strategist.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I want to run high-ROI Digital Marketing & Paid Ad campaigns for my business.',
    },
    'uiux-design': {
        'badge_text': '✦ Human-Centered Digital Experiences',
        'tagline': 'Breathtaking, intuitive, and modern UI/UX designs that captivate users, build trust, and multiply conversion rates.',
        'highlight_chips': ['Custom Figma Design System', '+85% User Engagement Lift', 'Developer-Ready Handoff', 'Clickable Interactive Prototype'],
        'metrics': [
            {'val': '100%', 'label': 'Bespoke Figma UI System', 'icon': 'bi-palette-fill'},
            {'val': '+85%', 'label': 'Higher User Engagement', 'icon': 'bi-hand-index-thumb-fill'},
            {'val': '0-Friction', 'label': 'Streamlined User Flows', 'icon': 'bi-check2-circle'},
            {'val': 'Clickable', 'label': 'Interactive Mobile Prototype', 'icon': 'bi-play-circle-fill'},
        ],
        'why_choose': [
            {'icon': 'bi-layers-fill', 'title': 'Scalable Design Systems', 'desc': 'Standardized component libraries, auto-layout tokens, color palettes, and typography for seamless future updates.'},
            {'icon': 'bi-eye-fill', 'title': 'Conversion-Driven Psychology', 'desc': 'Visual hierarchy, CTA positioning, and contrast ratios engineered to guide user attention and maximize signups.'},
            {'icon': 'bi-phone-fill', 'title': 'Interactive Mobile & Web Prototypes', 'desc': 'Experience and test full user journeys on your actual smartphone before a single line of code is written.'},
            {'icon': 'bi-code-slash', 'title': 'Zero-Hassle Developer Handoff', 'desc': 'Pixel-perfect CSS tokens, SVG assets, and spacing documentation ready for immediate developer implementation.'},
        ],
        'process': [
            {'num': '01', 'title': 'Research & User Journey Mapping', 'desc': 'Analyzing user expectations, information architecture, and core screen workflows to remove user friction.'},
            {'num': '02', 'title': 'Low-Fidelity Wireframes', 'desc': 'Rapid structural wireframing to establish optimal layout hierarchy and content placement.'},
            {'num': '03', 'title': 'High-Fidelity Visual Design in Figma', 'desc': 'Infusing modern aesthetics, vibrant brand color harmony, micro-animations, and sleek dark/light styling.'},
            {'num': '04', 'title': 'Interactive Prototype & Dev Handoff', 'desc': 'Delivering clickable prototypes, user validation testing, and complete developer component asset packages.'},
        ],
        'faqs': [
            {'q': 'What design software do you use?', 'a': 'We use industry-standard Figma, giving you real-time collaboration, commenting capabilities, and clickable prototypes on web and mobile.'},
            {'q': 'Do I get the complete editable Figma source file?', 'a': 'Yes! You receive full edit access and ownership of the complete Figma file including components, variants, and style guides.'},
            {'q': 'Can your team also code the designed UI into a live product?', 'a': 'Yes! Our full-stack engineering team can seamlessly turn the Figma designs into production-ready Web, iOS, or Android applications.'},
            {'q': 'How many rounds of design revisions are included?', 'a': 'We work iteratively with unlimited design adjustments during the wireframing and high-fidelity design phase until you are 100% in love with the look.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I need a modern, beautiful UI/UX Design for my product. Let\'s talk!',
    },
    'ai-automation': {
        'badge_text': '✦ Next-Gen AI & Intelligent Automation',
        'tagline': 'Supercharge your operations with intelligent 24/7 AI chatbots, custom workflows, and smart automation pipelines.',
        'highlight_chips': ['10x Operational Efficiency', '24/7 WhatsApp AI Chatbots', '99% Manual Error Elimination', 'Zero-Code Zapier / n8n Sync'],
        'metrics': [
            {'val': '10x', 'label': 'Efficiency & Time Saved', 'icon': 'bi-lightning-charge-fill'},
            {'val': '24/7', 'label': 'Instant AI Lead Response', 'icon': 'bi-robot'},
            {'val': '99%', 'label': 'Manual Error Elimination', 'icon': 'bi-patch-check-fill'},
            {'val': '100%', 'label': 'Secure & Private Data', 'icon': 'bi-shield-lock-fill'},
        ],
        'why_choose': [
            {'icon': 'bi-robot', 'title': 'Custom Knowledge-Trained AI', 'desc': 'AI agents trained exclusively on your business documentation, PDFs, and FAQs to answer customer queries with 100% precision.'},
            {'icon': 'bi-whatsapp', 'title': 'WhatsApp Business Automation', 'desc': 'Instant lead capture, payment notifications, appointment scheduling, and customer service directly via WhatsApp.'},
            {'icon': 'bi-diagram-3-fill', 'title': 'Seamless Multi-App Integrations', 'desc': 'Connect CRM, Google Sheets, ERP, Email, and payment gateways with zero manual copy-paste overhead.'},
            {'icon': 'bi-shield-lock-fill', 'title': 'Enterprise-Grade Privacy & Security', 'desc': 'Your proprietary customer and business data remains private, encrypted, and is never used to train public models.'},
        ],
        'process': [
            {'num': '01', 'title': 'Workflow & Bottleneck Audit', 'desc': 'Identifying repetitive manual operations and mapping high-impact automation quick-wins.'},
            {'num': '02', 'title': 'Custom AI Architecture & Prompting', 'desc': 'Setting up private vector databases, fine-tuned system prompts, and multi-step logic flows.'},
            {'num': '03', 'title': 'Pipeline Build & Integration Testing', 'desc': 'Connecting webhook pipelines (n8n, Python, Make, LangChain) with resilient error handling and fallbacks.'},
            {'num': '04', 'title': 'Deployment & Staff Handover', 'desc': 'Live deployment, performance stress testing, automated logging, and training your team on how to manage the system.'},
        ],
        'faqs': [
            {'q': 'Can AI chatbots handle our customer inquiries on WhatsApp?', 'a': 'Yes! We build official WhatsApp Business API chatbots that converse naturally in multiple languages, answer product questions, and book orders 24/7.'},
            {'q': 'Can you connect AI automation with our existing software?', 'a': 'Yes, we integrate with Google Sheets, Excel, Zoho, HubSpot, Shopify, WooCommerce, Slack, and custom SQL databases via secure APIs.'},
            {'q': 'Is our private business data secure and confidential?', 'a': 'Yes, strictly. We deploy enterprise AI endpoints with strict data residency and zero-retention policies where your data is never shared.'},
            {'q': 'What happens if an AI bot cannot answer a question?', 'a': 'We configure smart human handoff rules that instantly notify your human team on WhatsApp or Email whenever a complex query arises.'},
        ],
        'whatsapp_msg': 'Hi Code Yari! I want to implement AI & Automation solutions for my business operations.',
    },
}


def _get_fallback_extras(service):
    """Generate dynamic, high-converting metadata for any service."""
    return {
        'badge_text': f'✦ Certified {service.name} Solutions',
        'tagline': service.short_description or f'Enterprise-grade {service.name} engineered for speed, reliability, and business growth.',
        'highlight_chips': [f'{service.name} Experts', '100% Tailored Code', 'Fast Turnaround', 'Full IP Rights'],
        'metrics': [
            {'val': '99%+', 'label': 'Client Satisfaction', 'icon': 'bi-star-fill'},
            {'val': 'Fast', 'label': 'Agile Turnaround', 'icon': 'bi-lightning-fill'},
            {'val': '100%', 'label': 'Custom Architecture', 'icon': 'bi-patch-check-fill'},
            {'val': '24/7', 'label': 'Direct Tech Support', 'icon': 'bi-headset'},
        ],
        'why_choose': [
            {'icon': 'bi-award-fill', 'title': 'Senior Dedicated Engineers', 'desc': f'Our experienced developers work directly on your {service.name} project with zero outsourced delays.'},
            {'icon': 'bi-speedometer2', 'title': 'Built for Peak Performance', 'desc': f'Every deliverable for {service.name} is engineered for speed, clean architecture, and modern best practices.'},
            {'icon': 'bi-shield-check', 'title': 'Transparent & Milestone-Based', 'desc': 'Clear milestone deliverables, regular progress demos, and zero hidden costs.'},
            {'icon': 'bi-arrow-repeat', 'title': 'Long-Term Growth Support', 'desc': 'Continuous monitoring, maintenance, and technical updates after successful deployment.'},
        ],
        'process': [
            {'num': '01', 'title': 'Discovery & Requirement Mapping', 'desc': f'We define exact scopes, deliverables, timelines, and technology stack for your {service.name} project.'},
            {'num': '02', 'title': 'Architecture & Prototyping', 'desc': 'Creating comprehensive prototypes, design workflows, and architectural blueprints for your approval.'},
            {'num': '03', 'title': 'Agile Sprint Development', 'desc': 'Executing development in transparent sprints with regular code commits and live preview demos.'},
            {'num': '04', 'title': 'QA, Deployment & Launch', 'desc': 'Rigorous automated testing, security validation, smooth live deployment, and handover.'},
        ],
        'faqs': [
            {'q': f'How do we get started with {service.name}?', 'a': f'Simply click "Request a Quote" or message us directly on WhatsApp. We provide a detailed scope and cost breakdown within 24 hours.'},
            {'q': 'What is the expected project turnaround time?', 'a': 'Depending on project complexity, timelines typically range from 1 to 4 weeks with weekly milestones and demo previews.'},
            {'q': 'Do I own all source code and deliverables?', 'a': 'Yes, 100%! All repositories, designs, code, and documentation belong completely to you upon handover.'},
            {'q': 'Do you provide post-delivery support?', 'a': 'Yes! Every project includes complimentary post-launch bug fixes and support, with optional ongoing maintenance.'},
        ],
        'whatsapp_msg': f'Hi Code Yari! I am interested in your {service.name} service. Can we discuss my project?',
    }


def services_list(request):
    services = Service.objects.filter(is_active=True).order_by('order')
    featured = services.filter(is_featured=True)
    context = {
        'page_title': 'Our Services — Code Yari',
        'meta_description': 'Explore Code Yari\'s full range of digital services: web development, app development, SEO, digital marketing, UI/UX, AI automation, and more.',
        'services': services,
        'featured_services': featured,
    }
    return render(request, 'services/list.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related_services = Service.objects.filter(
        is_active=True
    ).exclude(pk=service.pk).order_by('order')[:4]

    extras = SERVICE_EXTRAS.get(service.slug, _get_fallback_extras(service))

    # Pre-encode WhatsApp text
    whatsapp_encoded = urllib.parse.quote(extras.get('whatsapp_msg', f'Hi Code Yari! I want to discuss {service.name}.'))

    context = {
        'page_title': service.get_seo_title(),
        'meta_description': service.get_seo_description(),
        'service': service,
        'related_services': related_services,
        'features': service.features if isinstance(service.features, list) else [],
        'technologies': service.technologies if isinstance(service.technologies, list) else [],
        'extras': extras,
        'whatsapp_encoded': whatsapp_encoded,
    }
    return render(request, 'services/detail.html', context)

