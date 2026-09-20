#!/usr/bin/env python3
"""Resolve a YouTube video through Invidious and transcode it to RTSP."""
import json, os, re, subprocess, sys, urllib.parse, urllib.request

INVIDIOUS_API = os.environ.get("INVIDIOUS_API", "https://yewtu.be/api/v1").rstrip("/")
RTSP_TARGET = os.environ.get("RTSP_TARGET", "rtsp://127.0.0.1:8554").rstrip("/")
VIDEO_HEIGHT = int(os.environ.get("MOBILETUBE_HEIGHT", "240"))
VIDEO_FPS = int(os.environ.get("MOBILETUBE_FPS", "15"))
VIDEO_BITRATE = os.environ.get("MOBILETUBE_VIDEO_BITRATE", "180k")

def get_video_id(path):
    value = path.rstrip("/").split("/")[-1]
    if not re.fullmatch(r"[A-Za-z0-9_-]{6,20}", value):
        raise ValueError("Invalid video id")
    return value

def get_invidious_video(video_id):
    url = f"{INVIDIOUS_API}/videos/{urllib.parse.quote(video_id)}"
    with urllib.request.urlopen(url, timeout=20) as response:
        return json.load(response)

def choose_source(data):
    candidates = []
    for item in data.get("formatStreams", []):
        url = item.get("url")
        if not url:
            continue
        try:
            height = int(item.get("height") or 0)
        except (TypeError, ValueError):
            height = 0
        candidates.append((height, url))
    if not candidates:
        raise RuntimeError("Invidious returned no progressive video stream")
    above = [item for item in candidates if item[0] >= VIDEO_HEIGHT]
    return min(above or candidates, key=lambda item: abs(item[0] - VIDEO_HEIGHT))[1]

def main():
    if len(sys.argv) != 2:
        print("Usage: stream_youtube.py <video-id>", file=sys.stderr)
        return 2
    video_id = get_video_id(sys.argv[1])
    stream_url = choose_source(get_invidious_video(video_id))
    target = f"{RTSP_TARGET}/{video_id}"
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "warning", "-re", "-i", stream_url,
        "-vf", f"scale=-2:{VIDEO_HEIGHT}:flags=bicubic", "-r", str(VIDEO_FPS),
        "-c:v", "h263", "-b:v", VIDEO_BITRATE,
        "-c:a", "libopencore_amrnb", "-ar", "8000", "-ac", "1", "-b:a", "12.2k",
        "-f", "rtsp", "-rtsp_transport", "tcp", target,
    ]
    return subprocess.call(command)

if __name__ == "__main__":
    raise SystemExit(main())
