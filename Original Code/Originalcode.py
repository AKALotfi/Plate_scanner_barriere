import cv2
import easyocr
import time

harcascade = "model/haarcascade_russian_plate_number.xml"

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)  # height

min_area = 500
capture_cooldown = 5
last_capture = 0


reader = easyocr.Reader(['en'])


plate_cascade = cv2.CascadeClassifier(harcascade)

while True:
    ret, img = cap.read()

    if not ret:
        print("Error capturing frame")
        break

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=4)

    for (x, y, w, h) in plates:
        area = w * h

        if area > min_area:
            # Draw rectangle around the plate
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            # Extract the region of interest (ROI) for OCR
            img_roi = img[y: y + h, x: x + w]

            # Perform OCR on the ROI
            result = reader.readtext(img_roi)
            for (bbox, text, prob) in result:
                # Display the detected plate text
                print(f"Detected Plate: {text}")
                # Draw text on the main frame
                cv2.putText(img, text, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
