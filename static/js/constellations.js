<<<<<<< HEAD
/**
 * AgentX Particle & Constellation Engine (v2.5 High-Density Quantum Galaxy)
 * Rich, dense multi-color glowing constellations across the entire viewport.
 */
function initParticles() {
    if (document.getElementById('particles-js')) return;

=======
function initParticles() {
    if (document.getElementById('particles-js')) return;
    
>>>>>>> 70348e341f47bba4657b70688d9be21d0fa5d075
    const particlesDiv = document.createElement('div');
    particlesDiv.id = 'particles-js';
    particlesDiv.style.position = 'fixed';
    particlesDiv.style.top = '0';
    particlesDiv.style.left = '0';
    particlesDiv.style.width = '100vw';
    particlesDiv.style.height = '100vh';
    particlesDiv.style.zIndex = '-2';
<<<<<<< HEAD
    particlesDiv.style.background = 'transparent';
    particlesDiv.style.pointerEvents = 'none';
    document.body.prepend(particlesDiv);

    document.body.style.backgroundColor = '#050811';

    // Enable lines unless explicitly disabled via window.ENABLE_CONSTELLATION_LINES = false or body attribute
    const enableLines = window.ENABLE_CONSTELLATION_LINES !== false && document.body.dataset.constellations !== 'false';

    // Rich multi-color gaming cosmic neon palette
    const multiColors = [
        "#00f3ff", // Neon Cyan
        "#38bdf8", // Sky Ice Blue
        "#ff007f", // Electric Pink/Magenta
        "#9d4edd", // Cyber Purple
        "#a855f7", // Neon Violet
        "#00ff88", // Neon Lime / Mint
        "#10b981", // Emerald Green
        "#ffd700", // Solar Gold/Yellow
        "#ff5722", // Neon Coral Orange
        "#ffffff"  // Starlight White
    ];
=======
    particlesDiv.style.background = '#0a0a1a'; // Deep space background
    particlesDiv.style.pointerEvents = 'none';
    document.body.prepend(particlesDiv);
    
    document.body.style.backgroundColor = 'transparent';
>>>>>>> 70348e341f47bba4657b70688d9be21d0fa5d075

    if (typeof particlesJS !== 'undefined') {
        particlesJS("particles-js", {
            "particles": {
                "number": {
<<<<<<< HEAD
                    "value": 115, // High-density cosmic network (increased from 28)
                    "density": { "enable": true, "value_area": 650 }
                },
                "color": {
                    "value": multiColors
                },
                "shape": {
                    "type": ["circle", "triangle"],
                    "stroke": { "width": 0, "color": "#000000" }
                },
                "opacity": {
                    "value": 0.85,
                    "random": true,
                    "anim": { "enable": true, "speed": 1.6, "opacity_min": 0.35, "sync": false }
                },
                "size": {
                    "value": 3.8,
                    "random": true,
                    "anim": { "enable": true, "speed": 2.4, "size_min": 1.2, "sync": false }
                },
                "line_linked": {
                    "enable": enableLines,
                    "distance": 155, // Wide connection radius for rich, dense geometric constellation nets
                    "color": "#00f3ff",
                    "opacity": 0.55,
                    "width": 1.35
                },
                "move": {
                    "enable": true,
                    "speed": enableLines ? 1.9 : 1.3,
=======
                    "value": 140,
                    "density": { "enable": true, "value_area": 800 }
                },
                "color": { "value": ["#ffffff", "#00f2fe", "#a855f7", "#38bdf8"] },
                "shape": { "type": "circle" },
                "opacity": {
                    "value": 0.8,
                    "random": true,
                    "anim": { "enable": true, "speed": 1, "opacity_min": 0.2, "sync": false }
                },
                "size": {
                    "value": 3,
                    "random": true,
                    "anim": { "enable": true, "speed": 2, "size_min": 0.5, "sync": false }
                },
                "line_linked": {
                    "enable": true,
                    "distance": 140,
                    "color": "#38bdf8",
                    "opacity": 0.45,
                    "width": 1.4
                },
                "move": {
                    "enable": true,
                    "speed": 1.6,
>>>>>>> 70348e341f47bba4657b70688d9be21d0fa5d075
                    "direction": "none",
                    "random": true,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                    "attract": { "enable": true, "rotateX": 600, "rotateY": 1200 }
                }
            },
            "interactivity": {
                "detect_on": "window",
                "events": {
<<<<<<< HEAD
                    "onhover": { "enable": true, "mode": enableLines ? "grab" : "bubble" },
=======
                    "onhover": { "enable": true, "mode": "grab" },
>>>>>>> 70348e341f47bba4657b70688d9be21d0fa5d075
                    "onclick": { "enable": true, "mode": "push" },
                    "resize": true
                },
                "modes": {
<<<<<<< HEAD
                    "grab": {
                        "distance": 210,
                        "line_linked": { "opacity": 0.92 }
                    },
                    "bubble": {
                        "distance": 200,
                        "size": 6.5,
                        "opacity": 0.9,
                        "duration": 2
                    },
                    "push": { "particles_nb": 6 }
                }
            },
            "retina_detect": false
=======
                    "grab": { "distance": 180, "line_linked": { "opacity": 0.9 } },
                    "push": { "particles_nb": 4 }
                }
            },
            "retina_detect": true
>>>>>>> 70348e341f47bba4657b70688d9be21d0fa5d075
        });
    }
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initParticles);
} else {
    initParticles();
}
