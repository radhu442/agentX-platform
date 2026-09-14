"""
Bulk-update all dashboard template sidebars to conditionally show/hide nav items
based on the `allowed_pages` variable injected by the Flask context processor.
Restricted items are shown as dimmed with a 🔒 lock icon for non-permitted roles.
"""

import os
import re

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

# The old nav items to find and replace (these are the hardcoded links in each template)
# We'll find each nav item pattern and add an `{% if %}` guard around restricted ones.

REPLACEMENTS = [
    # Skills - blocked for integration
    (
        r'<a href="/skills" class="nav-item(?:[^"]*)">(.*?)</a>',
        lambda m: (
            '{{% if \'skills\' in allowed_pages %}}\n'
            '      <a href="/skills" class="nav-item{act}">⚙️ SKILL REGISTRY</a>\n'
            '      {{% else %}}\n'
            '      <span class="nav-item disabled">⚙️ SKILL REGISTRY <span class="lock-icon">🔒</span></span>\n'
            '      {{% endif %}}'
        ).format(act=' active' if 'active' in m.group(0) else '')
    ),
    # MCP - blocked for developer, prompt
    (
        r'<a href="/mcp" class="nav-item(?:[^"]*)">(.*?)</a>',
        lambda m: (
            '{{% if \'mcp\' in allowed_pages %}}\n'
            '      <a href="/mcp" class="nav-item{act}">🔗 MCP BRIDGES</a>\n'
            '      {{% else %}}\n'
            '      <span class="nav-item disabled">🔗 MCP BRIDGES <span class="lock-icon">🔒</span></span>\n'
            '      {{% endif %}}'
        ).format(act=' active' if 'active' in m.group(0) else '')
    ),
    # Freshworks - blocked for developer, prompt
    (
        r'<a href="/freshworks" class="nav-item(?:[^"]*)">(.*?)</a>',
        lambda m: (
            '{{% if \'freshworks\' in allowed_pages %}}\n'
            '      <a href="/freshworks" class="nav-item{act}">🚀 FRESHWORKS DEPLOYER</a>\n'
            '      {{% else %}}\n'
            '      <span class="nav-item disabled">🚀 FRESHWORKS DEPLOYER <span class="lock-icon">🔒</span></span>\n'
            '      {{% endif %}}'
        ).format(act=' active' if 'active' in m.group(0) else '')
    ),
    # Simulator - blocked for developer, integration
    (
        r'<a href="/simulator" class="nav-item(?:[^"]*)">(.*?)</a>',
        lambda m: (
            '{{% if \'simulator\' in allowed_pages %}}\n'
            '      <a href="/simulator" class="nav-item{act}">🤖 AGENT SIMULATOR</a>\n'
            '      {{% else %}}\n'
            '      <span class="nav-item disabled">🤖 AGENT SIMULATOR <span class="lock-icon">🔒</span></span>\n'
            '      {{% endif %}}'
        ).format(act=' active' if 'active' in m.group(0) else '')
    ),
]

# Also add a CSS rule for disabled nav items if missing
DISABLED_CSS = '''    .nav-item.disabled {
      opacity: 0.28;
      cursor: not-allowed;
      pointer-events: none;
    }
    .lock-icon { font-size: 0.7rem; margin-left: auto; }
'''

CSS_ANCHOR = '.nav-item.logout {'  # Insert before this

updated = 0
for fname in os.listdir(TEMPLATES_DIR):
    if not fname.endswith('.html'):
        continue
    if fname in ('access_denied.html', 'index.html', 'login.html', 'register.html'):
        continue

    fpath = os.path.join(TEMPLATES_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Skip if already updated
    if 'allowed_pages' in content and 'lock-icon' in content:
        print(f'  [SKIP] {fname} — already updated')
        continue

    # Apply nav item replacements
    for pattern, replacement_fn in REPLACEMENTS:
        content = re.sub(pattern, replacement_fn, content)

    # Add CSS for disabled nav items if not already there
    if '.nav-item.disabled' not in content and CSS_ANCHOR in content:
        content = content.replace(CSS_ANCHOR, DISABLED_CSS + '    ' + CSS_ANCHOR)

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  [OK]   {fname} — sidebar updated')
        updated += 1
    else:
        print(f'  [SKIP] {fname} — no changes needed')

print(f'\nDone. {updated} template(s) updated.')
