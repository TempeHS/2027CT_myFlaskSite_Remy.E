from flask import Flask, render_template

app = Flask(__name__)

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
  return render_template("photos.html")

@app.route("/sign-up")
def sign_up():
  return render_template("sign_up.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
