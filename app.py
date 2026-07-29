import csv
import hmac
import json
import os
import re
from datetime import datetime, UTC
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "tempe-choir-dev-secret")

ACCESSIBILITY_DEFAULTS = {
    "dyslexic_font": False,
    "dark_mode": False,
    "large_text": False,
}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VALID_SCHOOL_YEARS = ["7", "8", "9", "10", "11", "12"]
SIGN_UPS_FILE = Path(app.root_path) / "data" / "sign_ups.csv"
PERFORMANCES_FILE = Path(app.root_path) / "data" / "upcoming_performances.json"
SNACK_ROSTER_FILE = Path(app.root_path) / "data" / "snack_roster.json"
IMAGES_DIR = Path(app.static_folder) / "res" / "images"
LICENSE_FILE = Path(app.root_path) / "LICENSE"
ATTRIBUTION_FILE = Path(app.root_path) / "copyrightInfo.txt"
GITHUB_REPO_URL = "https://github.com/TempeHS/2027CT_myFlaskSite_Remy.E"
NSW_EDU_EMAIL_PATTERN = re.compile(
    r"^[A-Z0-9._%+-]+@education\.nsw\.gov\.au$",
    re.IGNORECASE,
)
ADMIN_SIGN_IN = {
    "full_name": "admin",
    "school_year": "12",
    "email": "admin",
}
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

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

DEFAULT_PERFORMANCES = [
    {
        "title": "Opera House Performance",
        "where": "Meet at C6; Performance at the Opera House",
        "time": "Meet at 4:00 PM",
        "date": "Thursday 10 June 26",
        "notes": "Don't bring a metal water bottle; Dinner goes 3:00-6:30",
    },
    {
        "title": "Ensembles Night",
        "where": "Meet outside Hall",
        "time": "Meet at 8:00 AM",
        "date": "Wednesday 3 June 26",
        "notes": "Performance starts at 6:30 PM",
    },
    {
        "title": "School Spec",
        "where": "Meet at C6; Performance in Homebush",
        "time": "TBD",
        "date": "TBD",
        "notes": "Unconfirmed, may not get in",
    },
]

FAQS = [
    {
        "question": "When and where are choir rehearsals?",
        "answer": "Choir rehearses every week on Wednesdays at 8:00 AM in C6.",
    },
    {
        "question": "What uniform do I need for performances?",
        "answer": "You will usually want performance blacks or school uniform.",
    },
    {
        "question": "Who teaches choir?",
        "answer": "Ms Erin Tillet.",
    },
    {
        "question": "What should I bring to a rehearsal or performance?",
        "answer": "Bring your sheet music, a water bottle, and any other items you need.",
    },
    {
        "question": "What do I do if I am absent from rehearsal?",
        "answer": "Ideally, contact Ms Tillet, but do not worry if you miss one or two.",
    },
    {
        "question": "How do I access the sheet music and practice materials?",
        "answer": "They will be handed to you in rehearsals or available here.",
    },
    {
        "question": "How will I know about upcoming performances and schedule changes?",
        "answer": "Check the home page.",
    },
    {
        "question": "Are parents or carers needed to help at events?",
        "answer": "No.",
    },
    {
        "question": "Who should I contact if I have a question?",
        "answer": "Contact Ms Tillet at: erin.tillet1@det.nsw.edu.au",
    },
]

DEFAULT_SNACK_ROSTER_ITEMS = [
    {
        "date": "24/06/26",
        "event": "Rehearsal",
        "family": "Kenyon",
        "snack": "Muffins",
    },
    {
        "date": "1/07/26",
        "event": "Rehearsal",
        "family": "Ellis",
        "snack": "Banana bread",
    },
    {
        "date": "8/07/26",
        "event": "Rehearsal",
        "family": "Nguyen",
        "snack": "Popcorn bags",
    },
    {
        "date": "15/07/26",
        "event": "Rehearsal",
        "family": "Patel",
        "snack": "Fruit cups",
    },
]

