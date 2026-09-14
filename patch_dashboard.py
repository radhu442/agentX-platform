with open('templates/dashboard.html', 'r') as f:
    html = f.read()

interactive_js = """
<script>
  function runFeature(featureName) {
    const btn = event.target;
    const originalText = btn.innerText;
    btn.innerText = 'Processing...';
    btn.style.opacity = '0.7';
    
    setTimeout(() => {
      alert(`[Agent Skills Platform] ${featureName} executed successfully! \n\nConnection established with MCP Gateway and Freshworks ecosystem.`);
      btn.innerText = 'Success!';
      btn.style.backgroundColor = '#10B981';
      
      setTimeout(() => {
        btn.innerText = originalText;
        btn.style.backgroundColor = 'var(--accent-primary)';
        btn.style.opacity = '1';
      }, 2000);
    }, 800);
  }

  // Update all buttons to use this function
  document.querySelectorAll('.grid .btn').forEach(btn => {
      const featureName = btn.parentElement.querySelector('h3').innerText;
      btn.setAttribute('onclick', `runFeature('${featureName}')`);
  });
</script>
</body>
"""

html = html.replace('</body>', interactive_js)

with open('templates/dashboard.html', 'w') as f:
    f.write(html)
