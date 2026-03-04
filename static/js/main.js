/* ── Page Loader ─────────────────────────────────────────────── */
(function () {
  const loader  = document.getElementById('page-loader');
  const bar     = document.getElementById('loader-bar');
  const statusEl= document.getElementById('loader-status-text');
  const pctEl   = document.getElementById('loader-percent');
  const linesEl = document.getElementById('loader-lines');
  const term    = document.getElementById('loader-terminal');
  const nameEl  = document.getElementById('loader-name');

  if (!loader) return;

  /* inject styles */
  const s = document.createElement('style');
  s.textContent = `
    @keyframes scanLine { 0%{top:0;opacity:.5} 100%{top:100%;opacity:0} }
    @keyframes hexFlick  { 0%,100%{opacity:.18} 50%{opacity:.32} }
    @keyframes blink     { 0%,100%{opacity:1}   50%{opacity:0}   }
    @keyframes glitch {
      0%,100%{transform:translateX(0);opacity:1}
      20%{transform:translateX(-3px);clip-path:inset(15% 0 70% 0)}
      40%{transform:translateX(3px);clip-path:inset(55% 0 10% 0)}
      60%{transform:translateX(-1px);clip-path:inset(0)}
      80%{transform:translateX(2px);opacity:.8}
    }
    #loader-name.glitch { animation: glitch .45s steps(1) forwards; }
    #loader-scanline { position:absolute;left:0;right:0;height:2px;
      background:linear-gradient(90deg,transparent,rgba(204,0,0,.25),transparent);
      animation:scanLine 2.5s linear infinite;pointer-events:none;z-index:5; }
    #loader-corner-tl,#loader-corner-tr,#loader-corner-bl,#loader-corner-br {
      position:absolute;width:14px;height:14px;border-color:#cc0000;border-style:solid;opacity:.7;
    }
    #loader-corner-tl{top:-1px;left:-1px;border-width:2px 0 0 2px}
    #loader-corner-tr{top:-1px;right:-1px;border-width:2px 2px 0 0}
    #loader-corner-bl{bottom:-1px;left:-1px;border-width:0 0 2px 2px}
    #loader-corner-br{bottom:-1px;right:-1px;border-width:0 2px 2px 0}
    #loader-hex { position:absolute;bottom:10px;right:14px;
      font-family:'Share Tech Mono',monospace;font-size:.38rem;color:#1e1e1e;
      line-height:1.6;text-align:right;pointer-events:none;animation:hexFlick 1.2s ease infinite; }
    #loader-cursor { display:inline-block;width:7px;height:.9em;background:#cc0000;
      vertical-align:middle;margin-left:3px;animation:blink .7s step-end infinite; }
  `;
  document.head.appendChild(s);

  /* scanline */
  const scan = document.createElement('div');
  scan.id = 'loader-scanline';
  term.style.position = 'relative';
  term.appendChild(scan);

  /* corners */
  ['tl','tr','bl','br'].forEach(p => {
    const c = document.createElement('div');
    c.id = 'loader-corner-' + p;
    term.appendChild(c);
  });

  /* hex noise */
  const hex = document.createElement('div');
  hex.id = 'loader-hex';
  const mkHex = () => Array.from({length:5},()=>
    Array.from({length:9},()=>Math.floor(Math.random()*256).toString(16).padStart(2,'0').toUpperCase()).join(' ')
  ).join('\n');
  hex.textContent = mkHex();
  term.appendChild(hex);
  const hexInterval = setInterval(()=>{ hex.textContent = mkHex(); }, 350);

  /* cursor */
  const cursor = document.createElement('span');
  cursor.id = 'loader-cursor';

  const sequence = [
    { text:'<span class="l-dim">┌──────────────────────────────────────────┐</span>', status:'BOOTING...', pct:0, delay:0 },
    { text:'<span class="l-dim">│</span>  <span class="l-white">AFT SECURE BOOT SEQUENCE v2.4.1</span>  <span class="l-dim">│</span>', status:'BOOTING...', pct:5, delay:80 },
    { text:'<span class="l-dim">└──────────────────────────────────────────┘</span>', status:'BOOTING...', pct:8, delay:160 },
    { text:'<span class="l-dim">──────────────────────────────────────────</span>', status:'BOOTING...', pct:10, delay:240 },
    { text:'&gt; Verifying hardware signature...  <span class="l-ok">PASS</span>', status:'VERIFYING HARDWARE...', pct:18, delay:400 },
    { text:'&gt; Loading kernel modules...        <span class="l-ok">DONE</span>', status:'LOADING KERNEL...', pct:28, delay:560 },
    { text:'&gt; Mounting encrypted filesystem... <span class="l-ok">DONE</span>', status:'MOUNTING FILESYSTEM...', pct:38, delay:700 },
    { text:'&gt; AES-256-GCM cipher suite...      <span class="l-ok">LOADED</span>', status:'CIPHER ACTIVE...', pct:47, delay:840 },
    { text:'&gt; Initializing secure datalink...  <span class="l-warn">WAIT</span>', status:'ESTABLISHING LINK...', pct:54, delay:980 },
    { text:'&gt; Datalink handshake complete      <span class="l-ok">ONLINE</span>', status:'LINK SECURED...', pct:62, delay:1140 },
    { text:'<span class="l-dim">──────────────────────────────────────────</span>', status:'LOADING REGISTRY...', pct:65, delay:1220 },
    { text:'&gt; FALCON X1  [SURVEILLANCE]        <span class="l-ok">OPERATIONAL</span>', status:'FALCON X1...', pct:72, delay:1340 },
    { text:'&gt; FALCON X2  [TACTICAL UAV]        <span class="l-warn">DEVELOPMENT</span>', status:'FALCON X2...', pct:79, delay:1460 },
    { text:'&gt; FALCON L3  [LOITERING MUN.]      <span class="l-dim">PROTOTYPE</span>', status:'FALCON L3...', pct:84, delay:1560 },
    { text:'&gt; CR-100     [CIVIL RECON]         <span class="l-ok">OPERATIONAL</span>', status:'CR-100...', pct:89, delay:1650 },
    { text:'<span class="l-dim">──────────────────────────────────────────</span>', status:'LOADING AI ENGINE...', pct:91, delay:1730 },
    { text:'&gt; AI targeting engine...           <span class="l-ok">READY</span>', status:'AI ENGINE...', pct:94, delay:1820 },
    { text:'&gt; GPS-denied navigation stack...   <span class="l-ok">READY</span>', status:'GPS NAV STACK...', pct:96, delay:1900 },
    { text:'&gt; Threat assessment module...      <span class="l-ok">ACTIVE</span>', status:'THREAT MODULE...', pct:98, delay:1980 },
  ];

  sequence.forEach(({ text, status, pct, delay }) => {
    setTimeout(() => {
      if (bar) bar.style.width = pct + '%';
      if (pctEl) pctEl.textContent = pct + '%';
      if (statusEl) statusEl.textContent = status;
      if (linesEl) {
        if (cursor.parentNode) cursor.parentNode.removeChild(cursor);
        const row = document.createElement('span');
        row.className = 'loader-line';
        row.innerHTML = text;
        linesEl.appendChild(row);
        linesEl.appendChild(cursor);
        term.scrollTop = term.scrollHeight;
      }
    }, delay);
  });

  /* final ACCESS GRANTED */
  setTimeout(() => {
    clearInterval(hexInterval);
    if (cursor.parentNode) cursor.parentNode.removeChild(cursor);
    if (bar) bar.style.width = '100%';
    if (pctEl) { pctEl.textContent = '100%'; pctEl.style.color = '#00ff41'; }
    if (statusEl) { statusEl.textContent = 'ACCESS GRANTED'; statusEl.style.color = '#00ff41'; }
    const final = document.createElement('span');
    final.className = 'loader-line';
    final.innerHTML = '<span class="l-dim">──────────────────────────────────────────</span>';
    linesEl.appendChild(final);
    const granted = document.createElement('span');
    granted.className = 'loader-line';
    granted.innerHTML = '&gt; <span style="color:#cc0000;letter-spacing:.15em;">AFalconeri Technologies</span> — <span class="l-ok" style="font-weight:700;letter-spacing:.2em;">ACCESS GRANTED</span>';
    linesEl.appendChild(granted);
    term.scrollTop = term.scrollHeight;
    if (nameEl) {
      setTimeout(() => nameEl.classList.add('glitch'), 150);
    }
  }, 2150);

  setTimeout(() => {
    loader.classList.add('done');
    setTimeout(() => { loader.style.display = 'none'; }, 800);
  }, 2900);
})();

