"""
This script captures video from the default webcam, detects vehicle number plates using a Haar Cascade classifier,
and performs Optical Character Recognition (OCR) on detected plates using EasyOCR. Detected plates are highlighted
with rectangles and annotated with recognized text in real-time.
Modules:
    - cv2: OpenCV library for image processing and video capture.
    - easyocr: Library for performing OCR on images.
Workflow:
    1. Load Haar Cascade model for Russian number plate detection.
    2. Initialize webcam video capture and set frame dimensions.
    3. Continuously read frames from the webcam.
    4. Convert each frame to grayscale and detect number plates.
    5. For each detected plate:
        - Draw a rectangle around the plate.
        - Extract the region of interest (ROI).
        - Perform OCR on the ROI to recognize text.
        - Display recognized text on the frame and print it to the console.
    6. Display the processed video stream in a window.
    7. Exit the loop and release resources when 'q' is pressed.
Attributes:
    harcascade (str): Path to the Haar Cascade XML file for plate detection.
    cap (cv2.VideoCapture): Video capture object for webcam.
    min_area (int): Minimum area threshold for detected plates.
    capture_cooldown (int): Cooldown time between captures (unused in current code).
    last_capture (int): Timestamp of last capture (unused in current code).
    reader (easyocr.Reader): EasyOCR reader instance for English language.
    plate_cascade (cv2.CascadeClassifier): Cascade classifier for plate detection.
"""
