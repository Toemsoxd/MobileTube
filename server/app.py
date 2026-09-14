import html
import os
from pathlib import Path
from urllib.parse import quote

from flask import Flask, abort, request, send_file, send_from_directory
from werkzeug.utils import secure_filename

ROOT = Path(__file__).resolve().parent.parent
VIDS = ROOT / "vids"
WEB = ROOT / "web"

VIDS.mkdir(exist_ok=True)

app = Flask(__name__, static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1 GB
RTSP_BASE_URL = os.environ.get("RTSP_BASE_URL", "rtsp://localhost:8554").rstrip("/")


def is_mobile_user_agent(user_agent: str) -> bool:
    ua = user_agent.lower()
    mobile_markers = (
        "android", "iphone", "ipad", "ipod", "windows phone",
        "windows ce", "iemobile", "opera mini", "opera mobi",
        "mobile safari",
    )
    return any(marker in ua for marker in mobile_markers)


def video_title(filename: str) -> str:
    title = Path(filename).stem
    title = title.replace("+", " ").replace("_", " ").replace("-", " ")
    return " ".join(title.split())


def rtsp_path(filename: str) -> str:
    return Path(filename).stem


def render_index() -> str:
    videos = sorted(
        (path for path in VIDS.iterdir() if path.is_file() and path.suffix.lower() == ".3gp"),
        key=lambda path: path.name.lower(),
    )

    items = []
    for video in videos:
        filename = video.name
        stream_url = f"{RTSP_BASE_URL}/{quote(rtsp_path(filename))}"
        title = html.escape(video_title(filename))
        items.append(f'''<div class="video-item">
    <div class="video-thumb">VIDEO</div>
    <div class="video-info">
        <div class="video-title"><a href="{html.escape(stream_url, quote=True)}">{title}</a></div>
        <div class="video-meta">RTSP &bull; 3GP video &bull; Legacy mobile format</div>
    </div>
</div>''')

    video_list = "\n".join(items) if items else '<p>No videos available.</p>'

    return f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MobileTube - YouTube on the go!</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
<div id="page">
    <div id="masthead">
        <div id="topbar"></div>
        <div id="header">
            <a id="brand" href="/"><img src="/MobileTubeLog.png" alt="MobileTube"></a>
            <span id="tagline">YouTube on the go!</span>
            <div id="nav">
                <a href="/">Home</a>
                <a href="#videos">Videos</a>
                <a href="/web/upload.html">Upload from PC</a>
            </div>
        </div>
    </div>
    <div id="content">
        <h1>MobileTube</h1>
        <p id="intro">Watch videos on the go, even on older mobile devices.</p>
        <h2 id="videos">Videos</h2>
        <div class="video-list">
            {video_list}
        </div>
    </div>
    <div id="footer">
        MobileTube &mdash; YouTube on the go! &nbsp;|&nbsp;
        <a href="/web/upload.html">Upload a video from PC</a>
    </div>
</div>
</body>
</html>'''


@app.get("/")
def index():
    return render_index()


@app.get("/style.css")
def stylesheet():
    return send_from_directory(ROOT, "style.css", mimetype="text/css")


@app.get("/MobileTubeLog.png")
def logo():
    return send_from_directory(ROOT, "MobileTubeLog.png")


@app.get("/web/<path:filename>")
def web_files(filename: str):
    return send_from_directory(WEB, filename)


@app.get("/vids/<path:filename>")
def videos(filename: str):
    requested = VIDS / filename
    if requested.suffix.lower() != ".3gp" or not requested.is_file():
        abort(404)

    return send_file(
        requested,
        mimetype="video/3gpp",
        as_attachment=False,
        conditional=True,
    )


@app.post("/upload")
def upload():
    if is_mobile_user_agent(request.headers.get("User-Agent", "")):
        abort(403, description="Mobile uploads are disabled. Please use a PC.")

    video = request.files.get("video")
    if video is None or not video.filename:
        abort(400, description="No video was selected.")

    filename = secure_filename(video.filename)
    if not filename:
        abort(400, description="Invalid filename.")

    destination = VIDS / filename
    if destination.exists():
        stem = destination.stem
        suffix = destination.suffix
        number = 2
        while destination.exists():
            destination = VIDS / f"{stem}-{number}{suffix}"
            number += 1

    video.save(destination)
    return f"Video uploaded successfully: {destination.name}", 201


@app.errorhandler(413)
def too_large(_error):
    return "Video is too large. The current limit is 1 GB.", 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), debug=True)
