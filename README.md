# Hand Gesture Controlled Virtual Mouse

This project implements a virtual mouse that can be controlled using hand gestures detected via a webcam. The system uses **MediaPipe** for hand tracking and **PyAutoGUI** for controlling the mouse pointer and performing click actions. This innovative approach replaces the need for a physical mouse, making it a fun and futuristic way to interact with your computer.

---

## Features
- **Real-Time Mouse Control**: Move the mouse pointer by simply moving your index finger.
- **Click Action**: Perform a click when the index finger and thumb come close to each other.
- **Gesture Detection**: Uses hand landmarks provided by MediaPipe for precise gesture recognition.
- **Seamless Integration**: Works with any screen resolution by dynamically mapping hand movements to screen coordinates.

---

## How It Works
1. **Hand Tracking**: 
   - The program uses MediaPipe's Hands solution to detect and track the hand's landmarks in real time.
   - Each landmark is identified by a unique ID.

2. **Mouse Movement**:
   - The position of the index finger (landmark ID 8) is mapped to the screen dimensions, allowing the user to move the mouse pointer.

3. **Click Detection**:
   - When the distance between the index finger and thumb (landmark ID 4) is small, a click action is performed.

4. **Smooth Interaction**:
   - OpenCV is used to process the video feed, and PyAutoGUI ensures smooth and responsive mouse actions.

---

## Requirements
Make sure you have the following installed:
- Python 3.7 or above
- OpenCV
- MediaPipe
- PyAutoGUI

Install the dependencies with:
```bash
pip install opencv-python mediapipe pyautogui
