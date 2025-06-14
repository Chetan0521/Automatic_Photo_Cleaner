import cv2
import face_recognition
import numpy as np
from PIL import Image

def has_face(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    return len(face_locations) > 0

def are_eyes_open(image_path):
    image = face_recognition.load_image_file(image_path)
    landmarks_list = face_recognition.face_landmarks(image)

    for landmarks in landmarks_list:
        if 'left_eye' in landmarks and 'right_eye' in landmarks:
            # Calculate eye openness based on vertical eye height
            left_eye = landmarks['left_eye']
            right_eye = landmarks['right_eye']

            def eye_openness(eye):
                return np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))

            if eye_openness(left_eye) > 2.0 and eye_openness(right_eye) > 2.0:
                return True
    return False

def image_resolution(image_path):
    with Image.open(image_path) as img:
        return img.size[0] * img.size[1]

def image_sharpness(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return cv2.Laplacian(img, cv2.CV_64F).var()

def image_brightness(image_path):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    brightness = hsv[..., 2].mean()
    return brightness

def score_image(image_path):
    score = 0

    resolution = image_resolution(image_path)
    sharpness = image_sharpness(image_path)
    brightness = image_brightness(image_path)

    if has_face(image_path):
        score += 30  # Face present

        if are_eyes_open(image_path):
            score += 30  # Eyes open

        # Add sharpness score (capped at 100)
        score += min(sharpness, 100) * 0.3  # Max 30 pts

        # Add brightness score (ideal range: 80–200)
        score += max(0, min(brightness, 200)) * 0.1  # Max 20 pts

        # Resolution: 1 point per 0.5 megapixel, capped at 40 pts
        score += min((resolution / 500000), 40)

    else:
        score -= 100  # No face = disqualified

    return round(score, 2)




