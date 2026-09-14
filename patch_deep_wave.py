import os

for html_path in [
    os.path.expanduser('~/Desktop/AgentX-Platform/templates/index.html'),
    '/Users/apple/.gemini/antigravity/scratch/agent-platform/templates/index.html'
]:
    with open(html_path, 'r') as f:
        html = f.read()

    old_css_start = html.find('/* Antigravity-style Infinite Floating Tool Icons with Wave Motion */')
    if old_css_start != -1:
        old_css_end = html.find('</style>', old_css_start)
        new_css = """/* Antigravity-style Infinite Floating Tool Icons with Deep Wave Motion (~1.5cm / 58px) */
        .marquee-section {
            width: 100%;
            overflow: hidden;
            padding: 6.5rem 0;
            position: relative;
            background: rgba(10, 10, 26, 0.4);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            margin: 2.5rem 0;
        }

        .marquee-track {
            display: flex;
            width: max-content;
            animation: scrollMarquee 26s linear infinite;
            gap: 1.8rem;
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
            width: 76px;
            height: 76px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(12px);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.85rem;
            color: #fff;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            cursor: pointer;
            flex-shrink: 0;
            animation: deepWaveMotion 2.8s ease-in-out infinite alternate;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), background 0.3s, border-color 0.3s, box-shadow 0.3s, color 0.3s;
        }

        /* Continuous Up & Down Sinusoidal Wave Staggering (~1.5cm displacement) */
        .icon-bubble:nth-child(1), .icon-bubble:nth-child(16) { animation-delay: 0.0s; }
        .icon-bubble:nth-child(2), .icon-bubble:nth-child(17) { animation-delay: 0.2s; }
        .icon-bubble:nth-child(3), .icon-bubble:nth-child(18) { animation-delay: 0.4s; }
        .icon-bubble:nth-child(4), .icon-bubble:nth-child(19) { animation-delay: 0.6s; }
        .icon-bubble:nth-child(5), .icon-bubble:nth-child(20) { animation-delay: 0.8s; }
        .icon-bubble:nth-child(6), .icon-bubble:nth-child(21) { animation-delay: 1.0s; }
        .icon-bubble:nth-child(7), .icon-bubble:nth-child(22) { animation-delay: 1.2s; }
        .icon-bubble:nth-child(8), .icon-bubble:nth-child(23) { animation-delay: 1.4s; }
        .icon-bubble:nth-child(9), .icon-bubble:nth-child(24) { animation-delay: 1.6s; }
        .icon-bubble:nth-child(10), .icon-bubble:nth-child(25) { animation-delay: 1.8s; }
        .icon-bubble:nth-child(11), .icon-bubble:nth-child(26) { animation-delay: 2.0s; }
        .icon-bubble:nth-child(12), .icon-bubble:nth-child(27) { animation-delay: 2.2s; }
        .icon-bubble:nth-child(13), .icon-bubble:nth-child(28) { animation-delay: 2.4s; }
        .icon-bubble:nth-child(14), .icon-bubble:nth-child(29) { animation-delay: 2.6s; }
        .icon-bubble:nth-child(15), .icon-bubble:nth-child(30) { animation-delay: 2.8s; }

        @keyframes deepWaveMotion {
            0% {
                transform: translateY(-58px) rotate(-6deg);
            }
            50% {
                transform: translateY(0px) rotate(0deg);
            }
            100% {
                transform: translateY(58px) rotate(6deg);
            }
        }

        .icon-bubble:hover {
            transform: scale(1.25) translateY(-20px) !important;
            background: rgba(0, 242, 254, 0.2);
            border-color: rgba(0, 242, 254, 0.8);
            box-shadow: 0 0 35px rgba(0, 242, 254, 0.7), 0 10px 30px rgba(0, 0, 0, 0.6);
            color: #00f2fe;
            animation-play-state: paused;
        }

        /* Fade gradient masks on edges */
        .marquee-section::before,
        .marquee-section::after {
            content: '';
            position: absolute;
            top: 0;
            width: 180px;
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

print("Deep wave (~1.5cm / 58px) applied successfully!")
