import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self, max_hands=1, model_complexity=1):
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            model_complexity=model_complexity,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

    def process_frame(self, frame):
        if frame is None or frame.size == 0:
            return None
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if not results.multi_hand_landmarks:
            return None
            
        return {
            'landmarks': results.multi_hand_landmarks,
            'multi_handedness': results.multi_handedness
        }
    
    def get_index_tip_coords(self, landmarks, frame_shape):
        if not landmarks:
            return None
        h, w = frame_shape[:2]
        landmark = landmarks[0].landmark[8]
        return (int(landmark.x * w), int(landmark.y * h))