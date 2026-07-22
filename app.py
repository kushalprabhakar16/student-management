import io
import os
import zipfile
from flask import Flask, render_template, request, jsonify, send_file
from models import db, Student

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'students.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ---------- Page routes ----------
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/add")
    def add_page():
        return render_template("form.html")

    @app.route("/view")
    def view_page():
        return render_template("view.html")

    @app.route("/download")
    def download_project():
        """Bundle all source files into a downloadable ZIP archive."""
        skip_dirs = {"__pycache__", ".bolt", ".v3", "instance"}
        skip_files = {"students.db", ".env"}
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(BASE_DIR):
                dirs[:] = [d for d in dirs if d not in skip_dirs]
                for fname in files:
                    if fname in skip_files or fname.endswith(".db"):
                        continue
                    full = os.path.join(root, fname)
                    arcname = os.path.relpath(full, BASE_DIR)
                    zf.write(full, arcname)
        buf.seek(0)
        return send_file(
            buf,
            mimetype="application/zip",
            as_attachment=True,
            download_name="student-management-system.zip",
        )

    # ---------- REST API ----------
    @app.route("/students", methods=["GET"])
    def get_students():
        students = Student.query.order_by(Student.id.desc()).all()
        return jsonify([s.to_dict() for s in students]), 200

    @app.route("/students/<int:sid>", methods=["GET"])
    def get_student(sid):
        student = Student.query.get(sid)
        if not student:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(student.to_dict()), 200

    @app.route("/students", methods=["POST"])
    def create_student():
        data = request.get_json(silent=True) or {}
        errors = validate_student(data)
        if errors:
            return jsonify({"errors": errors}), 400

        if Student.query.filter_by(student_id=data["student_id"]).first():
            return jsonify({"error": "Student ID already exists"}), 409
        if Student.query.filter_by(email=data["email"].lower()).first():
            return jsonify({"error": "Email already exists"}), 409

        student = Student(
            student_id=data["student_id"],
            name=data["name"].strip(),
            age=data["age"],
            email=data["email"].lower().strip(),
            marks=data.get("marks", []),
        )
        student.calculate_average()
        db.session.add(student)
        db.session.commit()
        return jsonify(student.to_dict()), 201

    @app.route("/students/<int:sid>", methods=["PUT"])
    def update_student(sid):
        student = Student.query.get(sid)
        if not student:
            return jsonify({"error": "Student not found"}), 404

        data = request.get_json(silent=True) or {}
        errors = validate_student(data, partial=True)
        if errors:
            return jsonify({"errors": errors}), 400

        if "student_id" in data and data["student_id"] != student.student_id:
            if Student.query.filter_by(student_id=data["student_id"]).first():
                return jsonify({"error": "Student ID already exists"}), 409
            student.student_id = data["student_id"]
        if "email" in data and data["email"].lower() != student.email:
            if Student.query.filter_by(email=data["email"].lower()).first():
                return jsonify({"error": "Email already exists"}), 409
            student.email = data["email"].lower().strip()
        if "name" in data:
            student.name = data["name"].strip()
        if "age" in data:
            student.age = data["age"]
        if "marks" in data:
            student.marks = data["marks"]
        student.calculate_average()
        db.session.commit()
        return jsonify(student.to_dict()), 200

    @app.route("/students/<int:sid>", methods=["DELETE"])
    def delete_student(sid):
        student = Student.query.get(sid)
        if not student:
            return jsonify({"error": "Student not found"}), 404
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted"}), 200

    # ---------- Error handlers ----------
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app


def validate_student(data, partial=False):
    errors = {}
    required = ["student_id", "name", "age", "email"]
    for field in required:
        if field not in data or data[field] in (None, ""):
            if not partial:
                errors[field] = f"{field} is required"
    if errors and not partial:
        return errors

    if "name" in data and data.get("name"):
        if len(data["name"].strip()) < 2:
            errors["name"] = "Name must be at least 2 characters"
    if "age" in data and data.get("age") is not None:
        try:
            age = int(data["age"])
            if age < 5 or age > 120:
                errors["age"] = "Age must be between 5 and 120"
        except (ValueError, TypeError):
            errors["age"] = "Age must be a number"
    if "email" in data and data.get("email"):
        email = data["email"].strip()
        if "@" not in email or "." not in email.split("@")[-1]:
            errors["email"] = "Invalid email format"
    if "marks" in data and data.get("marks") is not None:
        if not isinstance(data["marks"], list):
            errors["marks"] = "Marks must be a list of numbers"
        elif not all(isinstance(m, (int, float)) and 0 <= m <= 100 for m in data["marks"]):
            errors["marks"] = "Marks must be numbers between 0 and 100"
    return errors


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
