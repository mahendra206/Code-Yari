/**
 * Code Yari — Main Frontend Interactions
 * Vanilla JavaScript for Theme, Animations, Filtering, Navbar & Widgets
 */

document.addEventListener('DOMContentLoaded', () => {
  initPagePreloader();
  initTheme();
  initNavbarScroll();
  initMobileNavbar();
  initStatsCounter();
  initPortfolioFilter();
  initAutoDismissAlerts();
  initScrollToTop();
  initCustomCursor();
  initLogoAnimation();
});

/* --------------------------------------------------------------------------
   1. Dark / Light Mode Theme Toggle
   -------------------------------------------------------------------------- */
function initTheme() {
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const themeIcon = document.getElementById('theme-icon');
  
  const savedTheme = localStorage.getItem('codeyari_theme');
  const currentTheme = savedTheme || 'light'; // Default to clean light agency aesthetic matching brand guide

  document.documentElement.setAttribute('data-theme', currentTheme);
  updateThemeIcon(themeIcon, currentTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const active = document.documentElement.getAttribute('data-theme');
      const nextTheme = active === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem('codeyari_theme', nextTheme);
      updateThemeIcon(themeIcon, nextTheme);
    });
  }
}

function updateThemeIcon(icon, theme) {
  if (!icon) return;
  if (theme === 'light') {
    icon.classList.remove('bi-moon-stars');
    icon.classList.add('bi-sun-fill');
  } else {
    icon.classList.remove('bi-sun-fill');
    icon.classList.add('bi-moon-stars');
  }
}

/* --------------------------------------------------------------------------
   2. Navbar Scroll Effect
   -------------------------------------------------------------------------- */
function initNavbarScroll() {
  const navbar = document.querySelector('.site-navbar');
  if (!navbar) return;

  const handleScroll = () => {
    if (window.scrollY > 40) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

/* --------------------------------------------------------------------------
   Mobile Navbar Interactions (Auto-close on click)
   -------------------------------------------------------------------------- */
function initMobileNavbar() {
  const navbarCollapse = document.getElementById('navbarMain');
  if (!navbarCollapse) return;

  const navLinks = navbarCollapse.querySelectorAll('.nav-link:not(.dropdown-toggle), .dropdown-item, .btn-navbar-quote, .btn-navbar-login');
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth < 992 && navbarCollapse.classList.contains('show') && typeof bootstrap !== 'undefined') {
        const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse) || new bootstrap.Collapse(navbarCollapse, { toggle: false });
        bsCollapse.hide();
      }
    });
  });
}

/* --------------------------------------------------------------------------
   3. Animated Numbers / Stats Counter
   -------------------------------------------------------------------------- */
function initStatsCounter() {
  const statElements = document.querySelectorAll('.stat-count');
  if (!statElements.length) return;

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const targetValue = parseInt(el.getAttribute('data-target'), 10);
        const suffix = el.getAttribute('data-suffix') || '';
        if (!isNaN(targetValue)) {
          animateCount(el, targetValue, suffix);
        }
        obs.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  statElements.forEach(el => observer.observe(el));
}

function animateCount(el, target, suffix) {
  let start = 0;
  const duration = 1500;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Ease out quart
    const easeProgress = 1 - Math.pow(1 - progress, 4);
    const current = Math.floor(easeProgress * target);
    
    el.textContent = current + suffix;

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      el.textContent = target + suffix;
    }
  }

  requestAnimationFrame(update);
}

/* --------------------------------------------------------------------------
   4. Portfolio Category Filtering (Client-side smooth filter)
   -------------------------------------------------------------------------- */
