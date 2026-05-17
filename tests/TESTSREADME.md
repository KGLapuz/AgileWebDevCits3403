# UniReviews Test Suite

This folder contains the automated unit tests for the UniReviews Flask web application.

The test suite uses:

- pytest
- Flask test client
- SQLite in-memory database
- Flask application factory pattern

The purpose of these tests is to verify that:

- routes function correctly
- authentication protections work
- database operations succeed
- users can create content correctly
- unit pages load successfully

---

# Initial Environment Setup

## 1. Create a virtual environment

From the project root directory:

### Windows

```powershell
python -m venv .venv
````

### Mac/Linux

```bash
python3 -m venv .venv
```

---

## 2. Activate the virtual environment

### Windows PowerShell

```powershell
.venv\Scripts\activate
```

### Mac/Linux

```bash
source .venv/bin/activate
```

---

## 3. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

---

## 4. Install project dependencies

If a requirements.txt file exists:

```powershell
pip install -r requirements.txt
```

Otherwise manually install the required packages:

```powershell
pip install flask
pip install flask-sqlalchemy
pip install flask-migrate
pip install flask-wtf
pip install flask-moment
pip install pytest
```

---

# Running the Application

To run the Flask server:

```powershell
python run_app.py
```

---

# Running the Tests

## Option 1 (recommended)

Run:

```powershell
python run_tests.py
```

## Option 2

Directly use pytest:

```powershell
pytest
```

or:

```powershell
pytest -v
```

---

# Understanding Test Results

## Successful Test Run

Example:

```text
================ 10 passed in 1.12s ================
```

This means all automated tests completed successfully.

---

# Failed Tests

Example:

```text
FAILED tests/test_reviews.py::test_submit_review
```

This means a specific feature failed validation.

The traceback below the failure shows:

* which file failed
* which test failed
* the exact line causing the issue
* the error message returned

---

# Common Failure Causes

## 404 NOT FOUND

Usually means:

* the tested route does not exist
* the test URL is incorrect
* required database objects were not created before the request

Example:

```text
assert 404 == 302
```

---

## IntegrityError

Usually means:

* a required database field was missing
* invalid data was inserted into the database

Example:

```text
sqlite3.IntegrityError: NOT NULL constraint failed
```

---

## AssertionError

Usually means:

* the application returned an unexpected result
* expected output does not match actual output

Example:

```text
assert response.status_code == 302
```

---

# Test Database

The test suite uses:

```python
sqlite:///:memory:
```

This creates a temporary in-memory SQLite database for every test run.

Benefits:

* isolated tests
* no permanent database modifications
* faster execution
* safer testing environment

---

# Current Test Coverage

The test suite currently validates:

* authentication redirects
* unit page loading
* review creation
* discussion creation
* project submission
* session handling
* flash messages
* comparison of meta values after and before creation

---
