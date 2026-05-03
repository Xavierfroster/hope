import cv2
import os
import numpy as np
from hope import config

TRAINING_DIR = os.path.join(config.LEARNING_DIR, "faces")

def init_vision():
    if not os.path.exists(TRAINING_DIR):
        os.makedirs(TRAINING_DIR)
    
    if not os.path.exists(config.RESOURCES_DIR):
        os.makedirs(config.RESOURCES_DIR)

def enroll_face(name="User"):
    """Captures 30 photos of the user to 'learn' their face."""
    cam = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    print(f"Face Enrollment started for {name}. Look at the camera...")
    count = 0
    
    while True:
        ret, frame = cam.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            count += 1
            # Save the captured face image
            cv2.imwrite(f"{TRAINING_DIR}/{name}.{count}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow('Enrolling Face - Stay Still', frame)
            
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 30:
            break
            
    cam.release()
    cv2.destroyAllWindows()
    return count >= 30

def recognize_face():
    """Attempts to recognize the face in the camera feed."""
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except AttributeError:
        return "ERROR: Please run 'pip install opencv-contrib-python' for face recognition."

    # Logic to train on the fly if needed, or load a saved model
    # For simplicity, we'll return a placeholder if no data exists
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    image_paths = [os.path.join(TRAINING_DIR, f) for f in os.listdir(TRAINING_DIR)]
    face_samples = []
    ids = []
    
    if not image_paths:
        return "UNKNOWN"

    for image_path in image_paths:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        face_samples.append(img)
        ids.append(1) # For now, just one user
        
    recognizer.train(face_samples, np.array(ids))
    
    cam = cv2.VideoCapture(0)
    recognized_user = "UNKNOWN"
    
    while True:
        ret, frame = cam.read()
        if not ret: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if confidence < 100:
                recognized_user = "MASTER"
            else:
                recognized_user = "STRANGER"
            break
        
        if recognized_user != "UNKNOWN" or cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cam.release()
    cv2.destroyAllWindows()
    return recognized_user
