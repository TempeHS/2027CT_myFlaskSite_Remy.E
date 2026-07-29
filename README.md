# Evaluation

## Section 1: Overview

This is a Flask website built to help members of the Tempe High School Choir better interact with parts of the choir like accessing sheet music or viewing the snack roster. It also provides information for people looking to join the choir and provide an easy way for them to sign up.

It's built with a combination of Flask, Jina2, HTML, CSS and Bootstrap.

## Section 2: Evaluation Against Statement of Intent

### 2.1 Homepage

My website contains a clean and informative homepage with a main Hero Image and a carousel to entice possible members as well as information on upcoming performances to help both potential new members as well as current ones. Clicking on the logo also takes you to `/home`

### 2.2 Music

The Music page contains sheet music for members to reference as downloadable PDFs that can also be run in the browser. You are also able to search the files. It is lacking audio tracks as I was not able to obtain any from my teacher due to copyright.

### 2.3 FAQs

There are FAQs in an accordion menu with useful information for mainly new members. You can also search keywords and it will look both in the Question and Answer.

### 2.4 Photos

There are photos in a responsive Bootstrap table with hover animations. I was not able to obtain any more photos from my Choir Teacher.

### 2.5 Sign Up

There is a Sign Up page that lets you enter your name, email and year which gets sent to the backend. This lets the Teacher track who signed up and who is currently participating in Choir.

### 2.6 Admin Page

By entering admin and year 12 in all applicable fields and then the `ADMIN_PASSWORD` stored in the `.env` file, you are able to access the admin page. This lets you edit the Snack Roster and Upcoming Performances as well as look at sign-ups and download them to a csv file. You are also able to upload photos to be displayed. All edits made by admin are stored in `.json` files. You can log out of admin in the top right of the navbar.

### 2.7 Footer

The footer contains my name and copyright ((c) Remy Ellis 2026), a dynamic 'Last Updated:', a link to the `LICENSE`, Github and Copyright Info.

### 2.8 Accessibility

There are four accessibility features. Links to `Skip to Main Content` and three settings in the footer: OpenDyslexic Font, Larger Text and Dark Mode. This makes the website more accessible to certain users. Accessibility features persist across pages.

## Overall Effectiveness

Overall, I believe my website has been highly effective in it's goal in improving availability of infomation to both members of Choir and those looking to join.

It falls short in a lack of photos and audio tracks I was able to obtain as well as slightly slow loading of pages containing multiple images.

But overall, my website achieved it's goals
