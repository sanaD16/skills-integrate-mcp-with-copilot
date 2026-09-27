# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Teacher login to register and unregister students
- Public viewing of activities and current participants

## Getting Started

1. Install the dependencies:

   ```
   pip install -r ../requirements.txt
   ```

2. Run the application:

   ```
   uvicorn app:app --reload
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/login`                                                          | Log in as a teacher                                                 |
| POST   | `/logout`                                                         | Log out                                                             |
| GET    | `/auth/status`                                                    | Check whether the current browser has a teacher session              |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up a student (teacher session required)                        |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student (teacher session required)                  |

## Teacher Accounts

Teacher credentials are read from `teachers.json` next to `app.py`. The file is local and ignored by Git; `teachers.example.json` shows its structure. Create or reset an account from the `src` directory with:

```
python manage_teachers.py teacher-username
```

The command prompts for the password and stores a salted PBKDF2 hash rather than the password itself. Install the test dependency and run the API tests with:

```
pip install -r ../requirements-dev.txt
python -m unittest test_app
```

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
