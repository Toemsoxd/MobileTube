# MobileTube RTSP

MobileTube opens videos as RTSP links instead of sending the phone to a normal HTTP video file.

The web frontend can live on KESUG or another shared web host, while the RTSP service runs on a machine/VPS that can expose an RTSP port.

## Test server

The repository includes `mediamtx.yml` for the first test video. It uses MediaMTX as the RTSP server and FFmpeg to publish the existing 3GP file only when a client requests the stream.

MediaMTX documents this `runOnDemand` pattern and supports H.263 as an MPEG-4 video codec. The RTSP server normally listens on TCP port 8554. See the upstream MediaMTX documentation for deployment details.

## Generate the website with the RTSP server address

From the repository root:

```text
python tools/generate_static.py --rtsp-base rtsp://YOUR-RTSP-SERVER:8554
```

The generated homepage will contain links such as:

```text
rtsp://YOUR-RTSP-SERVER:8554/super-mario-bros-in-first-person
```

Opera Mobile 10 can then hand the RTSP link to the phone's native Streaming Media application.

## Important hosting note

KESUG provides normal web-hosting features such as PHP/MySQL, but that does not mean a user can run an arbitrary long-lived RTSP daemon or open TCP/8554. The RTSP endpoint must therefore be verified separately before calling the deployment complete.