/* ============================================================
   AFalconeri Technologies — Main JavaScript
   ============================================================ */

'use strict';

/* ── Custom Cursor ─────────────────────────────────────────── */
const initCursor = () => {
  const cursor = document.querySelector('.cursor');
  const follower = document.querySelector('.cursor-follower');
  if (!cursor || !follower) return;

  let mouseX = 0, mouseY = 0;
  let followerX = 0, followerY = 0;

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    cursor.style.left = mouseX + 'px';
    cursor.style.top = mouseY + 'px';
  });

  const animateFollower = () => {
    followerX += (mouseX - followerX) * 0.12;
    followerY += (mouseY - followerY) * 0.12;
    follower.style.left = followerX + 'px';
    follower.style.top = followerY + 'px';
    requestAnimationFrame(animateFollower);
  };
  animateFollower();

  const hoverTargets = document.querySelectorAll('a, button, .system-card-preview, .cap-item, .doctrine-item, .vision-metric');
  hoverTargets.forEach(el => {
    el.addEventListener('mouseenter', () => {
      cursor.classList.add('hover');
      follower.classList.add('hover');
    });
    el.addEventListener('mouseleave', () => {
      cursor.classList.remove('hover');
      follower.classList.remove('hover');
    });
  });
};

/* ── Scroll Progress Bar ────────────────────────────────────── */
const initScrollProgress = () => {
  const bar = document.querySelector('.scroll-progress');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = scrollTop / docHeight;
    bar.style.width = (progress * 100) + '%';
  }, { passive: true });
};

