from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

app = Flask(__name__)

# Folder paths
UPLOAD_FOLDER = "static/uploads"
SCREENSHOT_FOLDER = "screenshots"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create folders if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# -----------------------------
# Demo Auto Person Information Database
# -----------------------------
PERSON_DATABASE = {
    "rahul123": {
        "name": "Rahul Sharma",
        "contact": "Not Public",
        "followers": "2450",
        "following": "380",
        "bio": "Crypto investor | Trading | Business",
        "risk_level": "Medium",
        "history": "Suspicious keywords found in public bio and repeated crypto scam patterns.",
        "keywords": "crypto, money, scam"
    },
    "scammer01": {
        "name": "Unknown Fraud Account",
        "contact": "Hidden",
        "followers": "980",
        "following": "1200",
        "bio": "Fast money | Investment returns | DM now",
        "risk_level": "High",
        "history": "Possible phishing/fraud indicators detected from profile pattern.",
        "keywords": "otp, investment, fast money, fraud"
    },
    "testuser": {
        "name": "Test User",
        "contact": "Not Available",
        "followers": "1200",
        "following": "450",
        "bio": "Public profile used for demo testing.",
        "risk_level": "Low",
        "history": "No major suspicious history found in demo data.",
        "keywords": "none"
    }
}

# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------
# Process Form
# -----------------------------
@app.route("/process", methods=["POST"])
def process():
    case_id = request.form.get("case_id", "")
    officer_name = request.form.get("officer_name", "")
    suspect_name = request.form.get("suspect_name", "")
    platform = request.form.get("platform", "")
    profile_url = request.form.get("profile_url", "")
    username = request.form.get("username", "").strip().lower()

    # Auto fetch person info from database
    person_info = PERSON_DATABASE.get(username, {
        "name": suspect_name if suspect_name else "Unknown Person",
        "contact": "Not Publicly Available",
        "followers": "Not Found",
        "following": "Not Found",
        "bio": "No public profile information found.",
        "risk_level": "Unknown",
        "history": "No suspicious history found in available demo data.",
        "keywords": "No keywords detected"
    })

    # Upload profile image (optional)
    profile_image = request.files.get("profile_image")
    image_filename = None

    if profile_image and profile_image.filename != "":
        image_filename = secure_filename(profile_image.filename)
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_filename)
        profile_image.save(image_path)

    # Create dummy screenshot file names
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot1 = f"{case_id}_profile_{timestamp}.png"
    screenshot2 = f"{case_id}_timeline_{timestamp}.png"
    screenshot3 = f"{case_id}_messages_{timestamp}.png"

    # Create empty files for demo
    open(os.path.join(SCREENSHOT_FOLDER, screenshot1), "a").close()
    open(os.path.join(SCREENSHOT_FOLDER, screenshot2), "a").close()
    open(os.path.join(SCREENSHOT_FOLDER, screenshot3), "a").close()

    screenshots = [screenshot1, screenshot2, screenshot3]

    # Create PDF report
    pdf_filename = f"{case_id}_report.pdf"
    pdf_path = os.path.join(REPORT_FOLDER, pdf_filename)

    generate_pdf_report(
        pdf_path,
        case_id,
        officer_name,
        suspect_name,
        platform,
        profile_url,
        username,
        person_info
    )

    return render_template(
        "result.html",
        case_id=case_id,
        officer_name=officer_name,
        suspect_name=suspect_name,
        platform=platform,
        profile_url=profile_url,
        username=username,
        image_filename=image_filename,
        screenshots=screenshots,
        pdf_filename=pdf_filename,
        person_info=person_info
    )

# -----------------------------
# PDF Generator
# -----------------------------
def generate_pdf_report(pdf_path, case_id, officer_name, suspect_name, platform, profile_url, username, person_info):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Social Media Evidence Report")
    y -= 30

    c.setFont("Helvetica", 11)
    lines = [
        f"Case ID: {case_id}",
        f"Officer Name: {officer_name}",
        f"Suspect Name: {suspect_name}",
        f"Platform: {platform}",
        f"Profile URL: {profile_url}",
        f"Username / ID: {username}",
        f"Detected Name: {person_info['name']}",
        f"Contact: {person_info['contact']}",
        f"Followers / Friends: {person_info['followers']}",
        f"Following: {person_info['following']}",
        f"Bio / Public Info: {person_info['bio']}",
        f"Risk Level: {person_info['risk_level']}",
        f"Suspicious History: {person_info['history']}",
        f"Keywords: {person_info['keywords']}",
    ]

    for line in lines:
        c.drawString(50, y, line)
        y -= 20
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)

    c.save()

# -----------------------------
# Download PDF
# -----------------------------
@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(REPORT_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)