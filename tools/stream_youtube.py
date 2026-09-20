#!/usr/bin/env python3
"""Resolve a YouTube video through Invidious and transcode it for MobileTube RTSP."""

import json
import os
import re
import sys
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

# Prefer a progressive stream with the highest source quality, while keeping
# the input manageable for a low-power legacy target.
def quality(stream):
    try:
        return int(stream.get("itag", 0)), int(re.search(r"(\d+)p", stream.get("qualityLabel", "" )).group(1))
    except (AttributeError, ValueError):
        return (0, 0)

stream = max(streams, key=quality)
source_url = stream.get("url")
if not source_url:
    raise SystemExit("Selected Invidious stream has no URL")

# 240p means a 240-pixel target height while preserving the source aspect ratio.
# H.263/AMR-NB keeps the output compatible with the original MobileTube target.
args = [
    "ffmpeg", "-hide_banner", "-loglevel", "warning",
    "-re", "-i", source_url,
    "-vf", "scale=-2:240",
    "-r", "15",
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
