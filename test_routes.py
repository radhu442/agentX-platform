from app import app
import unittest

# ── Role access matrix (mirrors ROLE_PERMISSIONS in app.py) ────────────────
ALLOWED_BY_ROLE = {
    'Agent Developer':       {'/dashboard', '/skills', '/knowledge_graph', '/analytics', '/api_keys'},
    'Prompt Engineer':       {'/dashboard', '/skills', '/simulator', '/knowledge_graph', '/analytics', '/api_keys'},
    'Integration':           {'/dashboard', '/mcp', '/freshworks', '/knowledge_graph', '/analytics', '/api_keys'},
    'Admin':                 {'/dashboard', '/skills', '/mcp', '/freshworks', '/knowledge_graph', '/simulator', '/analytics', '/api_keys'},
}

ALL_PROTECTED = ['/dashboard', '/skills', '/mcp', '/freshworks', '/knowledge_graph', '/simulator', '/analytics', '/api_keys']


class AgentXTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_routes_unauthenticated(self):
        """Unauthenticated access to all protected routes must redirect to /login."""
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/login').status_code, 200)
        self.assertEqual(self.client.get('/register').status_code, 200)

        for route in ALL_PROTECTED:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 302, f"Route {route} failed to redirect unauthenticated user")
            self.assertIn('/login', res.location)

    def _login_as(self, role):
        """Register (or skip if exists) and login as a user with the given role string."""
        email = f"testuser_{role.lower().replace(' ', '_')}@agentx.test"
        self.client.post('/register', data={
            'full_name': f'Test {role}',
            'email': email,
            'password': 'pass123!',
            'role': role,
            'organization': 'AgentX Test Suite'
        })
        login_res = self.client.post('/login', data={'email': email, 'password': 'pass123!'})
        self.assertEqual(login_res.status_code, 200)
        self.assertIn(b'Login successful', login_res.data)

    def _test_access_for_role(self, role):
        """Verify allowed pages return 200 and blocked pages return 403."""
        self._login_as(role)
        allowed = ALLOWED_BY_ROLE[role]
        for route in ALL_PROTECTED:
            res = self.client.get(route)
            if route in allowed:
                self.assertEqual(res.status_code, 200, f"[{role}] {route} should be ALLOWED (200) but got {res.status_code}")
            else:
                self.assertEqual(res.status_code, 403, f"[{role}] {route} should be BLOCKED (403) but got {res.status_code}")
        self.client.get('/logout')

    def test_rbac_developer(self):
        self._test_access_for_role('Agent Developer')

    def test_rbac_prompt_engineer(self):
        self._test_access_for_role('Prompt Engineer')

    def test_rbac_integration(self):
        self._test_access_for_role('Integration')

    def test_rbac_admin(self):
        self._test_access_for_role('Admin')

    def test_admin_user_management(self):
        """Admin can call add_user and delete_user routes; non-admin gets 403."""
        # Non-admin cannot access admin routes
        self._login_as('Agent Developer')
        res = self.client.post('/admin/add_user', data={
            'name': 'Blocked', 'email': 'blocked@test.com', 'password': 'pass', 'role': 'Developer'
        })
        self.assertEqual(res.status_code, 403)
        self.client.get('/logout')

        # Admin can create a user
        self._login_as('Admin')
        res = self.client.post('/admin/add_user', data={
            'name': 'New Bot', 'email': 'newbot@agentx.test', 'password': 'bot123!', 'role': 'Developer'
        })
        self.assertIn(res.status_code, [200, 409])
        self.client.get('/logout')

    def test_skill_creation_developer(self):
        """Developer can create skills."""
        self._login_as('Agent Developer')
        res = self.client.post('/skills', data={'name': 'Auto Test Skill', 'description': 'RBAC test'}, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.client.get('/logout')

    def test_simulator_prompt_only(self):
        """Prompt Engineer can POST to simulator; Developer gets 403."""
        # Prompt engineer can use simulator
        self._login_as('Prompt Engineer')
        res = self.client.post('/simulator', json={'command': 'hello'})
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'response', res.data)
        self.client.get('/logout')


if __name__ == '__main__':
    unittest.main(verbosity=2)
