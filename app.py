import csv
import re
from datetime import datetime, UTC
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VALID_SCHOOL_YEARS = ["7", "8", "9", "10", "11", "12"]
SIGN_UPS_FILE = Path(app.root_path) / "data" / "sign_ups.csv"
NSW_EDU_EMAIL_PATTERN = re.compile(
    r"^[A-Z0-9._%+-]+@education\.nsw\.gov\.au$",
    re.IGNORECASE,
)

SHEET_MUSIC = [
    {
        "title": "Wicked Medley",
        "filename": "WickedMedleySheetMusic.pdf",
        "description": "Vocal score for Wicked Medley.",
    },
    {
        "title": "Songs From Grimm",
        "filename": "SongsFromGrimmSheetMusic.pdf",
        "description": "Sheet music for Songs From Grimm.",
    },
    {
        "title": "Requiem",
        "filename": "RequiemSheetMusic.pdf",
        "description": "Choir score for Requiem.",
    },
    {
        "title": "Over The Rainbow",
        "filename": "OverTheRainbowSheetMusic.pdf",
        "description": "Sheet music for Over The Rainbow.",
    },
    {
        "title": "Indodana",
        "filename": "IndodanaSheetMusic.pdf",
        "description": "Choir score for Indodana.",
    },
]


def load_gallery_images():
  image_dir = Path(app.static_folder) / "res" / "images"
  gallery_images = []

  if not image_dir.exists():
    return gallery_images

  for image_path in sorted(image_dir.iterdir()):
    if image_path.is_file() and image_path.suffix.lower() in IMAGE_EXTENSIONS:
      title = image_path.stem.replace("_", " ").replace("-", " ").title()
      gallery_images.append(
        {
          "filename": image_path.name,
          "title": title,
        }
      )

  return gallery_images


def blank_sign_up_form():
  return {
      "full_name": "",
      "school_year": "",
      "email": "",
  }


def validate_sign_up(form_data):
  cleaned = {
      "full_name": " ".join(form_data["full_name"].split()),
      "school_year": form_data["school_year"].strip(),
      "email": form_data["email"].strip().lower(),
  }
  errors = {}

  if not cleaned["full_name"]:
    errors["full_name"] = "Please enter your full name."

  if cleaned["school_year"] not in VALID_SCHOOL_YEARS:
    errors["school_year"] = "Please choose your school year."

  if not cleaned["email"]:
    errors["email"] = "Please enter your school email."
  elif not NSW_EDU_EMAIL_PATTERN.fullmatch(cleaned["email"]):
    errors["email"] = "Email must end in @education.nsw.gov.au."

  return cleaned, errors


def save_sign_up(sign_up_data):
  SIGN_UPS_FILE.parent.mkdir(exist_ok=True)
  file_exists = SIGN_UPS_FILE.exists() and SIGN_UPS_FILE.stat().st_size > 0

  with SIGN_UPS_FILE.open("a", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(
        csv_file,
        fieldnames=["submitted_at", "full_name", "school_year", "email"],
    )

    if not file_exists:
      writer.writeheader()

    writer.writerow(
        {
            "submitted_at": datetime.now(UTC).isoformat(),
            "full_name": sign_up_data["full_name"],
            "school_year": sign_up_data["school_year"],
            "email": sign_up_data["email"],
        }
    )

@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html")

@app.route("/music")
def music():
  return render_template("music.html", sheet_music=SHEET_MUSIC)

@app.route("/snack-roster")
def snack_roster():
  return render_template("snack_roster.html")

@app.route("/faqs")
def faqs():
  return render_template("faqs.html")

@app.route("/photos")
def photos():
  return render_template("photos.html", gallery_images=load_gallery_images())

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
  form_data = blank_sign_up_form()
  errors = {}
  form_message = ""
  success = request.args.get("success") == "1"

  if request.method == "POST":
    submitted_data = {
        "full_name": request.form.get("full_name", ""),
        "school_year": request.form.get("school_year", ""),
        "email": request.form.get("email", ""),
    }
    form_data, errors = validate_sign_up(submitted_data)

    if not errors:
      try:
        save_sign_up(form_data)
      except OSError:
        form_message = "Your sign-up could not be saved right now. Please try again."
      else:
        return redirect(url_for("sign_up", success="1"))

  return render_template(
      "sign_up.html",
      form_data=form_data,
      errors=errors,
      form_message=form_message,
      success=success,
      school_years=VALID_SCHOOL_YEARS,
  )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
