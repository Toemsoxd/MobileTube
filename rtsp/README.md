# MobileTube RTSP

MobileTube uses RTSP as the bridge between the lightweight 2009-style website and Windows Mobile Streaming Media.

Architecture:

YouTube -> Invidious API -> FFmpeg -> H.263 + AMR-NB at 240p -> MediaMTX -> RTSP -> Windows Mobile

The default video height is 240 pixels. It does NOT force 4:3; FFmpeg preserves the source aspect ratio.

Configuration:
- INVIDIOUS_API=https://YOUR-INSTANCE/api/v1
- MOBILETUBE_HEIGHT=240
- MOBILETUBE_FPS=15
- MOBILETUBE_VIDEO_BITRATE=180k
- RTSP_TARGET=rtsp://127.0.0.1:8554

Run MediaMTX with rtsp/mediamtx.yml. A request for rtsp://HOST:8554/<youtube-video-id> starts FFmpeg on demand.

The prototype selects a progressive Invidious format (audio + video), scales it to 240 pixels high, and publishes H.263/AMR-NB over RTSP.

H.263 and AMR-NB are intentional legacy targets; actual playback still needs validation on the HTC S730 Streaming Media player.
