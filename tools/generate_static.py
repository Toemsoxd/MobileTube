"""Generate the static MobileTube homepage for simple hosting providers."""

import html
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
VIDS = ROOT / "vids"
OUTPUT = ROOT / "index.html"


def title_for(filename: str) -> str:
    title = Path(filename).stem
    title = title.replace("+", " ").replace("_", " ").replace("-", " ")
    return " ".join(title.split())


def main() -> None:
    videos = sorted(
        (p for p in VIDS.iterdir() if p.is_file() and p.suffix.lower() == ".3gp"),
        key=lambda p: p.name.lower(),
    )

    if videos:
        items = []
        for video in videos:
            filename = quote(video.name)
            title = html.escape(title_for(video.name))
            items.append(f'''<div class="video-item">
    <div class="video-thumb">VIDEO</div>
    <div class="video-info">
        <div class="video-title"><a href="vids/{filename}">{title}</a></div>
        <div class="video-meta">3GP video &bull; Legacy mobile format</div>
    </div>
</div>''')
        video_list = "\n".join(items)
    else:
        video_list = "<p>No videos available.</p>"

    OUTPUT.write_text(f'''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>MobileTube - YouTube on the go!</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div id="page">
    <div id="masthead">
        <div id="topbar"></div>
        <div id="header">
            <a id="brand" href="index.html"><img src="MobileTubeLog.png" alt="MobileTube"></a>
            <span id="tagline">YouTube on the go!</span>
            <div id="nav">
                <a href="index.html">Home</a>
                <a href="#videos">Videos</a>
                <a href="web/upload.html">Upload from PC</a>
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
        <a href="web/upload.html">Upload a video from PC</a>
    </div>
</div>
</body>
</html>\n''', encoding="utf-8")


if __name__ == "__main__":
    main()
