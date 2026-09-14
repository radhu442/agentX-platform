with open('templates/dashboard.html', 'r') as f:
    html = f.read()

# Add Modal CSS
modal_css = """
    /* Custom Modal Styles */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(15, 23, 42, 0.8);
      backdrop-filter: blur(10px);
      z-index: 9999;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.3s ease;
    }
    .modal-overlay.active {
      opacity: 1;
      pointer-events: auto;
    }
    .modal-box {
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid rgba(0, 242, 254, 0.4);
      box-shadow: 0 0 30px rgba(79, 172, 254, 0.2), inset 0 0 20px rgba(240, 147, 251, 0.1);
      border-radius: 16px;
      padding: 2.5rem;
      max-width: 450px;
      text-align: center;
      transform: translateY(20px) scale(0.95);
      transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .modal-overlay.active .modal-box {
      transform: translateY(0) scale(1);
    }
    .modal-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
      text-shadow: 0 0 20px rgba(0, 242, 254, 0.8);
    }
    .modal-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 0.75rem;
      background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #f093fb 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .modal-message {
      color: var(--text-gray);
      line-height: 1.6;
      margin-bottom: 2rem;
    }
    .modal-close-btn {
      background: linear-gradient(45deg, #00f2fe, #f093fb);
      border: none;
      border-radius: 8px;
      color: white;
      font-weight: 600;
      padding: 10px 24px;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
      transition: all 0.2s;
    }
    .modal-close-btn:hover {
      transform: scale(1.05);
      box-shadow: 0 6px 20px rgba(240, 147, 251, 0.6);
    }
  </style>
"""
html = html.replace('</style>', modal_css)

# Add Modal HTML right after <body>
modal_html = """
<body>
  <div id="customModal" class="modal-overlay">
    <div class="modal-box">
      <div class="modal-icon" id="modalIcon">✨</div>
      <h2 class="modal-title" id="modalTitle">Success!</h2>
      <p class="modal-message" id="modalMessage">Operation completed.</p>
      <button class="modal-close-btn" onclick="closeModal()">Acknowledge</button>
    </div>
  </div>
"""
html = html.replace('<body>', modal_html)

# Update the JS to use the custom modal and fix the sidebar
js_update = """
<script>
  function showModal(title, message, icon = '✨') {
    document.getElementById('modalIcon').innerText = icon;
    document.getElementById('modalTitle').innerText = title;
    document.getElementById('modalMessage').innerText = message;
    document.getElementById('customModal').classList.add('active');
  }

  function closeModal() {
    document.getElementById('customModal').classList.remove('active');
  }

  function runFeature(featureName) {
    const btn = event.target;
    const originalText = btn.innerText;
    btn.innerText = 'Processing...';
    btn.style.opacity = '0.7';
    
    setTimeout(() => {
      showModal(
        featureName + ' Executed', 
        'Connection established with MCP Gateway and Freshworks ecosystem successfully. All data synchronized.',
        '🚀'
      );
      btn.innerText = 'Success!';
      btn.style.backgroundColor = '#10B981';
      
      setTimeout(() => {
        btn.innerText = originalText;
        btn.style.backgroundColor = 'var(--accent-primary)';
        btn.style.opacity = '1';
      }, 2000);
    }, 800);
  }

  // Bind grid buttons
  document.querySelectorAll('.grid .btn').forEach(btn => {
      const featureName = btn.parentElement.querySelector('h3').innerText;
      btn.setAttribute('onclick', `runFeature('${featureName}')`);
  });

  // Fix Sidebar interactions
  document.querySelectorAll('.sidebar .nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
      // Ignore logout button
      if(item.innerText === 'Logout') return;
      
      e.preventDefault();
      
      // Update active state
      document.querySelectorAll('.sidebar .nav-item').forEach(nav => nav.classList.remove('active'));
      item.classList.add('active');
      
      const menuName = item.innerText;
      
      // Show modal to acknowledge navigation
      if(menuName !== 'Dashboard') {
         showModal(
           menuName, 
           `The ${menuName} interface is securely loading. Fetching your environment configurations...`,
           '⚡'
         );
      }
    });
  });
</script>
</body>
"""

import re
html = re.sub(r'<script>.*?</script>\s*</body>', js_update, html, flags=re.DOTALL)

with open('templates/dashboard.html', 'w') as f:
    f.write(html)
