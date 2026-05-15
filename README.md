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
- Study tips (“Get Ahead” tips)

All content is organised by UWA unit codes (e.g. `CITS1401`), with user-generated contributions tied to authentication and session state.

---

## Setup & Running the Application

### 1. Clone the Repository

```bash
git clone https://github.com/KGLapuz/AgileWebDevCits3403
cd AgileWebDevCits3403
````

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

### 5. Set Environment Variables (optional but recommended)

For development mode:

#### Windows (PowerShell)

```bash
set FLASK_DEBUG=True
```

#### macOS / Linux

```bash
export FLASK_DEBUG=True
```

---

### 6. Seed the Database

Populate the database with sample UWA units and users, we used CSSE units for starters:

```bash
python seed_database.py
```

[Optional] - Add sample reviews, discussions, and projects:

```bash
python seed.py
```

> Ensure seeding is completed before running the app so all pages contain content.

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

The project uses **pytest** for automated testing.

### Run all tests

```bash
python run_tests.py
```

or directly:

```bash
pytest
```

### What tests cover

The test suite validates:

* Authentication (login-required routes)
* Unit pages exist and render correctly
* Discussion creation and retrieval
* Project submission workflow
* Review creation and validation rules

### Interpreting results

* `PASSED` → Feature behaves as expected
* `FAILED` → Likely one of:

  * Missing route or incorrect URL pattern
  * Authentication/session logic not behaving as expected
  * Database constraints not met in test setup (e.g. required fields missing)
  * Validation rules rejecting expected test input
* `ERROR` → Typically:

  * Database setup issue
  * Missing test configuration (e.g. TestingConfig not applied)
  * Import/path problems in test setup

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
* Optional “Get Ahead” tips are limited to 200 characters

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

## “Get Ahead” Tips Feature

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
* Tests must run using `TestingConfig`

---

## Testing Design Philosophy

Tests are designed to validate:

* Behaviour, not implementation
* Route accessibility
* Authentication enforcement
* Database integrity constraints
* Form validation logic

---

## Common Issues

### 1. 404 instead of redirect (302)

Usually means:

* Route mismatch
* Missing dynamic parameter (`<unit_code>`)
* Blueprint not registered correctly

---

### 2. SQLite IntegrityError (NOT NULL constraint)

Usually means:

* Test data missing required model fields
* Seed/helper functions not supplying all required attributes
* Model constraints stricter than test assumptions

---

### 3. Tests pass locally but fail in CI or vice versa

Check:

* Environment config (`TestingConfig` not applied)
* Database state leakage between tests
* Session state not reset properly

---

## License

This project is for educational use as part of [[CITS3403]: Agile Web Development](https://www.handbooks.uwa.edu.au/unitdetails?code=CITS3403) at the University of Western Australia in semester 1 of 2026.

```
```
