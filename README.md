# Object Detection

# Multi-Camera Object Detection System

## Description

This small script is an extension of Ultralytics YOLOV8 repo https://github.com/ultralytics/ultralytics, an advanced object detection system capable of handling multiple IP camera streams simultaneously. It notably enhances the original model's single-stream processing by integrating Redis, a robust in-memory database, to manage real-time video feeds from various cameras efficiently.

## Key Features

- **Multi-Camera Support:** Connects to multiple IP cameras using RTSP URLs.
- **Continuous Frame Capture:** Captures frames at a configurable rate (default: 3 fps) from all connected cameras.
- **Redis Integration:** Uses Redis for effective queue management, ensuring timely processing of a high volume of frames.
- **Real-Time Object Detection:** Implements the YOLOV8 by Ultralytics for advanced object detection.
- **Automated Image Processing:** Automatically processes images from the Redis queue for object detection, suitable for security, traffic analysis, and more.
- **Error Handling:** Robust error handling and logging are included for smooth operation and troubleshooting.
- **Multithreading:** Leverages Python threading for concurrent frame capture and image processing without blocking.

## Technical Stack

- **Python:** For the core logic.
- **OpenCV (cv2):** To capture frames from camera streams.
- **Redis:** As an in-memory database to manage the image queue.
- **Ultralytics YOLO:** For cutting-edge object detection. https://github.com/ultralytics/ultralytics
- **Threading:** To efficiently manage concurrent processes.

## Customization and Flexibility

Designed for easy customization, users can adjust camera URLs, frame rates, and YOLO model configurations, making it versatile for various applications.

## How It Works

1. **Camera Connection:** Tests connections to multiple camera streams.
2. **Frame Capture:** Captures and stores frames from each stream.
3. **Redis Queueing:** Frames are queued in Redis.
4. **Image Processing:** A separate thread processes images using YOLO.
5. **Object Detection:** Objects are identified and classified in each frame.

## Getting Started

Clone the repository, install dependencies, and follow the README for setup instructions. Designed for easy deployment, the script can be operational with minimal configuration.

---

**Note:** This project extends the original YOLO object detection model by Ultralytics at https://github.com/ultralytics/ultralytics, showcasing advanced application development with Python, Redis, and real-time data processing techniques.
