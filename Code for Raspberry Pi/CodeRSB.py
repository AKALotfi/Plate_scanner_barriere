import cv2
import pytesseract
import time

harcascade = "model/haarcascade_russian_plate_number.xml"

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)  # height

min_area = 500
capture_cooldown = 5
last_capture = 0

#The OCR has been updated here, from EasyOCR to Tesseract

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

            # ROI = region of interest of the picture we would need to read the plate
            img_roi = img[y: y + h, x: x + w]

            # -NOTES-
            # The following code has been updated right here, going from real time reading to reading the Snapshot 
          
            #Save the plate as an image
            if time.time() - last_capture > capture_cooldown:
                filename = f"captures/plate_{int(time.time())}.jpg"
                cv2.imwrite(filename, img_roi)
                print(f"Snapshot saved: {filename}")

                gray_roi=cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
                gray_roi=cv2.equalizeHist(gray_roi)
                resized_roi=cv2.resize(gray_roi,(w*2,h*2))

                text = pytesseract.image_to_string(resized_roi, config='--psm 7')
                print(f"OCR result: {text.strip()}")

                #Prepare a sleep for the Rasp Pi for a better performance
                #Haar cascade can read up to 20 ou 30 degrees 

                #result = reader.readtext(img_roi)
                last_capture=time.time()



    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
