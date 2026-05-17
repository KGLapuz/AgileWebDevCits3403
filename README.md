# AgileWebDevCits3403

This is a group project for **CITS3403 – Agile Web Development (Semester 1, 2026)** at the University of Western Australia.

CONTRIBUTORS:
|UWA ID  |NAME            |GITHUB USERNAME       |
|--------|----------------|----------------------|
|24177482|Mambwe M Nsanje |mambwensanje          |
|24313991|Bronte Watts    |brontewatts           |
|24803486|Keithlin Lapuz  |KGLapuz               |


The application is a **UniReviews platform** where students can view and contribute:
- Unit reviews
- Discussion threads
- Project ideas and submissions
- Study tips ("Get Ahead" tips)

All content is organised by UWA unit codes (e.g. `CITS1401`), with user-generated contributions tied to authentication and session state.

---

## Setup & Running the Application

### 1. Clone the Repository

```bash
git clone https://github.com/KGLapuz/AgileWebDevCits3403
cd AgileWebDevCits3403
```

---

### 2. Create and Activate a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Upgrade pip (recommended)

```bash
python -m pip install --upgrade pip
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Set Environment Variables

This project requires a secret key for Flask session security. **Do not hardcode secrets into the codebase.**

#### I. Create a `.env` file

In the root directory of the project, create a file named:

```
.env
```

Add the following variables:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
```

You can generate a secure secret key using Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### II. Install dependencies for environment loading

If not already installed:

```bash
pip install python-dotenv
```

#### III. Ensure environment variables are loaded

Make sure your application loads the `.env` file before running. In your main entry file (e.g. `app.py`):

```python
from dotenv import load_dotenv
load_dotenv()
```

#### IV. Do NOT commit `.env`

Ensure your `.env` file is excluded from version control:

```
.env
```

(Already included in `.gitignore`)

#### Security Note

The `SECRET_KEY` is used to secure user sessions and protect against tampering. Never share or expose this value publicly or commit it to Git.

---

### 6. Seed the Database

Populate the database with sample UWA units and users, we used CSSE units for starters:

```bash
python seed_database.py
```

---

### 7. Run the Application

Recommended entry point:

```bash
python run_app.py
```

The app will be available at:

```
http://127.0.0.1:5000
```

---

## Running Tests

The project uses Python's built-in **unittest** framework for automated testing.

### Run all tests

```bash
python run_tests.py
```

Tests are discovered automatically from the `tests/` directory. Each test file follows the `test_*.py` naming convention and each test function is prefixed with `test_`.

### Test structure

Each test class:
- Extends `unittest.TestCase`
- Uses `setUp` to spin up a fresh in-memory SQLite database and populate it with helper data before every test
- Uses `tearDown` to drop all tables and pop the app context after every test, ensuring no state leaks between tests

### What tests cover

The test suite validates:

* User Model (Auth & Session Flow): Password hashing, uniqueness constraints, and role defaults are tested via successful login/logout routing, registration pipelines, and UI flash errors for missing or duplicate credentials.
* Unit & Review Models (Submission & Metrics): Validation rules, optional fields, and relationships are tested by verifying that logged-in users can submit complete review forms to update dynamic list views, while unauthenticated guests are automatically redirected to login.
* Discussion & Comment Models (Interactivity & Hierarchy): Content constraints, linkage requirements, and auto-incrementing reply counts are tested via deep UI page traversal, verifying that authenticated users can post top-level thread comments and nested replies while guests trigger a flash warning.
* Project Model (Global Pipeline): Model relationships, structural constraints, and optional field inputs are tested via a standalone global submission pipeline that successfully renders custom project entries directly into the extended template listing view.

### Interpreting results

Each test prints its name and result to the terminal when run with `verbosity=2`:

* `OK` → Feature behaves as expected
* `FAIL` → An `assert` method did not hold — check the printed traceback for which assertion failed and why
* `ERROR` → The test itself raised an unexpected exception before reaching any assertion — typically caused by:
  * A missing or misconfigured `TestingConfig`
  * Import or path errors in the test setup
  * A database constraint violation in a helper function

