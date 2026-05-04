class GestureClassifier:
    FINGER_TIP_INDICES = [4, 8, 12, 16, 20]
    FINGER_BASE_INDICES = [2, 5, 9, 13, 17]
    
    def classify(self, landmarks):
        if not landmarks:
            return 'idle'
        
        hand_landmarks = landmarks[0].landmark
        extended_fingers = self._get_extended_fingers(hand_landmarks)
        
        if extended_fingers[1] and not extended_fingers[2]:
            return 'draw'
        elif extended_fingers[1] and extended_fingers[2] and not extended_fingers[3]:
            return 'toggle'
        else:
            return 'idle'
    
    def _get_extended_fingers(self, landmarks):
        fingers = []
        for tip_idx, base_idx in zip(self.FINGER_TIP_INDICES, self.FINGER_BASE_INDICES):
            tip_y = landmarks[tip_idx].y
            base_y = landmarks[base_idx].y
            fingers.append(tip_y < base_y)
        return fingers
    
    def is_two_finger_toggle(self, landmarks):
        return self.classify(landmarks) == 'toggle'