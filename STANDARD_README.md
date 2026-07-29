# Tempe High Choir Website

A Flask website for the Tempe High School Choir. The site gives students and families one place to check upcoming performances, browse sheet music, view photos, read FAQs, sign up for choir, and view the snack roster.

## Description

This project was built as a school web development task using Python and Flask. It includes public pages for choir members and families, plus a small admin area for updating content. Performance information and snack roster data are saved in JSON files, sign-ups are stored in CSV format, and gallery images are loaded from the `static` folder.

Main features:

- Home page with upcoming performances, a featured event card, and photo carousel
- Music page with embedded sheet music PDFs
- FAQ page with search
- Photo gallery
- Choir sign-up form with validation
- Snack roster page
- Admin dashboard for performances, snack roster entries, and photo uploads
- Accessibility options including OpenDyslexic font, dark mode, and larger text

## Project Structure

Important files and folders:

- `app.py`: main Flask application
- `templates/`: HTML templates
- `static/`: CSS, images, icons, and sheet music PDFs
- `data/`: saved choir sign-ups, performances, and snack roster data
- `test_app.py`: automated tests

## Getting Started

### Dependencies

- Python 3.11 or later
- Flask `3.1.3`
- pytest `9.0.3` or later

Install dependencies with:

```powershell
pip install -r requirements.txt
```

### Running the Website

From the project folder, run:

```powershell
python app.py
```

The site will be available at:

```text
http://127.0.0.1:5000
```

### Running the Tests

Run the automated tests with:

```powershell
pytest -v
```

## Data and Content

The project saves its content in local files:

- `data/sign_ups.csv`: choir sign-up submissions
- `data/upcoming_performances.json`: performance data for the home page
- `data/snack_roster.json`: snack roster entries

Uploaded images are stored in:

```text
static/res/images/
```

## Accessibility Features

The site includes accessibility settings:

- OpenDyslexic font mode
- Dark mode
- Larger text mode
- Skip to content link

These settings can be changed from the footer accessibility menu.

## Help

If the site does not start:

- Make sure Python is installed
- Make sure dependencies were installed with `pip install -r requirements.txt`
- Make sure you are running the command from the project folder

If tests fail, run:

```powershell
python -m pytest -q
```

## Author

Remy Ellis

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- [GitHub Markdown documentation](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [TempeHS Python Flask DevContainer template](https://github.com/TempeHS/TempeHS_Python-Flask_DevContainer)
- [Bootstrap](https://getbootstrap.com/)
- [Flask](https://github.com/pallets/flask?tab=BSD-3-Clause-1-ov-file)
