# Air Canvas

Real-time hand-tracking drawing application where users draw on a virtual canvas using finger gestures.

## Features

- **Hand Tracking** - Uses MediaPipe for 21-landmark hand detection
- **Gesture Drawing** - Draw with your index finger in the air
- **Tool Toggle** - Two-finger gesture switches between pen and eraser
- **Drawing Tools**: Pen, Eraser, Line, Circle, Rectangle, Spray
- **Web Dashboard** - Control panel with tool selection, color picker, brush size, undo/redo, and export

## Tech Stack

- **Backend**: Python Flask + Flask-SocketIO
- **Computer Vision**: OpenCV + MediaPipe Hands
- **Frontend**: HTML/CSS/JavaScript with SocketIO

## Requirements

```
opencv-python==4.8.1.78
mediapipe==0.10.9
flask==3.0.0
flask-socketio==5.3.6
numpy==1.24.3
eventlet==0.34.2
```

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python app.py
```

Open http://localhost:5050 in your browser.

## Usage

1. Allow camera access when prompted
2. Hold up your **index finger** to draw - the tip is tracked as your cursor
3. Make a **"peace sign"** (two fingers) to toggle between pen and eraser
4. Use the **web dashboard** to:
   - Select drawing tools
   - Pick colors
   - Adjust brush size (1-50px)
   - Undo/Redo strokes
   - Clear canvas
   - Export as PNG

## Project Structure

```
SimpleProj/
├── app.py                  # Flask app & SocketIO handlers
├── config.py               # Configuration settings
├── requirements.txt        # Dependencies
├── drawing/
│   ├── canvas.py          # Drawing engine & stroke management
│   └── tools.py           # Color conversion utilities
├── tracking/
│   ├── hand_tracker.py    # MediaPipe hand detection
│   └── gesture_classifier.py  # Gesture recognition
├── streaming/
│   └── video_stream.py    # Camera stream & frame processing
├── templates/
│   └── index.html         # Web dashboard
└── static/
    ├── css/style.css
    └── js/app.js
```

## Configuration

Edit `config.py` to adjust:
- Video resolution (default: 640x480)
- FPS (default: 20)
- Brush size range (default: 1-50)
- Undo stack size (default: 50)