SNACK_ROSTER_NOTES = [
    "Please label food clearly if it contains common allergens.",
    "Bring items to the music room before the performance call time.",
    "Use sealed or individually packed snacks where possible.",
]


def load_gallery_images():
  gallery_images = []

  if not IMAGES_DIR.exists():
    return gallery_images

  for image_path in sorted(IMAGES_DIR.iterdir()):
    if image_path.is_file() and image_path.suffix.lower() in IMAGE_EXTENSIONS:
      title = image_path.stem.replace("_", " ").replace("-", " ").title()
      gallery_images.append(
        {
          "filename": image_path.name,
          "title": title,
        }
      )

  return gallery_images


def build_home_stats():
  return [
      {"label": "Upcoming Performances", "value": len(load_upcoming_performances())},
      {"label": "Sheet Music Files", "value": len(SHEET_MUSIC)},
      {"label": "Gallery Photos", "value": len(load_gallery_images())},
      {"label": "FAQ Entries", "value": len(FAQS)},
  ]


def get_last_updated_date():
  tracked_paths = [
      Path(app.root_path) / "app.py",
      Path(app.root_path) / "templates",
      Path(app.root_path) / "static",
      LICENSE_FILE,
      PERFORMANCES_FILE,
      SNACK_ROSTER_FILE,
  ]
  latest_timestamp = 0.0

  for tracked_path in tracked_paths:
    if not tracked_path.exists():
      continue

    if tracked_path.is_file():
      latest_timestamp = max(latest_timestamp, tracked_path.stat().st_mtime)
      continue

    for file_path in tracked_path.rglob("*"):
      if file_path.is_file():
        latest_timestamp = max(latest_timestamp, file_path.stat().st_mtime)

  if latest_timestamp == 0.0:
    return "Unknown"

  return datetime.fromtimestamp(latest_timestamp).strftime("%d %B %Y")


def load_upcoming_performances():
  if not PERFORMANCES_FILE.exists():
    return [item.copy() for item in DEFAULT_PERFORMANCES]

  try:
    saved_performances = json.loads(PERFORMANCES_FILE.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError):
    return [item.copy() for item in DEFAULT_PERFORMANCES]

  performances = []
  for item in saved_performances:
    performances.append(
        {
            "title": item.get("title", "").strip(),
            "where": item.get("where", "").strip(),
            "time": item.get("time", "").strip(),
            "date": item.get("date", "").strip(),
            "notes": item.get("notes", "").strip(),
        }
    )

  return [item for item in performances if item["title"]] or [item.copy() for item in DEFAULT_PERFORMANCES]


def save_upcoming_performances(performances):
  PERFORMANCES_FILE.parent.mkdir(exist_ok=True)
  PERFORMANCES_FILE.write_text(
      json.dumps(performances, indent=2),
      encoding="utf-8",
  )


def performance_form_rows():
  performances = load_upcoming_performances()
  minimum_rows = 5
  while len(performances) < minimum_rows:
    performances.append(
        {
            "title": "",
            "where": "",
            "time": "",
            "date": "",
            "notes": "",
        }
    )

  return performances


def load_snack_roster_items():
  if not SNACK_ROSTER_FILE.exists():
    return [item.copy() for item in DEFAULT_SNACK_ROSTER_ITEMS]

  try:
    saved_items = json.loads(SNACK_ROSTER_FILE.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError):
    return [item.copy() for item in DEFAULT_SNACK_ROSTER_ITEMS]

  roster_items = []
  for item in saved_items:
    roster_items.append(
        {
            "date": item.get("date", "").strip(),
            "event": item.get("event", "").strip(),
            "family": item.get("family", "").strip(),
            "snack": item.get("snack", "").strip(),
        }
    )

  cleaned_items = [item for item in roster_items if any(item.values())]
  return cleaned_items or [item.copy() for item in DEFAULT_SNACK_ROSTER_ITEMS]


