with open('templates/index.html', 'r') as f:
    html = f.read()

# Replace the #register links with /register
html = html.replace('href="#register" class="nav-cta">Get Access', 'href="/login" class="nav-cta">Login</a> <a href="/register" class="nav-cta" style="margin-left: 10px;">Register')
html = html.replace('href="#register" class="btn btn-primary glowing">Request Early Access', 'href="/register" class="btn btn-primary glowing">Start Building')

# Hide or remove the on-page register section since we have a dedicated page now
import re
html = re.sub(r'<!-- Register Section -->.*?</section>', '', html, flags=re.DOTALL)

with open('templates/index.html', 'w') as f:
    f.write(html)
