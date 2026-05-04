import cv2
import numpy as np
from tracking import HandTracker, GestureClassifier
from drawing import DrawingCanvas
from drawing.tools import hex_to_rgb, color_to_bgr
import config

class VideoStream:
    def __init__(self):
        self.cap = None
        self.hand_tracker = HandTracker()
        self.gesture_classifier = GestureClassifier()
        self.canvas = DrawingCanvas(config.Config.CANVAS_WIDTH, config.Config.CANVAS_HEIGHT)
        self.current_tool = 'pen'
        self.current_color = hex_to_rgb(config.Config.DEFAULT_COLOR)
        self.current_size = config.Config.BRUSH_SIZE_DEFAULT
        self.is_drawing = False
        self.last_toggle_state = False
    
    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.Config.VIDEO_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.Config.VIDEO_HEIGHT)
    
    def stop(self):
        if self.cap:
            self.cap.release()
    
    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        frame = cv2.flip(frame, 1)
        
        result = self.hand_tracker.process_frame(frame)
        
        if result and result.get('landmarks'):
            landmarks = result['landmarks']
            gesture = self.gesture_classifier.classify(landmarks)
            
            index_tip = self.hand_tracker.get_index_tip_coords(landmarks, frame.shape)
            
            if index_tip:
                if gesture == 'draw':
                    if not self.is_drawing:
                        self.canvas.start_stroke(index_tip, color_to_bgr(self.current_color), 
                                                  self.current_size, self.current_tool)
                        self.is_drawing = True
                    else:
                        self.canvas.add_point_to_current(index_tip)
                else:
                    if self.is_drawing:
                        self.canvas.end_stroke()
                        self.is_drawing = False
                
                current_toggle = self.gesture_classifier.is_two_finger_toggle(landmarks)
                if current_toggle and not self.last_toggle_state:
                    self.current_tool = 'eraser' if self.current_tool == 'pen' else 'pen'
                self.last_toggle_state = current_toggle
                
                cv2.circle(frame, index_tip, 10, (0, 255, 0), -1)
        
        canvas_overlay = self.canvas.render()
        combined = cv2.addWeighted(frame, 0.7, canvas_overlay, 0.3, 0)
        
        return combined
    
    def get_jpeg_frame(self):
        frame = self.process_frame()
        if frame is None:
            return None
        _, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return jpeg.tobytes()
    
    def set_tool(self, tool):
        self.current_tool = tool
    
    def set_color(self, hex_color):
        self.current_color = hex_to_rgb(hex_color)
    
    def set_size(self, size):
        self.current_size = size
    
    def undo(self):
        return self.canvas.undo()
    
    def redo(self):
        return self.canvas.redo()
    
    def clear(self):
        self.canvas.clear()
    
    def export_png(self):
        return self.canvas.export_image()