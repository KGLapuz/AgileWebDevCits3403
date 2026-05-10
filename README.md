# AgileWebDevCits3403
This is a group project for CITS3403 Semester 1, 2026


## Setup & Running the Application

### 1. Clone the Repository

```bash
git clone [<repository-url>](https://github.com/KGLapuz/AgileWebDevCits3403)
cd <repository-folder>
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

### 3. Install Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 4. Seed the Database with Sample Data

Populate the SQLite database with sample users, units, reviews, discussions, comments, and projects:

```bash
python seed.py
```

> Ensure the seed script is run before starting the application so that all pages have content available.

---

### 5. Start the Flask Server

Run the application using:

```bash
python app.py
```

The Flask development server should now be running locally, typically at:

```text
http://127.0.0.1:5000
```

---

## Application Routes

The following routes are available once the server is running.

### Home Page

| Route | Description                                           |
| ----- | ----------------------------------------------------- |
| `/`   | Displays the homepage containing all available units. |

Example:

```text
http://127.0.0.1:5000/
```

---

### Unit Pages

Each unit has its own dedicated page displaying reviews, discussions, and projects related to that unit.

| Route               | Description                    |
| ------------------- | ------------------------------ |
| `/unit/<unit_code>` | Displays a specific unit page. |

Example:

```text
http://127.0.0.1:5000/unit/CITS3403
```

---

### Discussion Pages

| Route                         | Description                                                   |
| ----------------------------- | ------------------------------------------------------------- |
| `/<unit_code>/discussions`    | Displays all discussions for a unit.                          |
| `/discussion/<discussion_id>` | Displays an individual discussion thread and nested comments. |

Examples:

```text
http://127.0.0.1:5000/CITS3403/discussions
```

```text
http://127.0.0.1:5000/discussion/1
```

---

### Project Pages

| Route                    | Description                                 |
| ------------------------ | ------------------------------------------- |
| `/<unit_code>/projects`  | Displays all projects for a unit.           |
| `/projects/<project_id>` | Displays details for an individual project. |

Examples:

```text
http://127.0.0.1:5000/CITS3403/projects
```

```text
http://127.0.0.1:5000/projects/1
```

---

### Review Pages

| Route                  | Description                      |
| ---------------------- | -------------------------------- |
| `/<unit_code>/reviews` | Displays all reviews for a unit. |

Example:

```text
http://127.0.0.1:5000/CITS3403/reviews
```

---

### Test User Switching Route

A temporary development/testing route is included to simulate logging in as different users.

| Route       | Description                                      |
| ----------- | ------------------------------------------------ |
| `/set_user` | Sets the active session user via a POST request. |

This route is intended for development purposes only.
