from flask import Flask, render_template, request
import pdfplumber
import os

from werkzeug.utils import secure_filename

from resume_matcher import match_resume


app = Flask(__name__)


# ============================================================
# CONFIGURATION
# ============================================================

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf"}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

MIN_JD_LENGTH = 50


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ============================================================
# MAIN ROUTE
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    error = None

    if request.method == "POST":

        # ----------------------------------------------------
        # 1. CHECK RESUME FILE
        # ----------------------------------------------------

        resume_file = request.files.get("resume")

        if not resume_file:

            error = "Please upload your resume PDF."

            return render_template(
                "index.html",
                result=result,
                error=error
            )


        # ----------------------------------------------------
        # 2. CHECK FILE NAME
        # ----------------------------------------------------

        if not resume_file.filename:

            error = "Please select a resume file."

            return render_template(
                "index.html",
                result=result,
                error=error
            )


        # ----------------------------------------------------
        # 3. CHECK FILE TYPE
        # ----------------------------------------------------

        if not allowed_file(
            resume_file.filename
        ):

            error = (
                "Invalid file type. "
                "Please upload a PDF resume."
            )

            return render_template(
                "index.html",
                result=result,
                error=error
            )


        # ----------------------------------------------------
        # 4. GET JOB DESCRIPTION
        # ----------------------------------------------------

        jd_text = request.form.get(
            "jd",
            ""
        ).strip()


        # ----------------------------------------------------
        # 5. CHECK EMPTY JD
        # ----------------------------------------------------

        if not jd_text:

            error = (
                "Please enter a Job Description "
                "before analyzing the resume."
            )

            return render_template(
                "index.html",
                result=result,
                error=error
            )


        # ----------------------------------------------------
        # 6. CHECK JD LENGTH
        # ----------------------------------------------------

        if len(jd_text) < MIN_JD_LENGTH:

            error = (
                "The Job Description is too short. "
                "Please provide a more detailed Job Description."
            )

            return render_template(
                "index.html",
                result=result,
                error=error
            )


        # ----------------------------------------------------
        # 7. SECURE FILE NAME
        # ----------------------------------------------------

        filename = secure_filename(
            resume_file.filename
        )


        if not filename:

            error = (
                "The uploaded filename is invalid. "
                "Please rename the PDF and try again."
            )

            return render_template(
                "index.html",
                result=result,
                error=error
            )


        # ----------------------------------------------------
        # 8. CREATE UNIQUE FILE NAME
        # ----------------------------------------------------

        base_name, extension = os.path.splitext(
            filename
        )

        counter = 1

        final_filename = filename

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            final_filename
        )


        while os.path.exists(filepath):

            final_filename = (
                f"{base_name}_{counter}{extension}"
            )

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                final_filename
            )

            counter += 1


        # ----------------------------------------------------
        # 9. SAVE FILE
        # ----------------------------------------------------

        try:

            resume_file.save(filepath)

        except Exception as e:

            print(
                "File save error:",
                e
            )

            error = (
                "The resume could not be saved. "
                "Please try again."
            )

            return render_template(
                "index.html",
                result=result,
                error=error
            )


        # ----------------------------------------------------
        # 10. EXTRACT TEXT FROM PDF
        # ----------------------------------------------------

        resume_text = ""

        try:

            with pdfplumber.open(filepath) as pdf:

                for page in pdf.pages:

                    text = page.extract_text()

                    if text:

                        resume_text += (
                            text + "\n"
                        )


        except Exception as e:

            print(
                "PDF extraction error:",
                e
            )

            error = (
                "The uploaded PDF could not be read. "
                "Please make sure the file is a valid PDF."
            )

            return render_template(
                "index.html",
                result=result,
                error=error
            )


        # ----------------------------------------------------
        # 11. CHECK EXTRACTED TEXT
        # ----------------------------------------------------

        if not resume_text.strip():

            error = (
                "No readable text was found in the PDF. "
                "Please upload a text-based resume PDF."
            )

            return render_template(
                "index.html",
                result=result,
                error=error
            )


        # ----------------------------------------------------
        # 12. CHECK RESUME TEXT SIZE
        # ----------------------------------------------------

        if len(resume_text.strip()) < 100:

            error = (
                "The resume contains very little readable text. "
                "Please upload a complete resume."
            )

            return render_template(
                "index.html",
                result=result,
                error=error
            )


        # ----------------------------------------------------
        # 13. RUN RESUME MATCHING
        # ----------------------------------------------------

        try:

            result = match_resume(
                resume_text,
                jd_text
            )

        except Exception as e:

            print(
                "Resume matching error:",
                e
            )

            error = (
                "An error occurred while analyzing the resume. "
                "Please try again."
            )

            return render_template(
                "index.html",
                result=result,
                error=error
            )


        # ----------------------------------------------------
        # 14. DELETE UPLOADED FILE
        # ----------------------------------------------------

        try:

            if os.path.exists(filepath):

                os.remove(filepath)

        except Exception as e:

            print(
                "Temporary file cleanup error:",
                e
            )


        # ----------------------------------------------------
        # 15. SHOW RESULTS
        # ----------------------------------------------------

        return render_template(
            "index.html",
            result=result,
            error=None
        )


    # ========================================================
    # GET REQUEST
    # ========================================================

    return render_template(
        "index.html",
        result=result,
        error=error
    )


# ============================================================
# FILE TOO LARGE ERROR
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        result=None,
        error=(
            "The uploaded file is too large. "
            "Please upload a PDF smaller than 5 MB."
        )
    ), 413


# ============================================================
# GENERAL ERROR HANDLER
# ============================================================

@app.errorhandler(500)
def internal_server_error(error):

    print(
        "Internal server error:",
        error
    )

    return render_template(
        "index.html",
        result=None,
        error=(
            "Something went wrong while processing "
            "your request. Please try again."
        )
    ), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )