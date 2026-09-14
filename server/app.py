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


def is_mobile_user_agent(user_agent: str) -> bool:
    ua = user_agent.lower()
    mobile_markers = (
        "android",
        "iphone",
        "ipad",
        "ipod",
        "windows phone",
        "windows ce",
        "iemobile",
        "opera mini",
        "opera mobi",
        "mobile safari",
    )
    return any(marker in ua for marker in mobile_markers)


def video_title(filename: str) -> str:
    """Turn a video filename into a readable title."""
    title = Path(filename).stem
    title = title.replace("+", " ").replace("_", " ").replace("-", " ")
    return " ".join(title.split())


def render_index() -> str:
    """Build the video list directly from the current contents of vids/."""
    videos = sorted(
        (path for path in VIDS.iterdir() if path.is_file() and path.suffix.lower() == ".3gp"),
        key=lambda path: path.name.lower(),
    )

    items = []
    for video in videos:
        filename = video.name
        href = "/vids/" + quote(filename)
        title = html.escape(video_title(filename))
        items.append(f'<p><a href="{href}">{title}</a></p>')

    if not items:
        video_list = "<p>No videos available.</p>"
    else:
        video_list = "\n".join(items)

    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>MobileTube</title>
</head>
<body>
    <h1>MobileTube</h1>
    <p>Simple video platform for old mobile devices.</p>

    <hr>

    <h2>Videos</h2>
    {video_list}

    <hr>

    <p><a href="/web/upload.html">PC upload</a></p>
</body>
</html>
"""


@app.get("/")
def index():
    # The catalog is generated from vids/ on every request. Adding or removing
    # a .3gp file therefore changes the video list automatically.
    return render_index()


@app.get("/web/<path:filename>")
def web_files(filename: str):
    return send_from_directory(WEB, filename)


@app.get("/vids/<path:filename>")
def videos(filename: str):
    # Serve 3GP with its standard video MIME type so old browsers can
    # hand the URL to the device's media/streaming player.
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
    # Uploads are intentionally restricted to desktop browsers.
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
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
        debug=True,
    )
