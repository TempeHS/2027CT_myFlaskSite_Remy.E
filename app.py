from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

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

@app.route("/sign-up")
def sign_up():
  return render_template("sign_up.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
