# Face Recognition with Object Tracking

## Overview
This project implements a face recognition system integrated with object tracking capabilities. It tracks individuals in real-time and monitors their attendance based on specified time intervals. If a person is late, leaves early, or reaches the end of the designated time, the system will trigger alerts. The data is stored and managed using Firebase Realtime Database.

## Features
- **Real-Time Face Recognition**: Utilizes advanced algorithms to recognize faces in real-time.
- **Object Tracking**: Tracks the movement of recognized individuals across frames.
- **Attendance Monitoring**: Records attendance based on time intervals (arrival, departure, and total time).
- **Alerts for Late Arrivals**: Notifies users if an individual arrives late. (Soon alret in using bot Telegram)
- **Firebase Integration**: Stores attendance data and user information in Firebase Realtime Database for easy access and management.

## Technologies Used
- Python
- OpenCV
- dlib or Face Recognition Library
- Firebase Realtime Database
- NumPy
- Face_recognition lib (https://github.com/ageitgey/face_recognition)

## Installation

### Prerequisites
Make sure you have Python 3.x installed on your machine. You also need to install the required libraries:

```bash
pip install opencv-python dlib firebase-admin numpy
