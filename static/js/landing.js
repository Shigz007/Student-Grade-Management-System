/* ──────────────────────────────────────────────────────────────
 * Landing Page JS
 * - IntersectionObserver for scroll animations
 * - Sticky nav background toggle
 * - Active nav link highlighting
 * - Counter animation
 * - Smooth scroll for nav links
 * ────────────────────────────────────────────────────────────── */

(function() {
  'use strict';

  /* ─── Sticky nav ─── */
  var nav = document.querySelector('.lp-nav');
  var ticking = false;

  function updateNav() {
    if (window.scrollY > 60) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
    ticking = false;
  }

  window.addEventListener('scroll', function() {
    if (!ticking) {
      requestAnimationFrame(updateNav);
      ticking = true;
    }
  });

  /* ─── Mobile menu toggle ─── */
  var toggle = document.querySelector('.lp-nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function() {
      nav.classList.toggle('open');
    });
  }
  /* Close menu on link click */
  var navLinks = document.querySelectorAll('.lp-nav-links a');
  navLinks.forEach(function(a) {
    a.addEventListener('click', function() {
      nav.classList.remove('open');
    });
  });

  /* ─── Smooth scroll ─── */
  document.querySelectorAll('a[href^="#"]').forEach(function(link) {
    link.addEventListener('click', function(e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        var navHeight = 80; /* offset for sticky nav */
        var top = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });

  /* ─── Active nav link ─── */
  var sections = [];
  var navAs = document.querySelectorAll('.lp-nav-links a[href^="#"]');
  navAs.forEach(function(a) {
    var id = a.getAttribute('href').substring(1);
    var el = document.getElementById(id);
    if (el) sections.push({ el: el, a: a });
  });

  function updateActiveLink() {
    var scrollPos = window.scrollY + 120;
    var active = null;
    sections.forEach(function(s) {
      if (s.el.offsetTop <= scrollPos) {
        active = s;
      }
    });
    navAs.forEach(function(a) { a.classList.remove('nav-active'); });
    if (active) active.a.classList.add('nav-active');
  }

  window.addEventListener('scroll', function() {
    if (!ticking) {
      requestAnimationFrame(function() {
        updateNav();
        updateActiveLink();
        ticking = false;
      });
      ticking = true;
    }
  });

  /* ─── Intersection Observer for animations ─── */
  var observerOptions = { threshold: 0.15, rootMargin: '0px 0px -40px 0px' };

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        var el = entry.target;
        var delay = parseInt(el.getAttribute('data-animate-delay')) || 0;
        setTimeout(function() {
          el.classList.add('animated');
        }, delay);
        observer.unobserve(el);
      }
    });
  }, observerOptions);

  document.querySelectorAll('[class*="anim-"]').forEach(function(el) {
    observer.observe(el);
  });

  /* ─── Counter animation ─── */
  var counterObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        var el = entry.target;
        var target = parseInt(el.getAttribute('data-count-to'));
        if (!target || el._counted) return;
        el._counted = true;
        var duration = 1500;
        var startTime = null;
        var startVal = 0;

        function step(ts) {
          if (!startTime) startTime = ts;
          var progress = Math.min((ts - startTime) / duration, 1);
          var eased = 1 - Math.pow(1 - progress, 3);
          el.textContent = Math.round(startVal + (target - startVal) * eased);
          if (progress < 1) {
            requestAnimationFrame(step);
          } else {
            el.textContent = target;
          }
        }
        requestAnimationFrame(step);
        counterObserver.unobserve(el);
      }
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('[data-count-to]').forEach(function(el) {
    counterObserver.observe(el);
  });

  /* ─── Typewriter for terminal ─── */
  var terminal = document.querySelector('.lp-terminal');
  if (terminal) {
    var terminalObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var lines = terminal.querySelectorAll('.type-line');
          typeLines(lines, 0);
          terminalObserver.unobserve(terminal);
        }
      });
    }, { threshold: 0.3 });
    terminalObserver.observe(terminal);
  }

  function typeLines(lines, idx) {
    if (idx >= lines.length) return;
    var line = lines[idx];
    var text = line.getAttribute('data-text') || '';
    var cursor = line.querySelector('.cursor');
    var i = 0;
    line.textContent = '';

    function typeChar() {
      if (i < text.length) {
        line.textContent += text[i];
        i++;
        setTimeout(typeChar, 30 + Math.random() * 40);
      } else {
        if (cursor && idx < lines.length - 1) {
          line.appendChild(cursor);
        }
        setTimeout(function() {
          if (cursor && idx < lines.length - 1) {
            cursor.remove();
          }
          typeLines(lines, idx + 1);
        }, 400);
      }
    }
    typeChar();
  }

  /* ─── Bar chart animation ─── */
  var barObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        var bars = entry.target.querySelectorAll('.lp-bar, .lp-score-bar');
        bars.forEach(function(bar) {
          var h = bar.getAttribute('data-h');
          if (h) bar.style.height = h;
        });
        barObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  var barChart = document.querySelector('.lp-bars');
  var scoreChart = document.querySelector('.lp-score-bars');
  if (barChart) barObserver.observe(barChart);
  if (scoreChart) barObserver.observe(scoreChart);

})();
