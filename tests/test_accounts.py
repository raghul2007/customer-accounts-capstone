from unittest import TestCase
from service import app
from service.routes import reset_accounts

class AccountsTest(TestCase):
    def setUp(self):
        app.testing = True
        reset_accounts()
        self.client = app.test_client()

    def test_index(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_create(self):
        r = self.client.post("/accounts", json={"first_name":"John","last_name":"Doe","email":"john@example.com","address":"123 Main Street"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.get_json()["first_name"], "John")

    def test_list(self):
        self.client.post("/accounts", json={"first_name":"John"})
        self.assertEqual(len(self.client.get("/accounts").get_json()), 1)

    def test_read(self):
        a = self.client.post("/accounts", json={"first_name":"John","last_name":"Doe"}).get_json()
        r = self.client.get(f"/accounts/{a['id']}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["last_name"], "Doe")

    def test_update(self):
        a = self.client.post("/accounts", json={"first_name":"John"}).get_json()
        r = self.client.put(f"/accounts/{a['id']}", json={"first_name":"Jane"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["first_name"], "Jane")

    def test_delete(self):
        a = self.client.post("/accounts", json={"first_name":"John"}).get_json()
        self.assertEqual(self.client.delete(f"/accounts/{a['id']}").status_code, 204)
        self.assertEqual(self.client.get(f"/accounts/{a['id']}").status_code, 404)
