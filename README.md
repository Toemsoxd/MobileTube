# MobileTube

A standalone video platform designed for older mobile browsers and media players.

## Project goals

- Keep the client-side website extremely lightweight.
- Support Windows Mobile / Windows CE-era devices.
- Provide downloadable/streamable legacy video formats such as 3GP.
- Make uploads and transcoding happen on the server, not on the mobile device.
- Preserve a simple 2009–2010-era mobile web experience.

## Repository layout

```text
MobileTube/
├── index.html     # Main website entry point
├── vids/          # Stored video files
├── web/           # Additional web pages
├── server/        # Backend and upload/transcoding logic
└── README.md
```

## Upload policy

Video uploads are intended for **PC users only**. The mobile site is for browsing, searching, and watching videos; the upload endpoint rejects recognized mobile user agents.

## Video storage

Uploaded/processed videos are stored under `vids/`. The directory is intentionally kept separate from the web application code so video files can later be moved to dedicated storage without changing the frontend.

## Running the development server

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Then start MobileTube:

```bash
python server/app.py
```

The development server listens on port `8000`.

## First milestone

1. Create the basic site/backend structure.
2. Add PC-only video upload.
3. Store uploaded videos in `vids/`.
4. Add a first legacy-compatible transcoding profile.
5. Test playback on Opera Mobile 10 / Windows Mobile.
