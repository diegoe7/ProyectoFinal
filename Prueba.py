"""
test_camera_full.py

Manual test: runs the full detect_shapes() pipeline (shape + color)
on live camera frames.
"""

import cv2
from detector_de_colores import detectar_figuras


def main():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: could not open camera.")
        return

    print("Camera started. Press 'q' to quit.")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        items = detectar_figuras(frame)

        for det in items:
            x, y, w, h = det.box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            label = f"{det.color} {det.forma}"
            cv2.putText(frame, label, (x, max(0, y - 8)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Full Detection Test", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
