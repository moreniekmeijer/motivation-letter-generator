from flask import Flask, render_template, request, send_from_directory
from gemini_client import generate_motivation_letter
import os
import uuid
import helpers

app = Flask(__name__)
OUTPUT_DIR = "letter_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_info = request.form.get("user_info", "")
        job_description = request.form.get("job_description", "")

        sanitized_user_info = helpers.sanitize_input(user_info)
        sanitized_job_description = helpers.sanitize_input(job_description)

        letter = generate_motivation_letter(
            sanitized_user_info, sanitized_job_description)

        unique_filename = f"letter_{uuid.uuid4().hex}.txt"
        filepath = os.path.join(OUTPUT_DIR, unique_filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(letter)

        return render_template("result.html", letter=letter, filename=unique_filename)

    return render_template("index.html")


@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