def save_snack_roster_items(roster_items):
  SNACK_ROSTER_FILE.parent.mkdir(exist_ok=True)
  SNACK_ROSTER_FILE.write_text(
      json.dumps(roster_items, indent=2),
      encoding="utf-8",
  )


def snack_roster_form_rows():
  roster_items = load_snack_roster_items()
  minimum_rows = 6

  while len(roster_items) < minimum_rows:
    roster_items.append(
        {
            "date": "",
            "event": "",
            "family": "",
            "snack": "",
        }
    )

  return roster_items


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


def is_admin_sign_in_attempt(form_data):
  return (
      form_data["full_name"].strip().lower() == ADMIN_SIGN_IN["full_name"]
      and form_data["school_year"].strip() == ADMIN_SIGN_IN["school_year"]
      and form_data["email"].strip().lower() == ADMIN_SIGN_IN["email"]
      and ADMIN_PASSWORD is not None
      and hmac.compare_digest(form_data.get("admin_password", ""), ADMIN_PASSWORD)
  )


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


def load_sign_ups():
  if not SIGN_UPS_FILE.exists():
    return []

  with SIGN_UPS_FILE.open("r", newline="", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)
    rows = list(reader)

  return list(reversed(rows))


def format_sign_up_time(sign_up_row):
  timestamp = sign_up_row.get("submitted_at", "")

  try:
    parsed_time = datetime.fromisoformat(timestamp)
  except ValueError:
    return timestamp

  return parsed_time.strftime("%d %b %Y, %I:%M %p")


def filter_sign_ups(sign_ups, search_query):
  cleaned_query = search_query.strip().lower()

  if not cleaned_query:
    return sign_ups

  filtered = []

  for sign_up in sign_ups:
    searchable_text = " ".join(
        [
            sign_up.get("submitted_at", ""),
            sign_up.get("full_name", ""),
            sign_up.get("school_year", ""),
            sign_up.get("email", ""),
        ]
    ).lower()

    if cleaned_query in searchable_text:
      filtered.append(sign_up)

  return filtered


def request_uses_mono_path(path=None):
  target_path = path or request.path
  return target_path == "/mono" or target_path.endswith("/mono")


def get_accessibility_preferences():
  saved_preferences = session.get("accessibility_preferences", {})
  preferences = ACCESSIBILITY_DEFAULTS.copy()

  for key, default_value in ACCESSIBILITY_DEFAULTS.items():
    preferences[key] = bool(saved_preferences.get(key, default_value))

  return preferences


def save_accessibility_preferences(preferences):
  session["accessibility_preferences"] = preferences
  session.modified = True


def normalize_next_url(next_url):
  if not next_url or not next_url.startswith("/"):
    return "/"

  if not get_accessibility_preferences()["dyslexic_font"] and request_uses_mono_path(next_url):
    if next_url == "/mono":
      return "/"
    return next_url[:-5]

  return next_url


def normalize_uploaded_filename(filename):
  safe_name = secure_filename(filename)
  if not safe_name:
    return ""

  candidate = IMAGES_DIR / safe_name
  if not candidate.exists():
    return safe_name

  stem = candidate.stem
  suffix = candidate.suffix
  timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
  return f"{stem}-{timestamp}{suffix}"


def allowed_image_file(filename):
  return Path(filename).suffix.lower() in IMAGE_EXTENSIONS


def save_uploaded_images(files):
  IMAGES_DIR.mkdir(parents=True, exist_ok=True)
  saved_files = []

  for file in files:
    if not file or not file.filename:
      continue

    if not allowed_image_file(file.filename):
      continue

    final_name = normalize_uploaded_filename(file.filename)
    if not final_name:
      continue

    file.save(IMAGES_DIR / final_name)
    saved_files.append(final_name)

  return saved_files


def admin_required(view_func):
  @wraps(view_func)
  def wrapped_view(*args, **kwargs):
    if not session.get("is_admin"):
      flash("Admin sign-in required.", "warning")
      return redirect(mono_path_for("sign_up"))

    return view_func(*args, **kwargs)

  return wrapped_view