/* ── Navigation Scroll Behavior ─────────────────────────────── */
const initNav = () => {
  const nav = document.querySelector('.nav');
  if (!nav) return;
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) nav.classList.add('scrolled');
    else nav.classList.remove('scrolled');
  }, { passive: true });

  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath !== '/' && href !== '/' && currentPath.startsWith(href))) {
      link.classList.add('active');
    }
  });
};

/* ── Mobile Menu ────────────────────────────────────────────── */
const initMobileMenu = () => {
  const hamburger = document.querySelector('.nav-hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (!hamburger || !mobileMenu) return;

  let open = false;
  hamburger.addEventListener('click', () => {
    open = !open;
    mobileMenu.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    hamburger.querySelectorAll('span')[0].style.transform = open ? 'rotate(45deg) translate(4px, 4px)' : '';
    hamburger.querySelectorAll('span')[1].style.opacity = open ? '0' : '1';
    hamburger.querySelectorAll('span')[2].style.transform = open ? 'rotate(-45deg) translate(4px, -4px)' : '';
  });

  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      open = false;
      mobileMenu.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
};

/* ── Intersection Observer Animations ─────────────────────── */
const initRevealAnimations = () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05, rootMargin: '0px 0px 0px 0px' });

  document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => {
    observer.observe(el);
  });
};

/* ── Parallax Hero ──────────────────────────────────────────── */
const initParallax = () => {
  const heroBg = document.querySelector('.hero-bg');
  const heroDrone = document.querySelector('.hero-drone-silhouette');
  if (!heroBg) return;

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        const scrollY = window.scrollY;
        if (heroBg) heroBg.style.transform = `translateY(${scrollY * 0.3}px)`;
        if (heroDrone) heroDrone.style.transform = `translateY(calc(-50% + ${scrollY * 0.15}px))`;
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
};

