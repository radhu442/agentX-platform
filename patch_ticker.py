import os

html_path = os.path.expanduser('~/Desktop/AgentX-Platform/templates/index.html')
with open(html_path, 'r') as f:
    html = f.read()

ticker_css = """
        /* Antigravity-style Infinite Floating Tool Icons Marquee */
        .marquee-section {
            width: 100%;
            overflow: hidden;
            padding: 3rem 0;
            position: relative;
            background: rgba(10, 10, 26, 0.4);
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            margin: 2rem 0;
        }

        .marquee-track {
            display: flex;
            width: max-content;
            animation: scrollMarquee 25s linear infinite;
            gap: 1.5rem;
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
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            cursor: pointer;
            flex-shrink: 0;
        }

        .icon-bubble:hover {
            transform: scale(1.18) translateY(-6px);
            background: rgba(0, 242, 254, 0.15);
            border-color: rgba(0, 242, 254, 0.6);
            box-shadow: 0 0 25px rgba(0, 242, 254, 0.5), 0 10px 25px rgba(0, 0, 0, 0.5);
            color: #00f2fe;
        }

        /* Fade gradient masks on edges */
        .marquee-section::before,
        .marquee-section::after {
            content: '';
            position: absolute;
            top: 0;
            width: 150px;
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
    </style>
"""

html = html.replace('</style>', ticker_css)

ticker_html = """
    <!-- Antigravity-Style Floating Tool Icons Ribbon -->
    <div class="marquee-section">
        <div class="marquee-track">
            <!-- Set 1 -->
            <div class="icon-bubble" title="Code Primitives">{ }</div>
            <div class="icon-bubble" title="AI Sparkle">✦</div>
            <div class="icon-bubble" title="Skill Directory">📁</div>
            <div class="icon-bubble" title="Tool Calling">&lt; &gt;</div>
            <div class="icon-bubble" title="Semantic Search">🔍</div>
            <div class="icon-bubble" title="Terminal Prompt">⌨️</div>
            <div class="icon-bubble" title="Verification & Test">✔</div>
            <div class="icon-bubble" title="Model Context Protocol">⚯</div>
            <div class="icon-bubble" title="Agent Studio">⚙️</div>
            <div class="icon-bubble" title="Documentation">📄</div>
            <div class="icon-bubble" title="Knowledge Cube">⬡</div>
            <div class="icon-bubble" title="Deploy Pipeline">🚀</div>
            <div class="icon-bubble" title="Telemetry Loop">⟳</div>
            <div class="icon-bubble" title="Freshworks Ecosystem">⚡</div>
            <div class="icon-bubble" title="Multi-Agent Mesh">⊞</div>

            <!-- Set 2 (Duplicate for Seamless Infinite Loop) -->
            <div class="icon-bubble" title="Code Primitives">{ }</div>
            <div class="icon-bubble" title="AI Sparkle">✦</div>
            <div class="icon-bubble" title="Skill Directory">📁</div>
            <div class="icon-bubble" title="Tool Calling">&lt; &gt;</div>
            <div class="icon-bubble" title="Semantic Search">🔍</div>
            <div class="icon-bubble" title="Terminal Prompt">⌨️</div>
            <div class="icon-bubble" title="Verification & Test">✔</div>
            <div class="icon-bubble" title="Model Context Protocol">⚯</div>
            <div class="icon-bubble" title="Agent Studio">⚙️</div>
            <div class="icon-bubble" title="Documentation">📄</div>
            <div class="icon-bubble" title="Knowledge Cube">⬡</div>
            <div class="icon-bubble" title="Deploy Pipeline">🚀</div>
            <div class="icon-bubble" title="Telemetry Loop">⟳</div>
            <div class="icon-bubble" title="Freshworks Ecosystem">⚡</div>
            <div class="icon-bubble" title="Multi-Agent Mesh">⊞</div>
        </div>
    </div>

    <!-- About Section -->
"""

html = html.replace('<!-- About Section -->', ticker_html)

with open(html_path, 'w') as f:
    f.write(html)

# Also sync to scratch directory
scratch_path = '/Users/apple/.gemini/antigravity/scratch/agent-platform/templates/index.html'
with open(scratch_path, 'w') as f:
    f.write(html)

print("Successfully injected Antigravity icon marquee before 'Why AgentX Platform'!")