def mono_mode_enabled():
  return get_accessibility_preferences()["dyslexic_font"] or request_uses_mono_path()


def standard_path_for(endpoint, **values):
  base_path = url_for(endpoint, **values)

  if base_path == "/mono":
    return "/"

  if base_path.endswith("/mono"):
    return base_path[:-5]

  return base_path


def mono_path_for(endpoint, **values):
  base_path = standard_path_for(endpoint, **values)

  if not mono_mode_enabled():
    return base_path

  if endpoint in {"license_text", "attribution_text", "download_sign_ups"}:
    return base_path

  if base_path == "/":
    return "/mono"

  if base_path.endswith("/mono"):
    return base_path

  return f"{base_path.rstrip('/')}/mono"


@app.before_request
def sync_mono_route_preference():
  if not request_uses_mono_path():
    return

  preferences = get_accessibility_preferences()
  if preferences["dyslexic_font"]:
    return

  preferences["dyslexic_font"] = True
  save_accessibility_preferences(preferences)


@app.context_processor
def inject_display_modes():
  return {
      "mono_mode": mono_mode_enabled(),
      "mono_url": mono_path_for,
      "plain_url": standard_path_for,
      "accessibility_preferences": get_accessibility_preferences(),
      "github_repo_url": GITHUB_REPO_URL,
      "last_updated": get_last_updated_date(),
      "current_year": datetime.now().year,
  }


@app.route("/accessibility", methods=["POST"])
@app.route("/accessibility/mono", methods=["POST"])
def update_accessibility():
  next_url = normalize_next_url(request.form.get("next_url", request.path))

  if request.form.get("reset") == "1":
    save_accessibility_preferences(ACCESSIBILITY_DEFAULTS.copy())
    return redirect(normalize_next_url(next_url))

  preferences = {
      "dyslexic_font": request.form.get("dyslexic_font") == "on",
      "dark_mode": request.form.get("dark_mode") == "on",
      "large_text": request.form.get("large_text") == "on",
  }
  save_accessibility_preferences(preferences)
  return redirect(normalize_next_url(next_url))

@app.route("/")
@app.route("/mono")
@app.route("/home")
@app.route("/home/mono")
def home():
  performances = load_upcoming_performances()
  return render_template(
      "home.html",
      performances=performances,
      featured_performance=performances[0] if performances else None,
      site_stats=build_home_stats(),
      last_updated=get_last_updated_date(),
      github_repo_url=GITHUB_REPO_URL,
  )


@app.route("/license")
def license_text():
  return send_file(
      LICENSE_FILE,
      as_attachment=False,
      download_name="LICENSE.txt",
      mimetype="text/plain",
  )


@app.route("/attribution")
def attribution_text():
  return send_file(
      ATTRIBUTION_FILE,
      as_attachment=False,
      download_name="attribution.txt",
      mimetype="text/plain",
  )

@app.route("/music")
@app.route("/music/mono")
def music():
  return render_template("music.html", sheet_music=SHEET_MUSIC, music_total=len(SHEET_MUSIC))

@app.route("/snack-roster")
@app.route("/snack-roster/mono")
def snack_roster():
  return render_template(
      "snack_roster.html",
      snack_roster_items=load_snack_roster_items(),
      snack_roster_notes=SNACK_ROSTER_NOTES,
  )

@app.route("/faqs")
@app.route("/faqs/mono")
def faqs():
  return render_template("faqs.html", faq_items=FAQS)

@app.route("/photos")
@app.route("/photos/mono")
def photos():
  gallery_images = load_gallery_images()
  return render_template("photos.html", gallery_images=gallery_images, gallery_total=len(gallery_images))

