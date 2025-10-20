from flask import Flask, render_template, request
from gemini_client import generate_motivation_letter
import helpers
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")


@app.route("/", methods=["GET", "POST"])
def index():
    letter = None
    title = None
    if request.method == "POST":
        title = request.form.get("title", "Untitled").strip()
        user_info = request.form.get("user_info", "").strip()
        job_description = request.form.get("job_description", "").strip()

        try:
            sanitized_user_info = helpers.sanitize_input(user_info)
            sanitized_job_description = helpers.sanitize_input(job_description)
        except Exception:
            sanitized_user_info = user_info
            sanitized_job_description = job_description

        language = request.form.get("language", "English")
        tone = request.form.get("tone", "Formal")

        letter = generate_motivation_letter(
            sanitized_user_info, sanitized_job_description, language, tone
        )

    return render_template("index.html", letter=letter, title=title)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
