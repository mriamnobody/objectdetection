import os
import cv2
import time
import redis
import threading
from ultralytics import YOLO
from datetime import datetime
from datetime import timedelta

# Configuration

CAMERA_CONFIG = {"DiningHall2Lawn":"rtsp://", "Lawn2MainGate":"rtsp://", "Garage2Servant":"rtsp://", "Servant2Garage":"rtsp://", "Garage2MainGate":"rtsp://"}

FRAMES_PER_SECOND = 3
BASE_IMAGE_SAVE_PATH = r'C:\Users\rosha\Downloads\objectdetection\savedimages'
IMAGE_SAVE_PATH = {camera: os.path.join(BASE_IMAGE_SAVE_PATH, camera) for camera in CAMERA_CONFIG.keys()}
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)  # Adjust host and port as needed

# Test camera connection
def test_camera_connection(rtsp_url, camera_name):
    cap = cv2.VideoCapture(rtsp_url)
    if cap.isOpened():
        print(f"Successfully connected to camera {camera_name}.")
        cap.release()
        return True
    else:
        print(f"Failed to connect to camera {camera_name}.")
        return False

# Capture frames from cameras
def capture_frames(rtsp_url, camera_name, redis_client):
    cap = cv2.VideoCapture(rtsp_url)
    camera_folder = IMAGE_SAVE_PATH[camera_name]
    if not os.path.exists(camera_folder):
        os.makedirs(camera_folder)

    try:
        while True:
            current_time = datetime.utcnow()
            next_second = (current_time.replace(microsecond=0) + timedelta(seconds=1)).timestamp()

            intervals = [0, 0.5, 0.99]  # adjust if necessary
            for offset in intervals:
                target_time = next_second + offset
                time_to_sleep = max(target_time - time.time(), 0)
                time.sleep(time_to_sleep)
                ret, frame = cap.read()
                if ret:
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    image_name = os.path.join(camera_folder, f"{camera_name}_{timestamp}.jpg")
                    cv2.imwrite(image_name, frame)
                    redis_client.rpush('camera_queue', image_name)
                else:
                    print(f"Failed to read frame for camera {camera_name}.")
                    break
    except Exception as e:
        print(f"An error occurred with camera {camera_name}: {e}")
    finally:
        cap.release()

# Process images from Redis queue
def process_images_from_queue(redis_client, model):
    while True:
        if redis_client.llen('camera_queue') > 0:
            image_path = redis_client.lpop('camera_queue').decode('utf-8')
            try:
                results = model(image_path)
                # Process results as needed
                time.sleep(1)
            except Exception as e:
                print(f"An error occurred while processing {image_path}: {e}")
        else:
            time.sleep(0.5)

# Main function
def main():

    model = YOLO("yolov8n.yaml")  # Assuming these files are correctly set up
    model.train(data="coco128.yaml", epochs=3)

    all_cameras_connected = all(test_camera_connection(url, name) for name, url in CAMERA_CONFIG.items())

    if all_cameras_connected:
        print('All cameras are connected. Capturing and saving of frames has started')
        threads = []
        for camera_name, rtsp_url in CAMERA_CONFIG.items():
            thread = threading.Thread(target=capture_frames, args=(rtsp_url, camera_name, redis_client))
            thread.start()
            threads.append(thread)

        # Start thread for processing images
        process_thread = threading.Thread(target=process_images_from_queue, args=(redis_client, model))
        process_thread.start()
        threads.append(process_thread)

        for thread in threads:
            thread.join()
    else:
        print("Not all cameras could be connected. Exiting.")

if __name__ == "__main__":
    main()

