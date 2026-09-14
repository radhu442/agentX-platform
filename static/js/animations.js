document.addEventListener('DOMContentLoaded', () => {
  // Check for prefers-reduced-motion
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  if (prefersReducedMotion || typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
    return;
  }

  // Register ScrollTrigger
  gsap.registerPlugin(ScrollTrigger);

  // Common ScrollTrigger settings
  const defaultST = {
    start: 'top 85%',
    toggleActions: 'play none none none',
    markers: false
  };

  // 1. Section titles
  gsap.utils.toArray('.section-title').forEach(title => {
    gsap.from(title, {
      scrollTrigger: {
        trigger: title,
        ...defaultST
      },
      y: 30,
      opacity: 0,
      duration: 0.8,
      ease: 'power2.out'
    });
  });

  // 2. About cards
  const aboutCards = gsap.utils.toArray('.about-card');
  if (aboutCards.length > 0) {
    gsap.from(aboutCards, {
      scrollTrigger: {
        trigger: aboutCards[0],
        ...defaultST
      },
      y: 50,
      opacity: 0,
      duration: 0.8,
      stagger: 0.2,
      ease: 'power2.out'
    });
  }

  // 3. Feature cards (Alternating left/right)
  const featureCards = gsap.utils.toArray('.feature-card');
  if (featureCards.length > 0) {
    featureCards.forEach((card, index) => {
      gsap.from(card, {
        scrollTrigger: {
          trigger: card,
          ...defaultST
        },
        x: index % 2 === 0 ? 50 : -50,
        opacity: 0,
        duration: 0.8,
        delay: index * 0.15,
        ease: 'power2.out'
      });
    });
  }

  // 4. Timeline items
  const timelineItems = gsap.utils.toArray('.timeline-item');
  timelineItems.forEach((item, index) => {
    const circle = item.querySelector('.timeline-circle');
    const content = item.querySelector('.timeline-content');
    
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: item,
        ...defaultST
      }
    });

    if (circle) {
      tl.from(circle, {
        scale: 0,
        duration: 0.4,
        ease: 'back.out(1.5)'
      });
    }

    if (content) {
      tl.from(content, {
        x: index % 2 === 0 ? -30 : 30,
        opacity: 0,
        duration: 0.6,
        ease: 'power2.out'
      }, '-=0.2');
    }
  });

  // 5. Track cards
  const trackCards = gsap.utils.toArray('.track-card');
  if (trackCards.length > 0) {
    gsap.from(trackCards, {
      scrollTrigger: {
        trigger: trackCards[0],
        ...defaultST
      },
      scale: 0.9,
      opacity: 0,
      duration: 0.6,
      stagger: 0.3,
      ease: 'power2.out'
    });
  }

  // 6. Prize cards
  const prizeCards = gsap.utils.toArray('.prize-card');
  if (prizeCards.length > 0) {
    prizeCards.forEach((card, index) => {
      // Assuming center card is the grand prize, e.g., index 1 if there are 3 cards
      const isGrandPrize = prizeCards.length === 3 && index === 1;
      
      gsap.from(card, {
        scrollTrigger: {
          trigger: card,
          ...defaultST
        },
        y: 60,
        opacity: 0,
        scale: isGrandPrize ? 0.95 : 1,
        duration: isGrandPrize ? 1 : 0.8,
        delay: index * 0.2,
        ease: isGrandPrize ? 'back.out(1.7)' : 'power2.out',
      });
    });
  }

  // 7. FAQ items
  const faqItems = gsap.utils.toArray('.faq-item');
  if (faqItems.length > 0) {
    gsap.from(faqItems, {
      scrollTrigger: {
        trigger: faqItems[0],
        ...defaultST
      },
      y: 20,
      opacity: 0,
      duration: 0.5,
      stagger: 0.1,
      ease: 'power1.out'
    });
  }

  // 8. Register form
  const registerForm = document.querySelector('.register-form');
  if (registerForm) {
    gsap.from(registerForm, {
      scrollTrigger: {
        trigger: registerForm,
        ...defaultST
      },
      scale: 0.95,
      opacity: 0,
      duration: 0.8,
      ease: 'power2.out'
    });
  }

  // 9. Stats counter animation
  const stats = gsap.utils.toArray('.stat-number');
  stats.forEach(stat => {
    const target = parseFloat(stat.getAttribute('data-target') || stat.innerText.replace(/[^0-9.]/g, ''));
    if (isNaN(target)) return;
    
    // Attempt to extract suffix like +, K, M
    const textOriginal = stat.innerText.trim();
    const match = textOriginal.match(/[^0-9.]+$/);
    const suffix = match ? match[0] : '';
    const isFloat = target % 1 !== 0;
    const decimals = isFloat ? (target.toString().split('.')[1] || '').length : 0;

    gsap.fromTo(stat, {
      innerHTML: 0,
    }, {
      scrollTrigger: {
        trigger: stat,
        ...defaultST
      },
      innerHTML: target,
      duration: 2,
      ease: 'power2.out',
      onUpdate: function() {
        const val = this.targets()[0].innerHTML;
        const num = parseFloat(val);
        this.targets()[0].innerHTML = num.toFixed(decimals) + suffix;
      }
    });
  });

  // 10. Hero content
  const heroTl = gsap.timeline();
  
  const heroBadge = document.querySelector('.hero-badge');
  const heroHeading = document.querySelector('.hero-heading');
  const heroSubtitle = document.querySelector('.hero-subtitle');
  const heroButtons = document.querySelectorAll('.hero-buttons .btn');
  const heroStats = document.querySelectorAll('.hero-stats .stat');

  if (heroBadge) {
    heroTl.from(heroBadge, { y: -20, opacity: 0, duration: 0.6, ease: 'power2.out' }, 0.3);
  }
  if (heroHeading) {
    heroTl.from(heroHeading, { y: 30, opacity: 0, duration: 0.8, ease: 'power2.out' }, 0.5);
  }
  if (heroSubtitle) {
    heroTl.from(heroSubtitle, { opacity: 0, duration: 0.8, ease: 'power2.out' }, 0.8);
  }
  if (heroButtons.length) {
    heroTl.from(heroButtons, { y: 20, opacity: 0, duration: 0.6, stagger: 0.2, ease: 'power2.out' }, 1.0);
  }
  if (heroStats.length) {
    heroTl.from(heroStats, { y: 20, opacity: 0, duration: 0.6, stagger: 0.15, ease: 'power2.out' }, 1.2);
  }

  // 11. Parallax on feature cards
  const featuresSection = document.querySelector('.features-section');
  if (featuresSection && featureCards.length > 0) {
    gsap.to(featureCards, {
      y: (i, target) => {
        return i % 2 === 0 ? -30 : 30; // Alternate direction
      },
      ease: 'none',
      scrollTrigger: {
        trigger: featuresSection,
        start: 'top bottom',
        end: 'bottom top',
        scrub: true
      }
    });
  }

  // 12. 3D Tilt effect on glass cards
  const tiltCards = document.querySelectorAll('.tilt-card');
  tiltCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      
      const rotateX = ((y - centerY) / centerY) * -8;
      const rotateY = ((x - centerX) / centerX) * 8;
      
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
      card.style.transition = 'transform 0.1s ease';
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = `perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)`;
      card.style.transition = 'transform 0.5s ease';
    });
  });

  // 13. Magnetic button effect
  const magneticBtns = document.querySelectorAll('.magnetic-btn');
  magneticBtns.forEach(btn => {
    const parent = btn.parentElement;
    // Bind to parent or window for wider range, let's use document for the 100px radius
    document.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      
      const distanceX = e.clientX - centerX;
      const distanceY = e.clientY - centerY;
      const distance = Math.sqrt(distanceX * distanceX + distanceY * distanceY);
      
      if (distance < 100) {
        // Calculate movement (max 10px)
        const moveX = (distanceX / 100) * 10;
        const moveY = (distanceY / 100) * 10;
        
        btn.style.transform = `translate(${moveX}px, ${moveY}px)`;
        btn.style.transition = 'transform 0.1s ease';
      } else {
        btn.style.transform = `translate(0px, 0px)`;
        btn.style.transition = 'transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
      }
    });
  });
});
