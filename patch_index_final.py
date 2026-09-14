with open('templates/index.html', 'r') as f:
    html = f.read()

# Fix static paths for Flask
html = html.replace('href="css/', 'href="/static/css/')
html = html.replace('src="js/', 'src="/static/js/')

# Update nav to have Login & Register links cleanly
html = html.replace('<a href="#register" class="nav-cta">Get Access</a>', '<a href="/login" class="nav-cta" style="margin-right: 8px;">Login</a><a href="/register" class="nav-cta glowing">Register</a>')

# Update Hero CTA
html = html.replace('<a href="#register" class="btn btn-primary glowing">Request Early Access</a>', '<a href="/register" class="btn btn-primary glowing">Start Building</a>')

# In the bottom register form, make sure it routes to /register or posts cleanly
html = html.replace('<a href="#" class="logo">⚡ AgentX Platform</a>', '<a href="/" class="logo">⚡ AgentX Platform</a>')

with open('templates/index.html', 'w') as f:
    f.write(html)