---

## Application Overview

### Home Page

| Route | Description                  |
| ----- | ---------------------------- |
| `/`   | Displays all available units |

---

### Unit Pages

| Route               | Description                   |
| ------------------- | ----------------------------- |
| `/unit/<unit_code>` | Displays a specific unit page |

Example:

```
/unit/CITS1401
```

---

### Reviews

| Route                        | Description                          |
| ---------------------------- | ------------------------------------ |
| `/<unit_code>/reviews`       | Displays all reviews for a unit      |
| `/<unit_code>/create_review` | Create a new review (login required) |

#### Review rules

* Users must be logged in to submit reviews
* Rating must be between 1 and 5 stars
* Workload must be between 1 and 20 hours
* Review content must be at least 30 characters
* Optional "Get Ahead" tips are limited to 200 characters

---

### Discussions

| Route                            | Description                          |
| -------------------------------- | ------------------------------------ |
| `/<unit_code>/discussions`       | View all discussions for a unit      |
| `/<unit_code>/create_discussion` | Create a discussion (login required) |
| `/discussion/<discussion_id>`    | View discussion thread               |

---

### Projects

| Route                         | Description                       |
| ----------------------------- | --------------------------------- |
| `/<unit_code>/projects`       | View all projects                 |
| `/<unit_code>/submit_project` | Submit a project (login required) |
| `/projects/<project_id>`      | View project details              |

---

## Authentication & Session Behaviour

### Login system

* Users authenticate via a login form
* On success, `user_id` is stored in the session
* Session state determines access to restricted actions

### Logout

* Logging out clears the session `user_id`
* This prevents access to:
  * Creating reviews
  * Posting discussions
  * Submitting projects

### Access control rules

Certain actions require authentication:

* Create review
* Create discussion
* Submit project

If a user is not logged in:

* They are redirected to the login page
* A flash message explains the requirement

---

## "Get Ahead" Tips Feature

Each unit supports optional **Get Ahead tips**, which allow students to:

* Share preparation advice before semester start
* Provide study strategies
* Share what caught them off guard

Rules:

* Optional field (can be left blank)
* Maximum 200 characters
* Stored as `NULL` if empty

---

## Notes for Developers

* Flask app uses application factory pattern (`create_app`)
* Config classes:
  * `DevelopmentConfig`
  * `TestingConfig` (uses in-memory SQLite + CSRF disabled)
* Database is managed via SQLAlchemy + Flask-Migrate
* All tests must run under `TestingConfig` — this is applied automatically via `run_tests.py`

---

## Testing Design Philosophy

Tests are designed to validate:

* Behaviour, not implementation
* Database integrity constraints
* Model property correctness
* Nullable and uniqueness constraint enforcement
* Authentication logic (password hashing, `authenticate()` method)

---

## Common Issues

### 1. 404 instead of redirect (302)

Usually means:

* Route mismatch
* Missing dynamic parameter (`<unit_code>`)
* Blueprint not registered correctly

---

### 2. `IntegrityError` (NOT NULL or UNIQUE constraint)

Usually means:

* Test data missing required model fields
* Helper functions not supplying all required attributes
* Model constraints stricter than test assumptions

---

### 3. `ERROR` instead of `FAIL` on a test

Usually means:

* `TestingConfig` not applied — check `create_app` accepts a config argument
* Database state not cleaned up — confirm `tearDown` calls `db.drop_all()` and `db.session.remove()`
* Import path issue — confirm `tests/` is discoverable from the project root

---

## License

This project is for educational use as part of [[CITS3403]: Agile Web Development](https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3403) at the University of Western Australia in semester 1 of 2026.

```
Disclaimer: This application is a student-built educational tool and is not affiliated with, endorsed by, or representative of the University of Western Australia; all official unit information is sourced directly from the [UWA Handbook](https://www.handbooks.uwa.edu.au/) and users should refer there for authoritative and up-to-date unit details.
```