# main.py
import cv2
import easyocr
import RPi.GPIO as GPIO
import time
import re

# --- GPIO Setup ---
RELAY_PIN = 18  # Change if using a different GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay OFF (assumes active-low)

def open_barrier():
    print("🔓 Opening barrier...")
    GPIO.output(RELAY_PIN, GPIO.LOW)   # Turn ON relay
    time.sleep(3)                      # Keep open 3 seconds
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn OFF
    print("🔒 Barrier closed")

# --- Load Authorized Plates from File ---

def clean_text(text):
    return re.sub(r'[^A-Za-z0-9]', '', text.upper())

try:
    with open("authorized.txt", "r") as f:
        authorized_plates = [clean_text(line) for line in f if line.strip()]
except FileNotFoundError:
    print("⚠️ authorized.txt not found. Using fallback list.")
    authorized_plates = ["ABC123", "XYZ789"]

print("✅ Authorized plates:", authorized_plates)

# --- Camera & Detection ---
harcascade = "haarcascade_russian_plate_number.xml"
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Better for Pi
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Load cascade
plate_cascade = cv2.CascadeClassifier(harcascade)
if plate_cascade.empty():
    print("❌ Error: Cannot load Haar Cascade XML. Check filename and integrity.")
    exit()

# Initialize EasyOCR (CPU-only, English)
reader = easyocr.Reader(['en'], gpu=False, model_storage_directory='.', download_enabled=False)


last_capture = 0
CAPTURE_COOLDOWN = 5  # seconds

print("🟢 Starting plate scanner... Press [q] to quit.")

try:
    while True:
        ret, img = cap.read()
        if not ret:
            print("❌ Failed to capture image")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 10))

        current_time = time.time()

        for (x, y, w, h) in plates:
            area = w * h
            if area > 500:
                # Draw box
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, "Plate", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 1)

                roi = img[y:y+h, x:x+w]

                # OCR only after cooldown
                if current_time - last_capture > CAPTURE_COOLDOWN:
                    result = reader.readtext(roi, detail=0, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                    for text in result:
                        cleaned = clean_text(text)
                        print(f"🔍 Scanned: {cleaned}")

                        if cleaned in authorized_plates:
                            print(f"✅ Access granted: {cleaned}")
                            open_barrier()
                        else:
                            print(f"❌ Denied: {cleaned}")

                    last_capture = current_time

        # Optional: Show video (disable if headless)
        cv2.imshow("Scanner", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n👋 Program stopped by user.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
    print("🧹 Clean exit: resources released.")