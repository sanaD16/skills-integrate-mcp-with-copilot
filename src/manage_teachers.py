import argparse
import json
from getpass import getpass

from teacher_auth import TEACHERS_FILE, create_password_record


def main() -> None:
    parser = argparse.ArgumentParser(description="Add or reset a teacher login")
    parser.add_argument("username")
    args = parser.parse_args()
    username = args.username.strip()
    if not username:
        parser.error("username cannot be empty")

    password = getpass("Teacher password: ")
    confirmation = getpass("Confirm password: ")
    if not password or password != confirmation:
        parser.error("passwords must be non-empty and match")

    if TEACHERS_FILE.exists():
        data = json.loads(TEACHERS_FILE.read_text(encoding="utf-8"))
    else:
        data = {"teachers": {}}
    teachers = data.setdefault("teachers", {})
    if not isinstance(teachers, dict):
        parser.error("teachers.json must contain a teachers object")

    teachers[username] = create_password_record(password)
    TEACHERS_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Teacher login saved for {username}")


if __name__ == "__main__":
    main()