document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("studentForm");
    if (!form) return;

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        if (!form.checkValidity()) {
            form.classList.add("was-validated");
            return;
        }

        const marksRaw = document.getElementById("marks").value.trim();
        const marks = marksRaw
            ? marksRaw.split(",").map(m => parseFloat(m.trim())).filter(m => !isNaN(m))
            : [];

        const payload = {
            student_id: document.getElementById("student_id").value.trim(),
            name: document.getElementById("name").value.trim(),
            age: parseInt(document.getElementById("age").value),
            email: document.getElementById("email").value.trim(),
            marks: marks,
        };

        const alertBox = document.getElementById("formAlert");

        try {
            const res = await fetch("/students", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
            const data = await res.json();

            if (res.ok) {
                alertBox.innerHTML =
                    `<div class="alert alert-success">Student added successfully! Grade: ${data.grade}</div>`;
                form.reset();
                form.classList.remove("was-validated");
                setTimeout(() => { window.location.href = "/view"; }, 1200);
            } else {
                const msg = data.errors
                    ? Object.values(data.errors).join(", ")
                    : data.error || "Failed to add student.";
                alertBox.innerHTML = `<div class="alert alert-danger">${msg}</div>`;
            }
        } catch (err) {
            alertBox.innerHTML =
                `<div class="alert alert-danger">Network error. Please try again.</div>`;
        }
    });
});
