import cv2
import easyocr
import time
import re

# --- Configuration ---
harcascade = "haarcascade_russian_plate_number.xml"
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)  # height

min_area = 500
capture_cooldown = 2
last_capture = 0

# --- Load Models ---
reader = easyocr.Reader(['en'])

plate_cascade = cv2.CascadeClassifier(harcascade)
if plate_cascade.empty():
    print("❌ ERROR: Failed to load Haar Cascade.")
    print("💡 Download from: https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_russian_plate_number.xml")
    exit()
else:
    print("✅ Cascade loaded successfully!")

def clean_text(text):
    return re.sub(r'[^A-Za-z0-9]', '', text.upper())

while True:
    ret, img = cap.read()
    if not ret:
        print("❌ Error: Failed to capture image")
        break

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.equalizeHist(img_gray)

    plates = plate_cascade.detectMultiScale(img_gray, scaleFactor=1.05, minNeighbors=5)

    current_time = time.time()

    for (x, y, w, h) in plates:
        area = w * h
        if area > min_area:
            # Draw bounding box
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "Plate", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

            # Extract and preprocess ROI
            roi = img[y:y+h, x:x+w]
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            roi_gray = cv2.resize(roi_gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            _, roi_thresh = cv2.threshold(roi_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # OCR
            if current_time - last_capture > capture_cooldown:
                result = reader.readtext(roi_thresh, detail=1, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                for bbox, text, prob in result:
                    cleaned = clean_text(text)
                    if len(cleaned) >= 5 and prob > 0.3:
                        print(f"🟢 Plate: {cleaned} (Confidence: {prob:.2f})")
                        cv2.putText(img, cleaned, (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                last_capture = current_time

    cv2.imshow("License Plate Scanner", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()