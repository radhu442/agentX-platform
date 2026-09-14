import os

for html_path in [
    os.path.expanduser('~/Desktop/AgentX-Platform/templates/index.html'),
    '/Users/apple/.gemini/antigravity/scratch/agent-platform/templates/index.html'
]:
    with open(html_path, 'r') as f:
        html = f.read()

    # Replace the marquee-section and icon-bubble CSS with wave animation
    old_css_start = html.find('/* Antigravity-style Infinite Floating Tool Icons Marquee */')
    if old_css_start != -1:
        old_css_end = html.find('</style>', old_css_start)
        new_css = """/* Antigravity-style Infinite Floating Tool Icons with Wave Motion */
        .marquee-section {
            width: 100%;
            overflow: hidden;
            padding: 4.5rem 0;
            position: relative;
            background: rgba(10, 10, 26, 0.4);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            margin: 2rem 0;
        }

        .marquee-track {
            display: flex;
            width: max-content;
            animation: scrollMarquee 28s linear infinite;
            gap: 1.6rem;
            align-items: center;
        }

        .marquee-track:hover {
            animation-play-state: paused;
        }

        @keyframes scrollMarquee {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }

        .icon-bubble {
            width: 72px;
            height: 72px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            color: #fff;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            cursor: pointer;
            flex-shrink: 0;
            animation: waveMotion 3.2s ease-in-out infinite alternate;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s, border-color 0.3s, box-shadow 0.3s, color 0.3s;
        }

        /* Continuous Up & Down Sinusoidal Wave Staggering */
        .icon-bubble:nth-child(1), .icon-bubble:nth-child(16) { animation-delay: 0.0s; }
        .icon-bubble:nth-child(2), .icon-bubble:nth-child(17) { animation-delay: 0.22s; }
        .icon-bubble:nth-child(3), .icon-bubble:nth-child(18) { animation-delay: 0.44s; }
        .icon-bubble:nth-child(4), .icon-bubble:nth-child(19) { animation-delay: 0.66s; }
        .icon-bubble:nth-child(5), .icon-bubble:nth-child(20) { animation-delay: 0.88s; }
        .icon-bubble:nth-child(6), .icon-bubble:nth-child(21) { animation-delay: 1.10s; }
        .icon-bubble:nth-child(7), .icon-bubble:nth-child(22) { animation-delay: 1.32s; }
        .icon-bubble:nth-child(8), .icon-bubble:nth-child(23) { animation-delay: 1.54s; }
        .icon-bubble:nth-child(9), .icon-bubble:nth-child(24) { animation-delay: 1.76s; }
        .icon-bubble:nth-child(10), .icon-bubble:nth-child(25) { animation-delay: 1.98s; }
        .icon-bubble:nth-child(11), .icon-bubble:nth-child(26) { animation-delay: 2.20s; }
        .icon-bubble:nth-child(12), .icon-bubble:nth-child(27) { animation-delay: 2.42s; }
        .icon-bubble:nth-child(13), .icon-bubble:nth-child(28) { animation-delay: 2.64s; }
        .icon-bubble:nth-child(14), .icon-bubble:nth-child(29) { animation-delay: 2.86s; }
        .icon-bubble:nth-child(15), .icon-bubble:nth-child(30) { animation-delay: 3.08s; }

        @keyframes waveMotion {
            0% {
                transform: translateY(-22px) rotate(-3deg);
            }
            50% {
                transform: translateY(0px) rotate(0deg);
            }
            100% {
                transform: translateY(22px) rotate(3deg);
            }
        }

        .icon-bubble:hover {
            transform: scale(1.22) translateY(-10px) !important;
            background: rgba(0, 242, 254, 0.18);
            border-color: rgba(0, 242, 254, 0.7);
            box-shadow: 0 0 30px rgba(0, 242, 254, 0.6), 0 10px 30px rgba(0, 0, 0, 0.5);
            color: #00f2fe;
            animation-play-state: paused;
        }

        /* Fade gradient masks on edges */
        .marquee-section::before,
        .marquee-section::after {
            content: '';
            position: absolute;
            top: 0;
            width: 160px;
            height: 100%;
            z-index: 2;
            pointer-events: none;
        }

        .marquee-section::before {
            left: 0;
            background: linear-gradient(90deg, #0a0a1a, transparent);
        }

        .marquee-section::after {
            right: 0;
            background: linear-gradient(-90deg, #0a0a1a, transparent);
        }
    """
        html = html[:old_css_start] + new_css + html[old_css_end:]
        with open(html_path, 'w') as f:
            f.write(html)

print("Wave animation applied successfully!")
