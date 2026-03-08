"""Computer vision module using OpenCV and YOLO object detection."""

from __future__ import annotations

import cv2
from ultralytics import YOLO


class VisionSystem:
    """Runs live camera object detection and returns detected labels."""

    def __init__(self, model_name: str = "yolov8n.pt") -> None:
        self.model = YOLO(model_name)

    def detect_from_webcam(self, camera_index: int = 0) -> list[str]:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            return []

        seen_labels: set[str] = set()

        while True:
            ok, frame = cap.read()
            if not ok:
                break

            results = self.model(frame, verbose=False)
            annotated = frame

            for result in results:
                annotated = result.plot()
                for box in result.boxes:
                    cls_id = int(box.cls.item())
                    seen_labels.add(self.model.names[cls_id])

            cv2.imshow("AMAN Vision - press q to quit", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        return sorted(seen_labels)
