# SentinelEdge Vision — Real-Time Zone Monitoring

SentinelEdge Vision is a standalone computer-vision application that detects people with an Ultralytics YOLO model and evaluates their position against a configurable restricted zone.

## Capabilities

- Camera, video-file or stream input
- Person-only detection
- Confidence threshold
- Configurable rectangular restricted zone
- Alert cooldown state handling
- CSV event logging
- Optional Windows audible alert
- FPS and event counters
- Portfolio dashboard preview asset

## Run

```bash
python -m venv .venv
```

Windows:

```bat
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
python app.py --source 0
```

Video file:

```bash
python app.py --source path/to/video.mp4
```

Press `q` to stop.

## Configuration

```bash
python app.py --source 0 --confidence 0.50 --zone 150 100 490 380
```

The source can be a local webcam index or a video path.

## Architecture

```text
Camera / Video
 -> YOLO detection
 -> person filtering
 -> zone geometry
 -> alert state and cooldown
 -> event log
 -> optional local alert
```

## Use Boundary

Use only with cameras, media and locations you are authorized to monitor. This project is a computer-vision reference implementation, not an access-control system.

## Technology

Ultralytics: https://docs.ultralytics.com/
OpenCV: https://docs.opencv.org/
Python: https://www.python.org/

Ultralytics offers AGPL-3.0 and Enterprise licensing options. Review the applicable terms before redistribution or commercial deployment.

## Visual Asset

`assets/sentinel_dashboard_preview.png` is an illustrative interface visual generated for presentation. It is not a measured runtime screenshot.

## License

Project source: MIT. Upstream library, model and license terms remain applicable.
