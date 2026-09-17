# Code Yari — Digital Services Agency Web Platform

> **"Code. Create. Grow."**  
> *"Sirf code nahi, Yari ke saath solution."*

Code Yari is a production-ready, full-stack website and lead management platform engineered for a modern digital technology agency. Built strictly using **Python Django**, **Django Templates**, **HTML5/CSS3**, and **Vanilla JavaScript** with a tailored high-performance design system.

---

## 🌟 Highlights & Features

- **End-to-End Modular Architecture**: 8 decoupled Django apps separating domain logic cleanly.
- **Rich Modern UI/UX**:
  - Dark Mode default with persistent Light Mode toggle.
  - Glassmorphism effects with backdrop blur.
  - Radiant brand gradients (Indigo / Violet / Cyan).
  - Subtle micro-animations, hover interactions, and card elevations.
  - Animated numbers / stats counter powered by `IntersectionObserver`.
  - Floating WhatsApp quick-chat widget.
- **Dynamic Content & CRM**:
  - **Dynamic Services Catalog**: Detailed capabilities, tech stack chips, and prefilled inquiry links.
  - **Portfolio Case Studies**: Category filtering (both client-side instant filter and server-side fallback) with detailed problem, solution, and business impact narratives.
  - **Blog & Technical Insights**: Categorized articles, read-time calculation, tag cloud, social sharing, and related post suggestions.
  - **Interactive FAQ**: Accordion grouped by categories.
  - **Client Testimonials**: Verified ratings, client roles, and avatars.
  - **Lead Capture & Quote Generator**: Multi-step quote request form with honeypot anti-spam protection and automatic email notification simulation.
  - **Contact Management**: Direct inquiry form with real-time feedback and validation.
- **SEO & Social Optimization**:
  - Dynamic `sitemap.xml` including static pages, services, portfolio items, and blog posts.
  - Automated `robots.txt` routing.
  - OpenGraph & Twitter Card metadata per page.
  - Schema.org `ProfessionalService` JSON-LD structured data.
- **Production Preparedness**:
  - Environment-based configuration via `.env` / `python-dotenv`.
  - Static file compression & caching via `whitenoise`.
  - Database agnostic: SQLite for lightweight dev, ready for PostgreSQL / MySQL in production.
  - Clearly tagged demo content with one-command seeding and purging.

---

## 🏗️ Project Architecture

```
code_yari/
│
├── config/                     # Project root configuration
│   ├── settings.py             # Base, environment, and security settings
│   ├── urls.py                 # Master URL configuration & Sitemaps
│   ├── asgi.py & wsgi.py       # ASGI / WSGI entry points
│
├── apps/                       # Modular business domain apps
│   ├── core/                   # Home, About, Contact, Legal, Settings, Sitemaps
│   │   └── management/commands/# seed_demo_data & clear_demo_data
│   ├── services/               # Service catalog and detail views
│   ├── portfolio/              # Projects, case studies, galleries, categories
│   ├── leads/                  # Quote request form & CRM lead intake
│   ├── testimonials/           # Client reviews and star ratings
│   ├── blog/                   # Articles, categories, tags, and insights
│   ├── faq/                    # Categorized FAQ accordions
│   └── accounts/               # Administrative staff profile handling
│
├── static/                     # Global static assets
│   ├── css/main.css            # Custom design tokens, glassmorphism & responsive CSS
│   ├── js/main.js              # Theme switcher, scroll state, counters, filters
│   ├── images/                 # SVG logos and graphic assets
│   └── icons/                  # Brand and tech icon sets
│
├── templates/                  # Django templates
│   ├── base.html               # Master layout with SEO headers and schema
│   ├── partials/               # Navbar, footer, messages, WhatsApp, CTA banner
│   ├── core/                   # Home, About, Contact, Privacy, Terms, robots.txt
│   ├── services/               # Services list and detail
│   ├── portfolio/              # Portfolio list and case study detail
│   ├── blog/                   # Blog list and article detail
│   ├── faq/                    # FAQ list
│   ├── testimonials/           # Testimonials list
│   ├── leads/                  # Get a Quote form
│   └── errors/                 # Custom 404 & 500 error pages
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
└── .env.example                # Example environment variables
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (Python 3.14 compatible)
- PowerShell or Bash terminal

### 2. Environment Setup
```bash
# Navigate to project directory
cd code_yari

# Create virtual environment (if not already created)
python -m venv ../venv

# Activate virtual environment
# Windows PowerShell:
..\venv\Scripts\Activate.ps1
# Linux / macOS:
source ../venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file from the provided `.env.example`:
```bash
cp .env.example .env
```

### 4. Database Setup & Migrations
```bash
python manage.py migrate
```

### 5. Seed Demo Content
Populate the database with realistic, clearly-labeled demo data (services, portfolio projects, blog posts, FAQs, testimonials, and team members):
```bash
python manage.py seed_demo_data
```

*(To clean up all demo data at any time: `python manage.py clear_demo_data --force`)*

### 6. Admin Account
A default superuser is ready for local development:
- **URL**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Username**: `admin`
- **Password**: `admin123`

### 7. Run Development Server
```bash
python manage.py runserver
```
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 🧪 Testing & Verification

Run the test suite:
```bash
python manage.py test apps.core
```

---

## 🔒 Security Best Practices
- Secret keys and credentials are abstracted into environment variables.
- Forms incorporate Django's `{% csrf_token %}` and hidden anti-spam honeypot fields.
- Content security, XSS protection, and host validation enabled.
- For production deployment, set `DEBUG=False` and supply an authorized `ALLOWED_HOSTS` list.