/* ── Animated Counter ───────────────────────────────────────── */
const animateCounter = (el, target, duration = 2000) => {
  const start = parseInt(el.textContent) || 0;
  const increment = (target - start) / (duration / 16);
  let current = start;
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) { current = target; clearInterval(timer); }
    el.textContent = Math.round(current) + (el.dataset.suffix || '');
  }, 16);
};

const initCounters = () => {
  const counters = document.querySelectorAll('[data-counter]');
  if (!counters.length) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target, parseInt(entry.target.dataset.counter));
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(el => observer.observe(el));
};

/* ── Text Glitch Effect on Hover ────────────────────────────── */
const initGlitch = () => {
  const glitchChars = '!@#$%^&*()_+ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  document.querySelectorAll('[data-glitch]').forEach(el => {
    const original = el.textContent;
    let interval;
    el.addEventListener('mouseenter', () => {
      let iterations = 0;
      clearInterval(interval);
      interval = setInterval(() => {
        el.textContent = original.split('').map((char, i) => {
          if (i < iterations) return original[i];
          if (char === ' ') return ' ';
          return glitchChars[Math.floor(Math.random() * glitchChars.length)];
        }).join('');
        if (iterations >= original.length) clearInterval(interval);
        iterations += 1 / 2;
      }, 30);
    });
    el.addEventListener('mouseleave', () => { clearInterval(interval); el.textContent = original; });
  });
};

/* ── Contact Form Enhancement ───────────────────────────────── */
const initContactForm = () => {
  const form = document.querySelector('.contact-form');
  if (!form) return;
  form.querySelectorAll('.form-control').forEach(input => {
    input.addEventListener('focus', () => input.closest('.form-group')?.classList.add('focused'));
    input.addEventListener('blur', () => {
      input.closest('.form-group')?.classList.remove('focused');
      if (input.value) input.closest('.form-group')?.classList.add('filled');
      else input.closest('.form-group')?.classList.remove('filled');
    });
  });
};

/* ── Smooth Anchor Scrolling ─────────────────────────────────── */
const initSmoothScroll = () => {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      const navH = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 70;
      window.scrollTo({ top: target.offsetTop - navH, behavior: 'smooth' });
    });
  });
};

/* ── Page Load Animation ─────────────────────────────────────── */
const initPageLoad = () => {
  document.body.classList.add('loaded');
  document.querySelectorAll('.nav-link').forEach((link, i) => {
    link.style.animationDelay = `${0.1 + i * 0.08}s`;
    link.style.animation = 'fadeUp 0.5s forwards';
    link.style.opacity = '0';
  });
};

/* ── Tactical Grid Pulse ──────────────────────────────────────── */
const initGridPulse = () => {
  const grid = document.querySelector('.grid-overlay');
  if (!grid) return;
  setInterval(() => {
    grid.style.opacity = '0.6';
    setTimeout(() => { grid.style.opacity = '1'; }, 200);
  }, 8000);
};

/* ── Boot Sequence ──────────────────────────────────────────── */

/* ── Back to Top ─────────────────────────────────────────────── */
const initBackToTop = () => {
  const btn = document.querySelector('.back-to-top');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });
  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
};
document.addEventListener('DOMContentLoaded', () => {
  initPageLoad();
  initCursor();
  initScrollProgress();
  initNav();
  initMobileMenu();
  initRevealAnimations();
  initParallax();
  initCounters();
  initGlitch();
  initContactForm();
  initSmoothScroll();
  initGridPulse();
  initBackToTop();

  console.log('%c AFalconeri Technologies ', 'background:#cc0000;color:#fff;font-family:monospace;font-size:14px;padding:4px 8px;');
  console.log('%c Advanced Defense & Aerospace Systems ', 'color:#cc0000;font-family:monospace;font-size:10px;');
});