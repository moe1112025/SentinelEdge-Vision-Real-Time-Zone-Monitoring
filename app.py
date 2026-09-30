from __future__ import annotations

import argparse
import csv
import platform
import time
from pathlib import Path

import cv2
from ultralytics import YOLO

from config import Settings, Zone

try:
    import winsound
except ImportError:
    winsound = None


def open_source(value):
    return cv2.VideoCapture(int(value)) if value.isdigit() else cv2.VideoCapture(value)


def sound_alert():
    if winsound is not None and platform.system().lower() == "windows":
        try:
            winsound.Beep(2200, 180)
        except RuntimeError:
            pass


def log_event(path, timestamp, confidence):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    first_write = not target.exists()
    with target.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if first_write:
            writer.writerow(["timestamp", "class", "confidence", "zone"])
        writer.writerow([timestamp, "person", f"{confidence:.4f}", "restricted"])


def parse_args():
    parser = argparse.ArgumentParser(description="Real-time person zone monitoring")
    parser.add_argument("--source", default="0")
    parser.add_argument("--model", default=Settings.model_path)
    parser.add_argument("--confidence", type=float, default=Settings.confidence)
    parser.add_argument("--zone", nargs=4, type=int, default=[Zone.left, Zone.top, Zone.right, Zone.bottom])
    parser.add_argument("--events", default="logs/events.csv")
    return parser.parse_args()


def main():
    args = parse_args()
    zone = Zone(*args.zone)
    detector = YOLO(args.model)
    capture = open_source(args.source)
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open source: {args.source}")
    last_alarm = 0.0
    frame_counter = 0
    frame_start = time.monotonic()
    fps = 0.0
    alert_count = 0
    try:
        while True:
            success, frame = capture.read()
            if not success:
                break
            result = detector.predict(frame, conf=max(0.05, min(args.confidence, 0.99)), classes=[0], verbose=False)[0]
            intrusion = False
            alert_confidence = 0.0
            for box in result.boxes:
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = [int(value) for value in box.xyxy[0].tolist()]
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                inside = zone.contains(center_x, center_y)
                if inside:
                    alert_confidence = max(alert_confidence, confidence)
                intrusion = intrusion or inside
                color = (0, 0, 255) if inside else (0, 210, 90)
                label = "ALERT" if inside else "PERSON"
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label} {confidence:.2f}", (x1, max(24, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
            cv2.rectangle(frame, (zone.left, zone.top), (zone.right, zone.bottom), (255, 180, 60), 2)
            cv2.putText(frame, "RESTRICTED ZONE", (zone.left, max(24, zone.top - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 180, 60), 2)
            if intrusion:
                current_time = time.monotonic()
                if current_time - last_alarm >= Settings.alarm_cooldown_seconds:
                    alert_count += 1
                    sound_alert()
                    log_event(args.events, time.strftime("%Y-%m-%d %H:%M:%S"), alert_confidence)
                    last_alarm = current_time
                cv2.putText(frame, "SECURITY ALERT: PERSON IN RESTRICTED ZONE", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            frame_counter += 1
            elapsed = time.monotonic() - frame_start
            if elapsed >= 1.0:
                fps = frame_counter / elapsed
                frame_counter = 0
                frame_start = time.monotonic()
            cv2.putText(frame, f"FPS {fps:.1f}  Alerts {alert_count}", (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (220, 230, 240), 2)
            cv2.imshow("SentinelEdge Vision", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