function initPortfolioFilter() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.portfolio-item-card');

  if (!filterBtns.length || !projectCards.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      // If user clicked link, let client filter handle or navigate
      const filterValue = btn.getAttribute('data-filter');
      
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      projectCards.forEach(card => {
        const cardCategory = card.getAttribute('data-category');
        if (filterValue === 'all' || cardCategory === filterValue) {
          card.style.display = 'block';
          card.style.animation = 'fadeIn 0.4s ease forwards';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* --------------------------------------------------------------------------
   5. Auto-dismiss Django Messages / Alerts
   -------------------------------------------------------------------------- */
function initAutoDismissAlerts() {
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });
}

/* --------------------------------------------------------------------------
   6. Scroll To Top Button
   -------------------------------------------------------------------------- */
function initScrollToTop() {
  const scrollBtn = document.getElementById('scroll-top-btn');
  if (!scrollBtn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      scrollBtn.classList.add('visible');
    } else {
      scrollBtn.classList.remove('visible');
    }
  }, { passive: true });

  scrollBtn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

/* --------------------------------------------------------------------------
   7. Custom Interactive Cursor (Dot + Circle Ring Follower)
   -------------------------------------------------------------------------- */
function initCustomCursor() {
  // Only enable on desktop devices with fine pointer (mouse)
  if (window.matchMedia('(pointer: coarse)').matches) return;

  const dot = document.getElementById('cursorDot');
  const circle = document.getElementById('cursorCircle');
  if (!dot || !circle) return;

  document.body.classList.add('custom-cursor-active');

  let mouseX = -100;
  let mouseY = -100;
  let circleX = -100;
  let circleY = -100;
  let isVisible = false;

  // Track mouse position
  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;

    if (!isVisible) {
      isVisible = true;
      circleX = mouseX;
      circleY = mouseY;
      dot.style.opacity = '1';
      circle.style.opacity = '1';
    }

    // Dot snaps directly to mouse coordinates
    dot.style.left = mouseX + 'px';
    dot.style.top = mouseY + 'px';
  }, { passive: true });

  // Outer circle follows with smooth fluid easing (LERP)
  const speed = 0.16; // Easing speed
  function animateCircle() {
    if (isVisible) {
      circleX += (mouseX - circleX) * speed;
      circleY += (mouseY - circleY) * speed;
      circle.style.left = circleX + 'px';
      circle.style.top = circleY + 'px';
    }
    requestAnimationFrame(animateCircle);
  }
  requestAnimationFrame(animateCircle);

  // Fade out on window leave
  document.addEventListener('mouseleave', () => {
    isVisible = false;
    dot.style.opacity = '0';
    circle.style.opacity = '0';
  });

  document.addEventListener('mouseenter', () => {
    isVisible = true;
    dot.style.opacity = '1';
    circle.style.opacity = '1';
  });

  // Clicking effect
  window.addEventListener('mousedown', () => {
    circle.classList.add('cursor-clicking');
    dot.classList.add('cursor-clicking');
  });

  window.addEventListener('mouseup', () => {
    circle.classList.remove('cursor-clicking');
    dot.classList.remove('cursor-clicking');
  });

  // Interactive hover expansion
  const interactiveSelector = 'a, button, input, select, textarea, [role="button"], .btn, .service-v2-card-link, .portfolio-card, .filter-btn, .theme-toggle-btn, .social-icon-link';

  document.addEventListener('mouseover', (e) => {
    if (e.target && e.target.closest && e.target.closest(interactiveSelector)) {
      circle.classList.add('cursor-hover');
      dot.classList.add('cursor-hover');
    }
  });

  document.addEventListener('mouseout', (e) => {
    if (e.target && e.target.closest && e.target.closest(interactiveSelector)) {
      circle.classList.remove('cursor-hover');
      dot.classList.remove('cursor-hover');
    }
  });
}

/* --------------------------------------------------------------------------
   8. Premium Page Preloader & Dynamic Progress Indicator
   -------------------------------------------------------------------------- */
function initPagePreloader() {
  const preloader = document.getElementById('page-preloader');
  const progressBar = document.getElementById('preloaderBar');
  const percentText = document.getElementById('preloaderPercent');
  if (!preloader) return;

  let progress = 0;
  let isWindowLoaded = (document.readyState === 'complete');

  window.addEventListener('load', () => {
    isWindowLoaded = true;
  });

  const timer = setInterval(() => {
    // Smooth progress increment
    if (progress < 65) {
      progress += Math.floor(Math.random() * 7) + 5;
    } else if (progress < 85) {
      progress += isWindowLoaded ? 7 : 3;
    } else if (progress < 99 && isWindowLoaded) {
      progress += 6;
    } else if (isWindowLoaded) {
      progress = 100;
    }

    if (progress > 100) progress = 100;

    if (progressBar) progressBar.style.width = progress + '%';
    if (percentText) percentText.textContent = progress + '%';

    if (progress >= 100) {
      clearInterval(timer);
      setTimeout(() => {
        preloader.classList.add('loaded');
        triggerLogoReveal();
        setTimeout(() => {
          preloader.style.display = 'none';
        }, 600);
      }, 180);
    }
  }, 28);

  // Fallback safety timeout (max 2 seconds)
  setTimeout(() => {
    isWindowLoaded = true;
    if (progress < 100) {
      progress = 100;
      if (progressBar) progressBar.style.width = '100%';
      if (percentText) percentText.textContent = '100%';
      setTimeout(() => {
        preloader.classList.add('loaded');
        triggerLogoReveal();
        setTimeout(() => {
          preloader.style.display = 'none';
        }, 600);
      }, 150);
    }
  }, 2000);
}

/* --------------------------------------------------------------------------
   9. Animated Brand Logo Controller (Letter-by-Letter Stagger & Hover Wave)
   -------------------------------------------------------------------------- */
function triggerLogoReveal() {
  const logos = document.querySelectorAll('.brand-logo-wrap');
  logos.forEach(logo => {
    if (!logo.classList.contains('is-revealed')) {
      logo.classList.add('is-revealed');
    }
  });
}

function initLogoAnimation() {
  const preloader = document.getElementById('page-preloader');
  
  // If preloader doesn't exist or is already marked loaded, trigger immediately
  if (!preloader || preloader.classList.contains('loaded')) {
    setTimeout(triggerLogoReveal, 80);
  } else {
    // Safety fallback so logo always shows up even if preloader timer encounters any lag
    setTimeout(triggerLogoReveal, 900);
  }

  // Interactive Replay: Re-trigger entrance animation on double click / logo click with Ctrl
  const logos = document.querySelectorAll('.brand-logo-wrap');
  logos.forEach(logo => {
    logo.addEventListener('dblclick', (e) => {
      e.preventDefault();
      replayLogoAnimation(logo);
    });
  });
}

function replayLogoAnimation(logo) {
  if (!logo) return;
  logo.classList.remove('is-revealed');
  void logo.offsetWidth; // Force DOM reflow
  logo.classList.add('is-revealed');
}



