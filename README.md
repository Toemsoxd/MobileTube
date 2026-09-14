# MobileTube

A standalone video platform designed for older mobile browsers and media players.

**YouTube on the go!**

## Project goals

- Recreate the feel of a lightweight 2009-era video site.
- Support Windows Mobile / Windows CE-era devices.
- Use legacy-friendly video formats such as 3GP.
- Keep the mobile-facing website extremely lightweight.
- Keep uploads restricted to PC users.
- Prepare the site for static legacy hosting such as KESUG/Web 1.0 Hosting.
- Use RTSP/Streaming Media for devices that support native mobile streaming.

## Repository layout

```text
MobileTube/
├── index.html             # Static homepage for simple hosting
├── style.css              # Lightweight 2009-inspired styling
├── MobileTubeLog.png      # MobileTube logo
├── vids/                  # Legacy-compatible video files
├── web/                   # Additional web pages
├── server/                # Flask development/backend server
├── tools/
│   └── generate_static.py # Rebuilds index.html from vids/
└── README.md
```

## Static hosting

MobileTube is designed so the frontend and `vids/` directory can be copied directly to a static host. No JavaScript is required for the basic catalog.

When videos are added or removed, regenerate the static homepage with:

```bash
python tools/generate_static.py
```

Then copy the site files to the legacy host.

## Video playback

The primary legacy video target is 3GP. The current test profile is:

- Container: 3GP
- Video: H.263
- Resolution: 176x144 (QCIF)
- Frame rate: 15 FPS
- Video bitrate: 96 kbps CBR
- Audio: AMR-NB, 12.2 kbps, 8 kHz, mono

The next streaming milestone is an RTSP endpoint so compatible Windows Mobile devices can open a video through Streaming Media.

## Upload policy

Video uploads are intended for **PC users only**. The mobile site is for browsing and watching videos; the Flask upload endpoint rejects recognized mobile user agents.

## Development server

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Then start MobileTube:

```bash
python server/app.py
```

The development server listens on port `8000`.

## Current milestone

1. Lightweight 2009-inspired interface.
2. Static homepage generator.
3. PC-only upload foundation.
4. Legacy 3GP video storage.
5. RTSP/Streaming Media support next.
