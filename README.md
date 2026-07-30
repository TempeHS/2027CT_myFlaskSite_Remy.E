# Tempe High School Choir Website

| Field               | Detail                                                              |
| ------------------- | ------------------------------------------------------------------- |
| **Website Title**   | Tempe High School Choir                                             |
| **Student Name(s)** | Remy Ellis                                                          |
| **Class / Course**  | 2027CT                                                              |
| **Repository**      | [GitHub Repo](https://github.com/TempeHS/2027CT_myFlaskSite_Remy.E) |
| **Date**            | 30/07/26                                                            |

---

## 1. Overview

**Purpose:** This is a Flask website built to help members of the Tempe High School Choir better interact with parts of the choir like accessing sheet music or viewing the snack roster. It also provides information for people looking to join the choir and provides an easy way for them to sign up.

**Target audience:** Current members of the Tempe High School Choir and people looking to join the choir.

**Technology stack:** Flask · Jinja2 · HTML · CSS · Bootstrap

---

## 2. Walkthrough Video

| Field            | Detail                                     |
| ---------------- | ------------------------------------------ |
| **Link / Embed** | [Demo Video](https://youtu.be/n_m2ZYHP0cA) |
| **Duration**     | 3:23                                       |

---

## 3. Evaluation

### 3.1 Statement of Intent

#### What is the Website?

The website will be an information and sign-up website for students looking to join or currently in the Tempe High Choir. It will have a homepage with our songs and their audio tracks and sheet music. It will also have the weekly roster for those bringing snacks and general information about time and location and upcoming events for those looking to join as well as a way to sign up for choir.

#### Why is it Needed?

This website is necessary as many students don't know when or where choir is and how to join. It's also currently difficult to find the sheet music and there's no organisation on who’s bringing snacks and tea. And it will let students keep track of upcoming events. This website will help by letting students sign up through a form, letting teachers know who's a part of it. A lot of students also would join choir but don't know when and where it's on so this will help spread the word. Having easy access to audio tracks and sheet music will make it easier to rehearse at home.

#### Who is it For?

The website is primarily for members of the choir. And secondarily for people looking to join and the teacher(s) running it. This website will make it much easier for choir members to rehearse at home, keep track of upcoming events and who needs to bring food that week. It will also make it much easier to join choir and for teachers to know who's a part of it.

### 3.2 What I Delivered

| Page / Feature | Route                 | What it delivers                                                                                                                |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Homepage       | `/home`               | Clean and informative homepage with a main Hero Image, carousel and information on upcoming performances.                       |
| Music          | `/music`              | Sheet music for members as downloadable PDFs that can also be viewed in the browser, as well as file searching.                 |
| Snack Roster   | `/snack-roster`       | Shows the weekly roster for who is bringing snacks, with the roster able to be updated through the admin page.                  |
| FAQs           | `/faqs`               | FAQs in an accordion menu with keyword searching through both the Question and Answer.                                          |
| Photos         | `/photos`             | Photos in a responsive Bootstrap table with hover animations.                                                                   |
| Sign Up        | `/sign-up`            | Lets users enter their name, email and year, which gets sent to the backend.                                                    |
| Admin          | `/admin`              | Lets the Teacher edit the Snack Roster and Upcoming Performances, view sign-ups, download them to a CSV file and upload photos. |
| Footer         | Across all main pages | Contains my name and copyright, a dynamic 'Last Updated:', and links to the `LICENSE`, GitHub and Copyright Info.               |
| Accessibility  | Across all main pages | `Skip to Main Content`, OpenDyslexic Font, Larger Text and Dark Mode, with accessibility features persisting across pages.      |

### 3.3 Evaluation Against My Intent

#### Homepage

My website contains a clean and informative homepage with a main Hero Image and a carousel to entice possible members as well as information on upcoming performances to help both potential new members as well as current ones. Clicking on the logo also takes you to `/home`.

This meets the goal in my Statement of Intent of providing general information and upcoming events for both current and potential members.

#### Music

The Music page contains sheet music for members to reference as downloadable PDFs that can also be viewed in the browser. You are also able to search the files. It is lacking audio tracks as I was not able to obtain any from my teacher due to copyright.

This means the original goal was only partially achieved, as the sheet music was provided but the planned audio tracks were not.

#### FAQs

There are FAQs in an accordion menu with useful information for mainly new members. You can also search keywords and it will look both in the Question and Answer.

This helps meet the goal of making information about joining choir easier to find.

#### Photos

There are photos in a responsive Bootstrap table with hover animations. I was not able to obtain any more photos from my Choir Teacher.

#### Sign Up

There is a Sign Up page that lets you enter your name, email and year which gets sent to the backend. This lets the Teacher track who signed up and who is currently participating in Choir.

This directly meets the Statement of Intent goal of making it easier for students to join and for teachers to know who is participating.

#### Snack Roster

The website includes a weekly snack roster, which directly addresses the problem identified in my Statement of Intent that there was previously no organisation around who was bringing snacks and tea.

#### Time and Location Information

The website also provides information about when and where choir takes place, helping address the problem that some students do not know when or where choir is held.

#### Admin Page

The admin page is protected by login details and an `ADMIN_PASSWORD` stored in the `.env` file. This lets you edit the Snack Roster and Upcoming Performances as well as look at sign-ups and download them to a CSV file. You are also able to upload photos to be displayed. All edits made by admin are stored in `.json` files. You can log out of admin in the top right of the navbar.

#### Footer

The footer contains my name and copyright ((c) Remy Ellis 2026), a dynamic 'Last Updated:', a link to the `LICENSE`, Github and Copyright Info.

#### Accessibility

There are four accessibility features. Links to `Skip to Main Content` and three settings in the footer: OpenDyslexic Font, Larger Text and Dark Mode. This makes the website more accessible to certain users. Accessibility features persist across pages.

### 3.4 Overall Effectiveness

Overall, I believe my website has been highly effective in it's goal in improving availability of information to both members of Choir and those looking to join.

The website provides centralised access to sheet music, upcoming performances, the snack roster, choir information and sign-ups, directly addressing most of the problems identified in my Statement of Intent.

It falls short in a lack of photos and audio tracks I was able to obtain as well as slightly slow loading of pages containing multiple images.

The main part of my original intent that was not achieved was providing audio tracks. If I improved the website further, I would add audio tracks if copyright permission became available and optimise the images to improve loading times.

But overall, my website achieved it's goals.

---

## 4. Acknowledgements

| What you used | Source / Creator  | Licence                   | What you used it for        |
| ------------- | ----------------- | ------------------------- | --------------------------- |
| Bootstrap     | Bootstrap team    | MIT                       | Layout and components       |
| Flask         | Pallets Projects  | BSD                       | Web server and routing      |
| Jinja2        | Pallets Projects  | BSD                       | HTML templates              |
| OpenDyslexic  | Abelardo Gonzalez | SIL Open Font License 1.1 | Optional accessibility font |
| Choir Images  | Erin Tillet       | Copyright                 | Photos on home page         |

---

> **Student Declaration:** All work submitted is my own except where explicitly acknowledged above.
