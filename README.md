# -Vithyarthi-AI-ML-project
Lane Detection Project

This project implements a basic Lane Detection System using Python and OpenCV. It detects lane lines on roads from a video file or webcam feed, which is a fundamental concept used in self-driving cars.

Features:-
Detects lane lines in real-time
Works with video files 
Uses edge detection and region masking
Simple and beginner-friendly implementation

Project Structure
Lane-Detection/

├── lane.py              
├── roadbackground short video..mp4        
├── README.md             Project documentation

 Requirements:-

Make sure you have Python installed (>=3.7)

Install dependencies:-

pip install opencv-python numpy

 How to Run:-

1. Using Video File

Place your video file in the project folder

Update the video path in the code if needed
Run:

python lane.py

2. Using Webcam

Replace video capture line with:


cv2.VideoCapture(0)

Run the same command:

python lane.py

Working Principle:-

1. Convert image to grayscale

2. Apply Gaussian blur

3. Detect edges using Canny Edge Detection

4. Mask region of interest

5. Detect lines using Hough Transform

6. Overlay detected lanes on original frame

 Common Errors & Fixes:-

 Error: No module named cv2

 Fix:

pip install opencv-python

 Error: Video not opening

 Fix:
Check file path

Ensure video format is supported (.mp4 recommended)

Notes:-
This is a basic implementation and may not work perfectly in all conditions  performance depends on lighting and road clarity
