#!/usr/bin/env python3
"""Resolve a YouTube video through Invidious and transcode it for MobileTube RTSP."""

import json
import os
import re
import urllib.parse
import urllib.request

INVIDIOUS_BASE = os.environ.get("INVIDIOUS_BASE", "https://inv.nadeko.net").rstrip("/")
MTX_PATH = os.environ.get("MTX_PATH", "")
VIDEO_ID = MTX_PATH.removeprefix("yt-").strip("/")

if not re.fullmatch(r"[A-Za-z0-9_-]{11}", VIDEO_ID):
    raise SystemExit("Invalid YouTube video ID in MTX_PATH")

api_url = f"{INVIDIOUS_BASE}/api/v1/videos/{urllib.parse.quote(VIDEO_ID)}"
with urllib.request.urlopen(api_url, timeout=15) as response:
    data = json.load(response)

streams = data.get("formatStreams", [])
if not streams:
    raise SystemExit("Invidious returned no progressive format streams")

def height(stream):
    match = re.search(r"(\d+)p", stream.get("qualityLabel", ""))
    return int(match.group(1)) if match else 0

# Prefer a progressive source around 240p/360p so the server does not pull
# an unnecessarily huge YouTube stream before reducing it for the phone.
low_res = [s for s in streams if 0 < height(s) <= 360]
stream = max(low_res or streams, key=height)

source_url = stream.get("url")
if not source_url:
    raise SystemExit("Selected Invidious stream has no URL")

# "240p" here means a 240-pixel target height, while preserving the source
# aspect ratio. The S730 can scale the resulting picture to its 320x240 LCD.
args = [
    "ffmpeg", "-hide_banner", "-loglevel", "warning",
    "-re", "-i", source_url,
    "-vf", "scale=-2:240",
    "-r", "15",
    "-pix_fmt", "yuv420p",
    "-c:v", "h263",
    "-b:v", "192k",
    "-c:a", "libopencore_amrnb",
    "-ar", "8000",
    "-ac", "1",
    "-b:a", "12.2k",
    "-f", "rtsp",
    f"rtsp://127.0.0.1:$RTSP_PORT/$MTX_PATH",
]
os.execvp(args[0], args)
