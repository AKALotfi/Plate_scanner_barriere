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
