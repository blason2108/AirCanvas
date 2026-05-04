import numpy as np
import cv2

class DrawingCanvas:
    def __init__(self, width, height, undo_stack_size=50):
        self.width = width
        self.height = height
        self.undo_stack_size = undo_stack_size
        self.strokes = []
        self.redo_stack = []
        self.current_stroke = None
    
    def add_stroke(self, points, color, size, tool):
        self.strokes.append({
            'points': points,
            'color': color,
            'size': size,
            'tool': tool
        })
        self.redo_stack.clear()
    
    def add_point_to_current(self, point):
        if self.current_stroke:
            self.current_stroke['points'].append(point)
    
    def start_stroke(self, point, color, size, tool):
        self.current_stroke = {
            'points': [point],
            'color': color,
            'size': size,
            'tool': tool
        }
    
    def end_stroke(self):
        if self.current_stroke and len(self.current_stroke['points']) > 0:
            self.add_stroke(
                self.current_stroke['points'],
                self.current_stroke['color'],
                self.current_stroke['size'],
                self.current_stroke['tool']
            )
        self.current_stroke = None
    
    def undo(self):
        if self.strokes:
            stroke = self.strokes.pop()
            self.redo_stack.append(stroke)
            return True
        return False
    
    def redo(self):
        if self.redo_stack:
            stroke = self.redo_stack.pop()
            self.strokes.append(stroke)
            return True
        return False
    
    def clear(self):
        self.strokes.clear()
        self.redo_stack.clear()
    
    def render(self, background=None):
        if background is None:
            canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        else:
            canvas = background.copy()
        
        for stroke in self.strokes:
            self._draw_stroke(canvas, stroke)
        
        if self.current_stroke:
            self._draw_stroke(canvas, self.current_stroke)
        
        return canvas
    
    def _draw_stroke(self, canvas, stroke):
        points = stroke['points']
        color = stroke['color']
        size = stroke['size']
        tool = stroke['tool']

        if not points:
            return

        if tool == 'spray':
            for point in points:
                self._draw_spray(canvas, point, color, size)
            return

        # Eraser paints with background color (black canvas).
        if tool == 'eraser':
            color = (0, 0, 0)

        if tool == 'line':
            if len(points) >= 2:
                cv2.line(canvas, points[0], points[-1], color, size)
            return

        if tool == 'rectangle':
            if len(points) >= 2:
                cv2.rectangle(canvas, points[0], points[-1], color, size)
            return

        if tool == 'circle':
            if len(points) >= 2:
                start = np.array(points[0], dtype=np.int32)
                end = np.array(points[-1], dtype=np.int32)
                radius = int(np.linalg.norm(end - start))
                if radius > 0:
                    cv2.circle(canvas, tuple(start), radius, color, size)
            return

        # Default: pen/freehand polyline.
        if len(points) < 2:
            cv2.circle(canvas, points[0], max(1, size // 2), color, -1)
            return

        for i in range(len(points) - 1):
            cv2.line(canvas, points[i], points[i + 1], color, size)
    
    def _draw_spray(self, canvas, center, color, size):
        import random
        for _ in range(size * 10):
            x = center[0] + random.randint(-size * 2, size * 2)
            y = center[1] + random.randint(-size * 2, size * 2)
            if 0 <= x < self.width and 0 <= y < self.height:
                canvas[y, x] = color
    
    def export_image(self):
        return self.render()
