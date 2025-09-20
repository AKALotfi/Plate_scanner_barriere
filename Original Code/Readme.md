# This folder contains the original code of this project
You will find in this folder, the original code we used to work on this project
This code uses a specialized Haar Cascade classifier trained specifically to detect Russian-style license plates in images or video frames. It’s part of OpenCV’s collection of pre-trained models and is used in vehicle surveillance, traffic monitoring, and automated toll systems.

This code reads in real time the plate seen in the camera, printing it on your terminal.
We used this specified Haar Cascade classifier to read plate numbers, (due to the algerian regulation having only numbers on it) but you can also read any type of plate

## Hardware Constraints

This code was originally developed to run in real time on a standard machine. However, for deployment on a **Raspberry Pi 3**, certain modifications will be necessary.

Due to the limited resources of the Raspberry Pi 3:
- Real-time detection may not be smooth or reliable.
- The code will be adjusted to:
  - Capture an image when a license plate is detected.
  - Process the captured image separately to extract the license plate number.

These changes aim to ensure better performance on low-power hardware.
