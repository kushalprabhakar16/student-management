# Student Management System

A complete Student Management System built with **Flask**, **SQLite**, **SQLAlchemy ORM**, and a responsive **Bootstrap 5** frontend using **Jinja2** templates.

## Project Overview

This web application lets you manage student records through a browser UI and a REST API. Students have an ID, name, age, email, marks list, and the system auto-calculates the average and letter grade (A+ to F).

## Features

- Full CRUD REST API for students
- Auto-calculated average and letter grade
- Responsive dashboard with stat cards
- Add Student form with client-side + server-side validation
- View Students page with searchable, responsive table
- Bootstrap 5 UI with custom styling and micro-interactions
- Duplicate Student ID / email detection (409 Conflict)
- Proper HTTP status codes and JSON error responses
- SQLite database (zero-config, file-based)

## Folder Structure

```
student-management-system/
├── app.py                  # Flask app, routes, REST API, error handlers
├── models.py               # SQLAlchemy Student model + serialization
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── postman_collection.json # Postman collection for API testing
├── students.db             # SQLite database (auto-created on first run)
├── templates/
│   ├── base.html           # Base layout with navbar + footer
│   ├── index.html          # Home / dashboard page
│   ├── form.html           # Add student form
│   └── view.html           # View all students table
└── static/
    ├── style.css           # Custom responsive CSS
    └── script.js           # Form submission + AJAX logic
```

## Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/student-management-system.git
   cd student-management-system
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Running Instructions

```bash
python app.py
```

The server starts on `http://localhost:5000` and binds to `0.0.0.0` so it is accessible from other devices on your network (phones, tablets, other computers).

Open the app in any browser — desktop or mobile. The responsive layout adapts to all screen sizes.

## Pages

| Route     | Page            | Description                          |
|-----------|-----------------|--------------------------------------|
| `/`       | Home / Dashboard | Stat cards + quick actions          |
| `/add`    | Add Student     | Registration form with validation   |
| `/view`   | View Students   | Searchable table of all students     |

## API Documentation

Base URL: `http://localhost:5000`

### 1. Get All Students

```
GET /students
```

**Response 200:**

```json
[
  {
    "id": 1,
    "student_id": "1",
    "name": "John",
    "age": 20,
    "email": "john@gmail.com",
    "marks": [85, 90, 78],
    "average": 84.33,
    "grade": "B"
  }
]
```

### 2. Get Student by ID

```
GET /students/1
```

**Response 200:** Single student object (same shape as above).

**Error 404:**

```json
{ "error": "Student not found" }
```

### 3. Create Student

```
POST /students
Content-Type: application/json
```

**Request body:**

```json
{
  "student_id": "2",
  "name": "Rahul",
  "age": 21,
  "email": "rahul@gmail.com",
  "marks": []
}
```

**Response 201:**

```json
{
  "age": 21,
  "average": null,
  "email": "rahul@gmail.com",
  "grade": "-",
  "id": 2,
  "marks": [],
  "name": "Rahul",
  "student_id": "2"
}
```

**Error 400 (validation):**

```json
{ "errors": { "email": "Invalid email format" } }
```

**Error 409 (conflict):**

```json
{ "error": "Student ID already exists" }
```

### 4. Update Student

```
PUT /students/2
Content-Type: application/json
```

**Request body (partial update):**

```json
{
  "name": "Rahul Sharma",
  "age": 22,
  "marks": [88, 92, 95]
}
```

**Response 200:** Updated student object with recalculated average and grade.

### 5. Delete Student

```
DELETE /students/2
```

**Response 200:**

```json
{ "message": "Student deleted" }
```

### Grade Scale

| Average | Grade |
|---------|-------|
| >= 90   | A+    |
| >= 80   | A     |
| >= 70   | B     |
| >= 60   | C     |
| >= 50   | D     |
| < 50    | F     |

## Postman Collection

Import `postman_collection.json` into Postman to test all five endpoints. Set the `base_url` collection variable to your server address.

## Screenshots

Add your screenshots here:

```
![Dashboard](screenshots/dashboard.png)
![Add Student](screenshots/add-student.png)
![View Students](screenshots/view-students.png)
```

## Tech Stack

- **Backend:** Flask 3.0
- **Database:** SQLite + Flask-SQLAlchemy
- **Frontend:** Bootstrap 5, Jinja2 templates, vanilla JS
- **Language:** Python 3.9+

## License

This project is open source and available under the MIT License.