@app.route("/sign-up", methods=["GET", "POST"])
@app.route("/sign-up/mono", methods=["GET", "POST"])
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
        "admin_password": request.form.get("admin_password", ""),
    }

    if is_admin_sign_in_attempt(submitted_data):
      session["is_admin"] = True
      flash("Admin access granted.", "success")
      return redirect(mono_path_for("admin_dashboard"))

    form_data, errors = validate_sign_up(submitted_data)

    if not errors:
      try:
        save_sign_up(form_data)
      except OSError:
        form_message = "Your sign-up could not be saved right now. Please try again."
      else:
        return redirect(mono_path_for("sign_up", success="1"))

  return render_template(
      "sign_up.html",
      form_data=form_data,
      errors=errors,
      form_message=form_message,
      success=success,
      school_years=VALID_SCHOOL_YEARS,
  )


@app.route("/admin", methods=["GET", "POST"])
@app.route("/admin/mono", methods=["GET", "POST"])
@admin_required
def admin_dashboard():
  performance_rows = performance_form_rows()
  snack_roster_rows = snack_roster_form_rows()
  search_query = request.args.get("search", "")
  sign_ups = load_sign_ups()

  for sign_up in sign_ups:
    sign_up["submitted_display"] = format_sign_up_time(sign_up)

  filtered_sign_ups = filter_sign_ups(sign_ups, search_query)

  if request.method == "POST":
    action = request.form.get("action", "")

    if action == "performances":
      titles = request.form.getlist("performance_title")
      wheres = request.form.getlist("performance_where")
      times = request.form.getlist("performance_time")
      dates = request.form.getlist("performance_date")
      notes = request.form.getlist("performance_notes")
      updated_performances = []

      for title, where, time, date, notes_value in zip(titles, wheres, times, dates, notes):
        cleaned_row = {
            "title": title.strip(),
            "where": where.strip(),
            "time": time.strip(),
            "date": date.strip(),
            "notes": notes_value.strip(),
        }
        if cleaned_row["title"]:
          updated_performances.append(cleaned_row)

      if updated_performances:
        save_upcoming_performances(updated_performances)
        flash("Upcoming performances updated.", "success")
      else:
        flash("Please keep at least one performance with a title.", "warning")

      return redirect(mono_path_for("admin_dashboard"))

    if action == "photos":
      uploaded_files = request.files.getlist("photo_uploads")
      saved_files = save_uploaded_images(uploaded_files)

      if saved_files:
        flash(f"Uploaded {len(saved_files)} photo(s).", "success")
      else:
        flash("No valid image files were uploaded.", "warning")

      return redirect(mono_path_for("admin_dashboard"))

    if action == "snack_roster":
      dates = request.form.getlist("roster_date")
      events = request.form.getlist("roster_event")
      families = request.form.getlist("roster_family")
      snacks = request.form.getlist("roster_snack")
      updated_roster_items = []

      for date, event, family, snack in zip(dates, events, families, snacks):
        cleaned_row = {
            "date": date.strip(),
            "event": event.strip(),
            "family": family.strip(),
            "snack": snack.strip(),
        }
        if any(cleaned_row.values()):
          updated_roster_items.append(cleaned_row)

      if updated_roster_items:
        save_snack_roster_items(updated_roster_items)
        flash("Snack roster updated.", "success")
      else:
        flash("Please keep at least one snack roster row.", "warning")

      return redirect(mono_path_for("admin_dashboard"))

  return render_template(
      "admin.html",
      performance_rows=performance_rows,
      snack_roster_rows=snack_roster_rows,
      sign_ups=filtered_sign_ups,
      search_query=search_query,
  )


@app.route("/admin/sign-ups/download")
@admin_required
def download_sign_ups():
  if not SIGN_UPS_FILE.exists():
    flash("There are no sign-ups to download yet.", "warning")
    return redirect(mono_path_for("admin_dashboard"))

  return send_file(
      SIGN_UPS_FILE,
      as_attachment=True,
      download_name="sign_ups.csv",
      mimetype="text/csv",
  )


@app.route("/admin/logout", methods=["POST"])
@app.route("/admin/logout/mono", methods=["POST"])
@admin_required
def admin_logout():
  session.clear()
  flash("Admin signed out.", "success")
  return redirect(mono_path_for("sign_up"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
