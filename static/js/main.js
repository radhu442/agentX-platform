document.addEventListener('DOMContentLoaded', () => {
  // 1. Smooth Scroll Navigation
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        const headerOffset = 80;
        const elementPosition = targetEl.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // 2. Active Nav Link via IntersectionObserver
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');

  const observerOptions = {
    root: null,
    rootMargin: '-80px 0px -60% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${entry.target.id}`) {
            link.classList.add('active');
          }
        });
      }
    });
  }, observerOptions);

  sections.forEach(sec => observer.observe(sec));

  // 3. Nav Scroll Effect
  const nav = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      nav?.classList.add('nav-scrolled');
    } else {
      nav?.classList.remove('nav-scrolled');
    }
  });

  // 4. Mobile Menu
  const mobileToggle = document.querySelector('.mobile-menu-btn');
  const mobileMenu = document.querySelector('.nav-links');
  const mobileLinks = document.querySelectorAll('.nav-links a');
  
  if (mobileToggle && mobileMenu) {
    const toggleMenu = () => {
      mobileToggle.classList.toggle('active');
      mobileMenu.classList.toggle('active');
      document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    };

    mobileToggle.addEventListener('click', toggleMenu);

    mobileLinks.forEach(link => {
      link.addEventListener('click', toggleMenu);
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
        toggleMenu();
      }
    });
  }

  // 5. Typing Animation
  const typingElement = document.getElementById('typing-text');
  if (typingElement) {
    const words = ['Reusable Skills', 'MCP Integrations', 'Freshworks Platform'];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    const typeEffect = () => {
      const currentWord = words[wordIndex];
      
      if (isDeleting) {
        typingElement.innerText = currentWord.substring(0, charIndex - 1);
        charIndex--;
      } else {
        typingElement.innerText = currentWord.substring(0, charIndex + 1);
        charIndex++;
      }

      let typeSpeed = isDeleting ? 30 : 50;

      if (!isDeleting && charIndex === currentWord.length) {
        typeSpeed = 2000;
        isDeleting = true;
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        wordIndex = (wordIndex + 1) % words.length;
        typeSpeed = 500;
      }

      setTimeout(typeEffect, typeSpeed);
    };

    setTimeout(typeEffect, 500);
  }

  // 6. FAQ Accordion
  const faqQuestions = document.querySelectorAll('.faq-question');
  faqQuestions.forEach(question => {
    question.addEventListener('click', () => {
      const parent = question.parentElement;
      const isOpen = parent.classList.contains('active');
      
      // Close all
      document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('active');
        const answer = item.querySelector('.faq-answer');
        if (answer) answer.style.maxHeight = null;
      });

      if (!isOpen) {
        parent.classList.add('active');
        const answer = parent.querySelector('.faq-answer');
        if (answer) {
          answer.style.maxHeight = answer.scrollHeight + 'px';
        }
      }
    });
  });

  // 7. Registration Form
  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const nameInput = registerForm.querySelector('input[name="name"]');
      const emailInput = registerForm.querySelector('input[name="email"]');
      const trackSelect = registerForm.querySelector('select[name="track"]');
      const submitBtn = registerForm.querySelector('button[type="submit"]');
      const successMessage = document.querySelector('.success-message');
      let isValid = true;

      // Reset errors
      registerForm.querySelectorAll('.form-error').forEach(el => el.classList.remove('form-error'));
      const oldError = registerForm.querySelector('.error-text');
      if (oldError) oldError.remove();

      // Validate
      if (!nameInput.value.trim()) {
        nameInput.classList.add('form-error');
        isValid = false;
      }
      
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailInput.value.trim() || !emailRegex.test(emailInput.value)) {
        emailInput.classList.add('form-error');
        isValid = false;
      }

      if (!trackSelect.value) {
        trackSelect.classList.add('form-error');
        isValid = false;
      }

      if (!isValid) return;

      // Submit
      const originalBtnText = submitBtn.innerText;
      submitBtn.innerText = 'Registering...';
      submitBtn.disabled = true;

      try {
        const teamInput = registerForm.querySelector('input[name="teamName"]');
        const skillsInput = registerForm.querySelector('input[name="skills"]');
        const githubInput = registerForm.querySelector('input[name="github"]');

        const response = await fetch('/api/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: nameInput.value,
            email: emailInput.value,
            team_name: teamInput ? teamInput.value : '',
            track: trackSelect.value,
            skills: skillsInput ? skillsInput.value : '',
            github_url: githubInput ? githubInput.value : ''
          })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Registration failed');

        // Success
        registerForm.style.display = 'none';
        if (successMessage) {
          successMessage.style.display = 'block';
          successMessage.style.animation = 'fadeIn 0.5s ease forwards';
        }
      } catch (err) {
        const errorMsg = document.createElement('div');
        errorMsg.className = 'error-text';
        errorMsg.style.color = '#ff4d4d';
        errorMsg.style.marginTop = '10px';
        errorMsg.innerText = 'Registration failed. Please try again.';
        registerForm.appendChild(errorMsg);
      } finally {
        submitBtn.innerText = originalBtnText;
        submitBtn.disabled = false;
      }
    });
  }

  // 8. Track Selection
  const selectTrackBtns = document.querySelectorAll('.select-track-btn');
  selectTrackBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const trackValue = btn.getAttribute('data-track');
      const trackSelect = document.querySelector('select[name="track"]');
      
      if (trackSelect && trackValue) {
        trackSelect.value = trackValue;
      }
      
      const registerSection = document.getElementById('register');
      if (registerSection) {
        const headerOffset = 80;
        const elementPosition = registerSection.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // 9. Custom Cursor (desktop only)
  const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  
  if (!isTouchDevice) {
    const cursorDot = document.createElement('div');
    const cursorRing = document.createElement('div');
    
    cursorDot.className = 'custom-cursor-dot';
    cursorRing.className = 'custom-cursor-ring';
    
    document.body.appendChild(cursorDot);
    document.body.appendChild(cursorRing);
    
    // Inject basic CSS for cursor if not present in main CSS
    const style = document.createElement('style');
    style.innerHTML = `
      body { cursor: none; }
      .custom-cursor-dot, .custom-cursor-ring {
        position: fixed;
        pointer-events: none;
        z-index: 9999;
        transform: translate(-50%, -50%);
        border-radius: 50%;
      }
      .custom-cursor-dot {
        width: 8px;
        height: 8px;
        background-color: var(--primary-color, #00ff88);
        transition: transform 0.1s ease;
      }
      .custom-cursor-ring {
        width: 32px;
        height: 32px;
        border: 2px solid var(--primary-color, #00ff88);
        transition: transform 0.1s ease, width 0.3s ease, height 0.3s ease;
      }
      .custom-cursor-ring.hover {
        width: 50px;
        height: 50px;
        background-color: rgba(0, 255, 136, 0.1);
      }
      a:hover, button:hover, .tilt-card:hover, input, select, textarea { cursor: none; }
    `;
    document.head.appendChild(style);

    let mouseX = 0;
    let mouseY = 0;
    let ringX = 0;
    let ringY = 0;

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      
      cursorDot.style.left = mouseX + 'px';
      cursorDot.style.top = mouseY + 'px';
    });

    const render = () => {
      ringX += (mouseX - ringX) * 0.15; // lerp
      ringY += (mouseY - ringY) * 0.15;
      
      cursorRing.style.left = ringX + 'px';
      cursorRing.style.top = ringY + 'px';
      
      requestAnimationFrame(render);
    };
    render();

    // Hover effect
    const interactables = document.querySelectorAll('a, button, .tilt-card, input, select, textarea');
    interactables.forEach(el => {
      el.addEventListener('mouseenter', () => cursorRing.classList.add('hover'));
      el.addEventListener('mouseleave', () => cursorRing.classList.remove('hover'));
    });
  }

  // 10. Scroll Progress Bar
  const progressBar = document.createElement('div');
  progressBar.className = 'scroll-progress-bar';
  progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    height: 2px;
    background: linear-gradient(90deg, #00ff88, #00aaff);
    z-index: 10000;
    width: 0%;
    transition: width 0.1s ease;
  `;
  document.body.appendChild(progressBar);

  window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    progressBar.style.width = scrolled + '%';
  });

  // 11. Back to Top Button
  const backToTop = document.createElement('button');
  backToTop.className = 'back-to-top';
  backToTop.innerHTML = '↑';
  backToTop.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    font-size: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 999;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
  `;
  document.body.appendChild(backToTop);

  window.addEventListener('scroll', () => {
    if (window.scrollY > 500) {
      backToTop.style.opacity = '1';
      backToTop.style.visibility = 'visible';
    } else {
      backToTop.style.opacity = '0';
      backToTop.style.visibility = 'hidden';
    }
  });

  backToTop.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
});
