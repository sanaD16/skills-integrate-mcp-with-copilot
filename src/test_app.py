import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

import app as app_module
import teacher_auth


class TeacherAuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.teachers_file = Path(self.temp_dir.name) / "teachers.json"
        self.teachers_file.write_text(
            json.dumps({"teachers": {"teacher": teacher_auth.create_password_record("correct-password")}}),
            encoding="utf-8",
        )
        self.teachers_file_patch = patch.object(teacher_auth, "TEACHERS_FILE", self.teachers_file)
        self.teachers_file_patch.start()
        app_module.sessions.clear()
        self.client = TestClient(app_module.app)
        self.activity = "Chess Club"
        self.original_participants = list(app_module.activities[self.activity]["participants"])

    def tearDown(self):
        app_module.activities[self.activity]["participants"] = self.original_participants
        app_module.sessions.clear()
        self.teachers_file_patch.stop()
        self.temp_dir.cleanup()

    def test_activity_list_is_public_but_mutations_require_login(self):
        self.assertEqual(self.client.get("/activities").status_code, 200)

        signup_response = self.client.post(
            f"/activities/{self.activity}/signup", params={"email": "student@mergington.edu"}
        )
        unregister_response = self.client.delete(
            f"/activities/{self.activity}/unregister",
            params={"email": self.original_participants[0]},
        )

        self.assertEqual(signup_response.status_code, 401)
        self.assertEqual(unregister_response.status_code, 401)
        self.assertEqual(app_module.activities[self.activity]["participants"], self.original_participants)

    def test_teacher_can_sign_up_unregister_and_log_out(self):
        bad_login = self.client.post(
            "/login", json={"username": "teacher", "password": "wrong-password"}
        )
        self.assertEqual(bad_login.status_code, 401)

        login_response = self.client.post(
            "/login", json={"username": "teacher", "password": "correct-password"}
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("httponly", login_response.headers["set-cookie"].lower())
        self.assertEqual(self.client.get("/auth/status").json(), {"authenticated": True})

        email = "new-student@mergington.edu"
        signup_response = self.client.post(
            f"/activities/{self.activity}/signup", params={"email": email}
        )
        self.assertEqual(signup_response.status_code, 200)

        unregister_response = self.client.delete(
            f"/activities/{self.activity}/unregister", params={"email": email}
        )
        self.assertEqual(unregister_response.status_code, 200)

        self.assertEqual(self.client.post("/logout").status_code, 200)
        self.assertEqual(self.client.get("/auth/status").json(), {"authenticated": False})
        self.assertEqual(
            self.client.post(f"/activities/{self.activity}/signup", params={"email": email}).status_code,
            401,
        )


if __name__ == "__main__":
    unittest.main()