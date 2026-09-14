/**
 * Three.js Neural Network Scene
 * Interactive 3D neural network visualization for the hero section background.
 */

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('hero-canvas');
    if (!canvas) return;

    // Configuration
    const isMobile = window.innerWidth < 768;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    const config = {
        nodeCount: isMobile ? 30 : 70,
        particleCount: isMobile ? 100 : 200,
        colors: [0x7c3aed, 0x06b6d4, 0xec4899],
        connectionDistance: 5,
        rotationSpeed: prefersReducedMotion ? 0.0001 : 0.001,
        motionMultiplier: prefersReducedMotion ? 0.1 : 1,
        pulseEnabled: !prefersReducedMotion,
        volumeSize: 15
    };

    // Scene Setup
    const scene = new THREE.Scene();
    
    // Camera Setup
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 10;
    
    // Renderer Setup
    const renderer = new THREE.WebGLRenderer({ 
        canvas: canvas, 
        alpha: true, 
        antialias: true 
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);

    // Groups
    const networkGroup = new THREE.Group();
    const particleGroup = new THREE.Group();
    scene.add(networkGroup);
    scene.add(particleGroup);

    // Nodes
    const nodes = [];
    const nodeGeometry = new THREE.SphereGeometry(0.15, 16, 16);
    
    for (let i = 0; i < config.nodeCount; i++) {
        const color = config.colors[Math.floor(Math.random() * config.colors.length)];
        const material = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.6 + Math.random() * 0.4
        });
        
        const node = new THREE.Mesh(nodeGeometry, material);
        
        // Random position within volume
        node.position.x = (Math.random() - 0.5) * config.volumeSize;
        node.position.y = (Math.random() - 0.5) * config.volumeSize;
        node.position.z = (Math.random() - 0.5) * (config.volumeSize * 0.5); // Flatter z depth
        
        // Custom properties for animation
        node.userData = {
            phaseX: Math.random() * Math.PI * 2,
            phaseY: Math.random() * Math.PI * 2,
            speedX: (0.01 + Math.random() * 0.02) * config.motionMultiplier,
            speedY: (0.01 + Math.random() * 0.02) * config.motionMultiplier,
            baseX: node.position.x,
            baseY: node.position.y
        };
        
        nodes.push(node);
        networkGroup.add(node);
    }

    // Connections
    const connections = [];
    const lineMaterial = new THREE.LineBasicMaterial({
        color: 0x7c3aed,
        transparent: true,
        opacity: 0.15
    });

    for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
            const dist = nodes[i].position.distanceTo(nodes[j].position);
            
            if (dist < config.connectionDistance) {
                const geometry = new THREE.BufferGeometry().setFromPoints([
                    nodes[i].position,
                    nodes[j].position
                ]);
                
                // Clone material so we can animate them individually
                const material = lineMaterial.clone();
                const line = new THREE.Line(geometry, material);
                
                line.userData = {
                    nodeA: nodes[i],
                    nodeB: nodes[j],
                    baseOpacity: 0.15,
                    baseColor: new THREE.Color(0x7c3aed),
                    isPulsing: false,
                    pulseProgress: 0
                };
                
                connections.push(line);
                networkGroup.add(line);
            }
        }
    }

    // Particles
    const particleGeometry = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(config.particleCount * 3);
    const particleOpacities = new Float32Array(config.particleCount);
    
    for (let i = 0; i < config.particleCount; i++) {
        particlePositions[i * 3] = (Math.random() - 0.5) * config.volumeSize * 1.5;
        particlePositions[i * 3 + 1] = (Math.random() - 0.5) * config.volumeSize * 1.5;
        particlePositions[i * 3 + 2] = (Math.random() - 0.5) * config.volumeSize;
        particleOpacities[i] = Math.random();
    }
    
    particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particleGeometry.setAttribute('aOpacity', new THREE.BufferAttribute(particleOpacities, 1));
    
    // Custom shader for varying opacity particles
    const particleMaterial = new THREE.ShaderMaterial({
        uniforms: {
            color: { value: new THREE.Color(0xf0f8ff) } // White with blue tint
        },
        vertexShader: `
            attribute float aOpacity;
            varying float vOpacity;
            void main() {
                vOpacity = aOpacity;
                vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
                gl_PointSize = 3.0 * (10.0 / -mvPosition.z);
                gl_Position = projectionMatrix * mvPosition;
            }
        `,
        fragmentShader: `
            uniform vec3 color;
            varying float vOpacity;
            void main() {
                float r = distance(gl_PointCoord, vec2(0.5));
                if (r > 0.5) discard;
                gl_FragColor = vec4(color, vOpacity * (1.0 - (r * 2.0)));
            }
        `,
        transparent: true,
        depthWrite: false
    });
    
    const particles = new THREE.Points(particleGeometry, particleMaterial);
    particleGroup.add(particles);

    // Mouse Interaction
    const mouse = { x: 0, y: 0, targetX: 0, targetY: 0 };
    
    window.addEventListener('mousemove', (e) => {
        mouse.targetX = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.targetY = -(e.clientY / window.innerHeight) * 2 + 1;
    });

    // Resize Handler
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Pulse Effect logic
    let pulseTimer = 0;
    const PULSE_INTERVAL = 100; // frames
    
    function updatePulses() {
        if (!config.pulseEnabled || connections.length === 0) return;
        
        pulseTimer++;
        if (pulseTimer > PULSE_INTERVAL) {
            pulseTimer = 0;
            // Trigger new pulse
            const idx = Math.floor(Math.random() * connections.length);
            if (!connections[idx].userData.isPulsing) {
                connections[idx].userData.isPulsing = true;
                connections[idx].userData.pulseProgress = 0;
            }
        }
        
        // Update active pulses
        for (let i = 0; i < connections.length; i++) {
            const conn = connections[i];
            if (conn.userData.isPulsing) {
                conn.userData.pulseProgress += 0.05 * config.motionMultiplier;
                
                const p = conn.userData.pulseProgress;
                if (p >= Math.PI) {
                    conn.userData.isPulsing = false;
                    conn.material.opacity = conn.userData.baseOpacity;
                    conn.material.color.copy(conn.userData.baseColor);
                } else {
                    // Sine wave pulse: 0 -> 1 -> 0
                    const intensity = Math.sin(p);
                    conn.material.opacity = conn.userData.baseOpacity + (0.6 * intensity);
                    
                    // Shift color to cyan (0x06b6d4)
                    const pulseColor = new THREE.Color(0x06b6d4);
                    conn.material.color.copy(conn.userData.baseColor).lerp(pulseColor, intensity);
                }
            }
        }
    }

    // Animation Loop
    let isVisible = true;
    let animationFrameId;

    document.addEventListener('visibilitychange', () => {
        isVisible = !document.hidden;
        if (isVisible) {
            animate();
        } else {
            cancelAnimationFrame(animationFrameId);
        }
    });

    function animate() {
        if (!isVisible) return;
        animationFrameId = requestAnimationFrame(animate);

        // Group Rotations
        networkGroup.rotation.y += config.rotationSpeed;
        networkGroup.rotation.x += config.rotationSpeed * 0.5;
        
        particleGroup.rotation.y -= config.rotationSpeed * 1.5;
        particleGroup.rotation.x -= config.rotationSpeed * 0.5;

        // Node floating motion
        for (let i = 0; i < nodes.length; i++) {
            const node = nodes[i];
            node.userData.phaseX += node.userData.speedX;
            node.userData.phaseY += node.userData.speedY;
            
            node.position.x = node.userData.baseX + Math.sin(node.userData.phaseX) * 0.5;
            node.position.y = node.userData.baseY + Math.cos(node.userData.phaseY) * 0.5;
        }

        // Update connection lines
        for (let i = 0; i < connections.length; i++) {
            const conn = connections[i];
            const positions = conn.geometry.attributes.position.array;
            
            positions[0] = conn.userData.nodeA.position.x;
            positions[1] = conn.userData.nodeA.position.y;
            positions[2] = conn.userData.nodeA.position.z;
            
            positions[3] = conn.userData.nodeB.position.x;
            positions[4] = conn.userData.nodeB.position.y;
            positions[5] = conn.userData.nodeB.position.z;
            
            conn.geometry.attributes.position.needsUpdate = true;
        }

        updatePulses();

        // Parallax camera movement
        mouse.x += (mouse.targetX - mouse.x) * 0.05;
        mouse.y += (mouse.targetY - mouse.y) * 0.05;
        
        // Shift camera, max 2 units offset
        camera.position.x = mouse.x * 2;
        camera.position.y = mouse.y * 2;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    }

    // Start animation
    animate();
});
