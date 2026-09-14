/**
 * Floating Particles System
 * Ambient floating particles using Canvas 2D API for background and footer sections.
 */

class ParticleSystem {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        
        // Configuration
        this.isMobile = window.innerWidth < 768;
        this.prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        
        this.config = {
            count: this.isMobile ? 40 : 80,
            colors: ['#7c3aed', '#06b6d4', '#ec4899', '#ffffff'],
            minSize: 1,
            maxSize: 4,
            speedMultiplier: this.prefersReducedMotion ? 0.1 : 1, // Reduce speed by 90% if needed
            connectionDist: 150,
            mousePushDist: 100,
            mousePushForce: 0.05
        };
        
        this.mouse = { x: -1000, y: -1000 };
        this.container = this.canvas.parentElement;
        this.isVisible = true;

        this.init();
    }

    init() {
        this.resize();
        this.createParticles();
        this.bindEvents();
        this.animate();
    }

    resize() {
        // Fill parent container
        const rect = this.container.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
    }

    createParticles() {
        this.particles = [];
        for (let i = 0; i < this.config.count; i++) {
            this.particles.push(this.createParticle());
        }
    }

    createParticle() {
        const radius = this.config.minSize + Math.random() * (this.config.maxSize - this.config.minSize);
        return {
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            vx: (Math.random() * 0.6 - 0.3) * this.config.speedMultiplier,
            vy: (Math.random() * 0.6 - 0.3) * this.config.speedMultiplier,
            radius: radius,
            color: this.config.colors[Math.floor(Math.random() * this.config.colors.length)],
            opacity: 0.1 + Math.random() * 0.4
        };
    }

    bindEvents() {
        window.addEventListener('resize', () => this.resize());
        
        this.container.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouse.x = e.clientX - rect.left;
            this.mouse.y = e.clientY - rect.top;
        });

        this.container.addEventListener('mouseleave', () => {
            this.mouse.x = -1000;
            this.mouse.y = -1000;
        });

        // Intersection Observer to pause when not visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                this.isVisible = entry.isIntersecting;
            });
        });
        observer.observe(this.canvas);
    }

    drawParticle(p) {
        this.ctx.beginPath();
        // Radial gradient for soft edges
        const gradient = this.ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.radius);
        
        // Helper to convert hex to rgba
        const hex2rgba = (hex, alpha) => {
            const r = parseInt(hex.slice(1, 3), 16);
            const g = parseInt(hex.slice(3, 5), 16);
            const b = parseInt(hex.slice(5, 7), 16);
            return \`rgba(\${r}, \${g}, \${b}, \${alpha})\`;
        };
        
        gradient.addColorStop(0, hex2rgba(p.color, p.opacity));
        gradient.addColorStop(1, hex2rgba(p.color, 0));
        
        this.ctx.fillStyle = gradient;
        this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        this.ctx.fill();
    }

    drawConnections() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const p1 = this.particles[i];
                const p2 = this.particles[j];
                
                const dx = p1.x - p2.x;
                const dy = p1.y - p2.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist < this.config.connectionDist) {
                    const opacity = (1 - (dist / this.config.connectionDist)) * 0.15;
                    this.ctx.beginPath();
                    this.ctx.moveTo(p1.x, p1.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.strokeStyle = \`rgba(124, 58, 237, \${opacity})\`; // Base color #7c3aed
                    this.ctx.lineWidth = 1;
                    this.ctx.stroke();
                }
            }
        }
    }

    update() {
        for (let p of this.particles) {
            // Mouse interaction (push away)
            const dx = p.x - this.mouse.x;
            const dy = p.y - this.mouse.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            
            if (dist < this.config.mousePushDist) {
                const force = (this.config.mousePushDist - dist) / this.config.mousePushDist;
                p.x += (dx / dist) * force * 2 * this.config.speedMultiplier;
                p.y += (dy / dist) * force * 2 * this.config.speedMultiplier;
            }

            // Normal movement
            p.x += p.vx;
            p.y += p.vy;

            // Wrap around edges
            if (p.x < -50) p.x = this.canvas.width + 50;
            if (p.x > this.canvas.width + 50) p.x = -50;
            if (p.y < -50) p.y = this.canvas.height + 50;
            if (p.y > this.canvas.height + 50) p.y = -50;
        }
    }

    animate() {
        if (this.isVisible) {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.update();
            this.drawConnections();
            for (let p of this.particles) {
                this.drawParticle(p);
            }
        }
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    // Create systems if canvases exist
    if (document.getElementById('bg-particles')) {
        new ParticleSystem('bg-particles');
    }
    
    if (document.getElementById('footer-particles')) {
        new ParticleSystem('footer-particles');
    }
});
