Real-time license plate detection and recognition using a camera connected to a Raspberry Pi.

Key functions:
Captures live video from the camera.

Uses a Haar Cascade classifier to detect license plates in each frame.

Performs OCR (text recognition) on detected plates using EasyOCR.

Cleans and standardizes the recognized text.

Checks the plate against a list of authorized plates stored in authorized.txt.

If the plate is authorized:

🟢 The code triggers a GPIO relay to open a barrier for 3 seconds.

If the plate is not authorized:

❌ Displays "Access Denied" in the console.

Optionally displays the live video feed with bounding boxes around detected plates.

✅ This system is fully automated and ideal for real-world use cases like:

Parking gate access,

Automatic vehicle entry control.

## Hello, this is the second contributor (and first creator of the project - Lotfi)

- I came here to add some details to the project to make it better.
- To optimize performance on Raspberry Pi 3, we capture snapshots for OCR instead of processing every video frame., being too consuming for a Raspberry Pi 3, rather than that, We should take a picture (Snapshot) of the plate to use the OCR on it and read it.
- We use EasyOCR to read the plate in real time, we can use another OCR (below)
- So this is a real time reader of plate numbers using EasyOCR, the thing is, for a PC it's pretty good, however for a Raspberry Pi, it's kinda heavy for it, therefore i recommand you to to use Tesseract OCR.
- More informations will be updated later.
