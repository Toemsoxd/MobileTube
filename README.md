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
├── vids/          # Stored video files
├── web/           # Website/frontend
├── server/        # Backend and upload/transcoding logic
└── README.md
```

## Upload policy

Video uploads are intended for **PC users only**. The mobile site is for browsing, searching, and watching videos; it does not expose the upload interface to mobile clients.

## Video storage

Uploaded/processed videos will be stored under `vids/`. The directory is intentionally kept separate from the web application code so video files can later be moved to dedicated storage without changing the frontend.

## First milestone

1. Create the basic site/backend structure.
2. Add PC-only video upload.
3. Store uploaded videos in `vids/`.
4. Add a first legacy-compatible transcoding profile.
5. Test playback on Opera Mobile 10 / Windows Mobile.
