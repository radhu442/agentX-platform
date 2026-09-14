import re

with open('app.py', 'r') as f:
    app_code = f.read()

new_routes = """
@app.route('/freshworks')
def freshworks():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('freshworks.html')

@app.route('/knowledge_graph')
def knowledge_graph():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('knowledge_graph.html')

@app.route('/analytics')
def analytics():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('analytics.html')

@app.route('/api_keys')
def api_keys():
    if 'user_id' not in session: return redirect(url_for('login'))
    return render_template('api_keys.html')
"""

app_code = app_code.replace("@app.route('/logout')", new_routes + "\n@app.route('/logout')")

with open('app.py', 'w') as f:
    f.write(app_code)
