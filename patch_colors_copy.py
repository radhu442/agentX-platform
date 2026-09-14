import os

for html_path in [
    os.path.expanduser('~/Desktop/AgentX-Platform/templates/index.html'),
    '/Users/apple/.gemini/antigravity/scratch/agent-platform/templates/index.html'
]:
    with open(html_path, 'r') as f:
        html = f.read()

    # 1. Update the badge text and styling from "🚀 Platform Agent Skills & Knowledge" to a polished enterprise badge
    old_badge_html = '<div class="badge">🚀 Platform Agent Skills & Knowledge</div>'
    new_badge_html = '<div class="badge"><span class="badge-dot"></span> Next-Gen Agentic Architecture</div>'
    html = html.replace(old_badge_html, new_badge_html)

    # 2. Modernize the typography and humanize the hero copy
    old_h1 = '<h1>\n            Empower Agents with<br>\n            <span class="gradient-text" id="typing-text">Freshworks Platform</span>\n        </h1>'
    new_h1 = '<h1 class="hero-headline">\n            Orchestrate Intelligent Agents with<br>\n            <span class="gradient-text" id="typing-text">Freshworks Studio</span>\n        </h1>'
    html = html.replace(old_h1, new_h1)

    old_p = '<p>\n            The definitive platform for building reusable skills, orchestrating MCP integrations, and deploying context-aware AI on the Freshworks developer platform.\n        </p>'
    new_p = '<p class="hero-subtext">\n            A unified developer hub to create modular agent skills, bridge live enterprise data via Model Context Protocol, and deploy automated CX & EX workflows directly into Freshworks.\n        </p>'
    html = html.replace(old_p, new_p)

    # 3. Refine Button & Glow Colors: Replace hot neon pink/magenta with high-end Cupertino/Linear Electric Indigo, Cyan & Crisp White
    # Update CSS in index.html
    html = html.replace(
        '--accent-pink: #f093fb;',
        '--accent-indigo: #6366f1;\n            --accent-glow: #38bdf8;'
    )
    
    # Refine Register button in Nav & CTA
    html = html.replace(
        'background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);\n            border: 1px solid rgba(236, 72, 153, 0.5);\n            color: #fff;\n            box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4);',
        'background: #ffffff;\n            border: 1px solid rgba(255, 255, 255, 0.9);\n            color: #090d16;\n            box-shadow: 0 4px 24px rgba(255, 255, 255, 0.25);'
    )
    html = html.replace(
        'box-shadow: 0 8px 30px rgba(236, 72, 153, 0.7);',
        'box-shadow: 0 8px 32px rgba(255, 255, 255, 0.45); transform: translateY(-2px);'
    )

    # Refine Gradient Text
    html = html.replace(
        'background: linear-gradient(135deg, #00f2fe 0%, #a855f7 50%, #f093fb 100%);',
        'background: linear-gradient(135deg, #38bdf8 0%, #818cf8 60%, #c084fc 100%);'
    )

    # Refine Badge CSS
    badge_css_old = """.badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.45rem 1.2rem;
            border-radius: 50px;
            background: rgba(168, 85, 247, 0.15);
            border: 1px solid rgba(168, 85, 247, 0.4);
            color: #c084fc;
            font-size: 0.88rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);
        }"""

    badge_css_new = """.badge {
            display: inline-flex;
            align-items: center;
            gap: 0.6rem;
            padding: 0.4rem 1.1rem;
            border-radius: 9999px;
            background: rgba(56, 189, 248, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.25);
            color: #7dd3fc;
            font-size: 0.85rem;
            font-weight: 500;
            letter-spacing: 0.3px;
            margin-bottom: 1.8rem;
            backdrop-filter: blur(12px);
        }
        .badge-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #38bdf8;
            box-shadow: 0 0 10px #38bdf8;
            animation: pulseDot 2s infinite;
        }
        @keyframes pulseDot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }
        .hero-headline {
            font-size: 3.6rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            line-height: 1.12;
            margin-bottom: 1.4rem;
            color: #f8fafc;
        }
        .hero-subtext {
            font-size: 1.15rem;
            color: #94a3b8;
            max-width: 680px;
            line-height: 1.65;
            font-weight: 400;
            margin-bottom: 2.5rem;
        }"""

    if badge_css_old in html:
        html = html.replace(badge_css_old, badge_css_new)

    # Refine CTA buttons on hero
    html = html.replace(
        '<a href="/register" class="btn btn-primary" style="padding: 0.85rem 2rem; font-size: 1.05rem;">Start Building 🚀</a>',
        '<a href="/register" class="btn" style="background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%); color: #ffffff; padding: 0.85rem 2.2rem; font-size: 1rem; font-weight: 600; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);">Get Started Free →</a>'
    )
    html = html.replace(
        '<a href="#skills" class="btn btn-outline" style="padding: 0.85rem 2rem; font-size: 1.05rem;">Explore Capabilities</a>',
        '<a href="#skills" class="btn btn-outline" style="padding: 0.85rem 2.2rem; font-size: 1rem; border-radius: 10px;">Explore Platform</a>'
    )

    # 4. Refine typing words
    html = html.replace(
        'const words = ["Freshworks Platform", "Reusable Skills", "Model Context Protocol", "Autonomous Agents"];',
        'const words = ["Freshworks Studio", "Reusable Skills", "Model Context Protocol", "Multi-Agent Workflows"];'
    )

    with open(html_path, 'w') as f:
        f.write(html)

print("Polished hero badge, colors, typography, and humanized copy successfully!")
