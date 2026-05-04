from flask import Flask, render_template, Response, jsonify, send_file
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'air-canvas-secret'
# Use standard threading mode to avoid eventlet + debug reloader bind races.
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

video_stream = None

def get_video_stream():
    global video_stream
    if video_stream is None:
        try:
            from streaming.video_stream import VideoStream
            video_stream = VideoStream()
            video_stream.start()
        except Exception as e:
            print(f"Warning: Camera not available: {e}")
            video_stream = None
    return video_stream

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    vs = get_video_stream()
    if vs is None:
        return
    while True:
        frame = vs.get_jpeg_frame()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    vs = get_video_stream()
    if vs is None:
        return "Camera not available", 503
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('set_tool')
def handle_set_tool(data):
    allowed_tools = {'pen', 'eraser', 'line', 'circle', 'rectangle', 'spray'}
    tool = (data or {}).get('tool')
    if tool not in allowed_tools:
        emit('action_response', {'action': 'set_tool', 'success': False})
        return
    vs = get_video_stream()
    if vs:
        vs.set_tool(tool)
    emit('action_response', {'action': 'set_tool', 'success': True})

@socketio.on('set_color')
def handle_set_color(data):
    color = (data or {}).get('color')
    if not isinstance(color, str) or not color.startswith('#') or len(color) != 7:
        emit('action_response', {'action': 'set_color', 'success': False})
        return
    vs = get_video_stream()
    if vs:
        vs.set_color(color)
    emit('action_response', {'action': 'set_color', 'success': True})

@socketio.on('set_size')
def handle_set_size(data):
    try:
        size = int((data or {}).get('size'))
    except (TypeError, ValueError):
        emit('action_response', {'action': 'set_size', 'success': False})
        return
    size = max(1, min(50, size))
    vs = get_video_stream()
    if vs:
        vs.set_size(size)
    emit('action_response', {'action': 'set_size', 'success': True})

@socketio.on('undo')
def handle_undo():
    vs = get_video_stream()
    result = vs.undo() if vs else False
    emit('action_response', {'action': 'undo', 'success': result})

@socketio.on('redo')
def handle_redo():
    vs = get_video_stream()
    result = vs.redo() if vs else False
    emit('action_response', {'action': 'redo', 'success': result})

@socketio.on('clear')
def handle_clear():
    vs = get_video_stream()
    if vs:
        vs.clear()
    emit('action_response', {'action': 'clear', 'success': True})

@app.route('/export')
def export():
    vs = get_video_stream()
    if vs is None:
        return "No drawing to export", 400
    img = vs.export_png()
    _, encoded = cv2.imencode('.png', img)
    return send_file(BytesIO(encoded.tobytes()), 
                     mimetype='image/png',
                     as_attachment=True,
                     download_name='drawing.png')

if __name__ == '__main__':
    port = 5050
    print(f"Starting Air Canvas on http://localhost:{port}")
    socketio.run(
        app,
        debug=True,
        use_reloader=False,
        allow_unsafe_werkzeug=True,
        host='0.0.0.0',
        port=port
    )
