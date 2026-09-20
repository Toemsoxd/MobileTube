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
- Bridge modern YouTube videos through Invidious and transcode them on demand.

## Repository layout

```text
MobileTube/
├── index.html             # Static homepage for simple hosting
├── vids/                  # Legacy-compatible local video files
├── web/                   # Additional web pages
├── server/                # Flask development/backend server
├── rtsp/
│   ├── mediamtx.yml       # Dynamic RTSP server configuration
│   └── README.md           # RTSP deployment notes
├── tools/
│   ├── generate_static.py  # Rebuilds index.html from vids/
│   └── stream_youtube.py   # Invidious -> FFmpeg -> MediaMTX helper
└── README.md
```

## Static hosting

MobileTube is designed so the frontend can be copied to a static host. No JavaScript is required for the basic catalog.

When videos are added or removed, regenerate the static homepage with:

```bash
python tools/generate_static.py
```

For an RTSP deployment, pass the public RTSP server address:

```bash
python tools/generate_static.py --rtsp-base rtsp://YOUR-RTSP-SERVER:8554
```

## YouTube -> RTSP pipeline

The dynamic streaming path is:

```text
YouTube
   ↓
Invidious API
   ↓
FFmpeg
   ↓
MediaMTX
   ↓
RTSP/TCP
   ↓
Windows Mobile Streaming Media
```

A YouTube video ID such as `dQw4w9WgXcQ` becomes:

```text
rtsp://YOUR-RTSP-SERVER:8554/yt-dQw4w9WgXcQ
```

MediaMTX starts the helper only when that path is requested. The helper resolves the ID through the configured Invidious instance and transcodes the result in real time.

Set the Invidious instance with:

```bash
export INVIDIOUS_BASE=https://YOUR-INVIDIOUS-INSTANCE
```

The default is a public instance for testing; for a permanent deployment, use an instance you control or one you have verified is operational.

## Video target

MobileTube targets a **240p-quality stream**, without forcing every source into a 4:3 frame. The FFmpeg pipeline preserves the source aspect ratio and uses a 240-pixel target height.

The current legacy output is:

- Video: H.263
- Target height: 240 pixels
- Frame rate: 15 FPS
- Video bitrate: 192 kbps CBR
- Pixel format: YUV420P
- Audio: AMR-NB, 12.2 kbps, 8 kHz, mono
- Transport: RTSP over TCP

This is intentionally aimed at the S730/Windows Mobile generation rather than modern browsers.

## Local 3GP playback

The existing `vids/` upload path remains available for locally stored 3GP files. These are useful for testing the S730 decoder before involving YouTube/Invidious.

## RTSP deployment

MediaMTX normally listens on TCP port 8554. Its `runOnDemand` hook starts FFmpeg only when a client requests a path, and MediaMTX exposes `$MTX_PATH` and `$RTSP_PORT` to the hook. citeturn1search0turn1search1

Install:

- MediaMTX
- FFmpeg with H.263 and AMR-NB encoder support
- Python 3

Run MediaMTX from the repository root:

```bash
./mediamtx rtsp/mediamtx.yml
```

Then test a stream:

```text
rtsp://YOUR-RTSP-SERVER:8554/yt-dQw4w9WgXcQ
```

The S730 should receive the RTSP stream through its native Streaming Media player.

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
5. Dynamic Invidious -> FFmpeg -> MediaMTX RTSP pipeline.
