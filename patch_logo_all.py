import os
import glob

dirs = [
    os.path.expanduser('~/Desktop/AgentX-Platform/templates'),
    '/Users/apple/.gemini/antigravity/scratch/agent-platform/templates'
]

for d in dirs:
    for fpath in glob.glob(os.path.join(d, '*.html')):
        with open(fpath, 'r') as f:
            html = f.read()

        # Update index.html navbar and footer logo
        if 'index.html' in fpath:
            html = html.replace(
                '<a href="/" class="logo">⚡ AgentX Platform</a>',
                '<a href="/" class="logo" style="text-decoration:none;"><img src="/static/logo.png" alt="AgentX Platform" style="height: 48px; width: auto; object-fit: contain; filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.5)); transition: transform 0.2s;" onmouseover="this.style.transform=\'scale(1.05)\'" onmouseout="this.style.transform=\'scale(1)\'"></a>'
            )
            # Clean up text styles for .logo in CSS if any
            html = html.replace(
                '.logo {\n            display: flex;\n            align-items: center;\n            gap: 0.6rem;\n            font-size: 1.4rem;\n            font-weight: 700;\n            color: #fff;\n            text-decoration: none;\n            filter: drop-shadow(0 0 12px rgba(0, 242, 254, 0.8));\n            animation: neonGlow 2.5s infinite alternate;\n        }',
                '.logo {\n            display: flex;\n            align-items: center;\n            text-decoration: none;\n        }'
            )
        
        # Update sidebar in dashboard & internal pages
        else:
            html = html.replace(
                '<div class="logo">⚡ AgentX</div>',
                '<div class="logo" style="text-align:center; margin-bottom: 2rem;"><a href="/dashboard"><img src="/static/logo.png" alt="AgentX Platform" style="max-width: 190px; height: auto; object-fit: contain; filter: drop-shadow(0 0 12px rgba(56, 189, 248, 0.6)); transition: transform 0.2s;" onmouseover="this.style.transform=\'scale(1.05)\'" onmouseout="this.style.transform=\'scale(1)\'"></a></div>'
            )

        with open(fpath, 'w') as f:
            f.write(html)

print("Updated logo image across all templates!")
