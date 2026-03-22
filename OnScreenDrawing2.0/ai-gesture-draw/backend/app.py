from flask import Flask, render_template, Response, jsonify
import cv2
import time
import os
import sys

# Ensure we can import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hand_tracking import HandTracker
from drawing_utils import DrawingSystem, COLOR_NAMES

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Global objects
tracker = None
drawer = None
camera = None
current_fps = 0
prev_time = 0

def get_camera():
    global camera
    if camera is None:
        print("Attempting to open camera with cv2.CAP_DSHOW...")
        # cv2.CAP_DSHOW is safer on Windows
        camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        
        if not camera.isOpened():
             print("Failed to open camera with CAP_DSHOW. Trying default...")
             camera = cv2.VideoCapture(1)
             
        if not camera.isOpened():
             print("CRITICAL: Camera failed to open on all backends.")
        else:
             print("Camera opened successfully.")
             
        # Set resolution for performance
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return camera

def init_systems():
    global tracker, drawer
    if tracker is None:
        try:
            tracker = HandTracker()
            print("Hand Tracker Initialized")
        except Exception as e:
            print(f"Error initializing tracker: {e}")
            tracker = None
            
    if drawer is None:
        drawer = DrawingSystem(width=1280, height=720)
        print("Drawing System Initialized")

def generate_frames():
    global camera, tracker, drawer, current_fps
    
    # Error frame generator helper
    def yield_error_frame(text):
        import numpy as np
        err_img = np.zeros((720, 1280, 3), dtype=np.uint8)
        # Fill with Blue to indicate error
        err_img[:] = (100, 0, 0) 
        cv2.putText(err_img, "SYSTEM ERROR", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 4)
        cv2.putText(err_img, str(text)[:50], (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        ret, buffer = cv2.imencode('.jpg', err_img)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    try:
        init_systems()
        cap = get_camera()
        
        print("Starting video generation...")
        prev_time = time.time()
        while True:
            try:
                success, frame = cap.read()
                if not success:
                    print("Failed to read from camera.")
                    # Create red error frame
                    import numpy as np
                    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
                    frame[:] = (0, 0, 100) # Dark Red
                    cv2.putText(frame, "CAMERA FAIL", (50, 360), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 4)
                
                # Flip for mirror effect, easier for drawing
                if success:
                     frame = cv2.flip(frame, 1)
                
                timestamp = int(time.time() * 1000)

                # FPS calculation
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time) if prev_time > 0 else 30
                prev_time = curr_time
                current_fps = int(fps)

                # Process
                if tracker:
                    try:
                        result = tracker.process_frame(frame, timestamp)
                        # Draw/Update
                        start_draw = time.time()
                        final_frame, _ = drawer.update_with_landmarks(frame, result)
                    except Exception as e:
                        print(f"Tracking/Drawing Error: {e}")
                        final_frame = frame
                else:
                    final_frame = frame

                # Encode
                ret, buffer = cv2.imencode('.jpg', final_frame)
                if not ret:
                    continue
                frame_bytes = buffer.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            except Exception as inner_e:
                print(f"Loop Error: {inner_e}")
                # Don't break immediately, try to recover or show error
                time.sleep(1)
                
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"CRITICAL GENERATOR ERROR: {e}")
        yield from yield_error_frame(f"Crash: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/state')
def get_state():
    if drawer:
        # Map color tuple to name for easier UI?
        # drawer.get_active_color() returns BGR.
        c_idx = drawer.current_color_idx
        c_name = COLOR_NAMES[c_idx] if c_idx < len(COLOR_NAMES) else "Custom"
        
        return jsonify({
            "mode": drawer.mode,
            "gesture": drawer.current_gesture,
            "color": c_name,
            "size": drawer.brush_size,
            "paused": drawer.is_paused,
            "fps": current_fps
        })
    return jsonify({"error": "System not ready"})

if __name__ == '__main__':
    try:
        init_systems()
        app.run(debug=True, port=5000, threaded=True, use_reloader=False) 
        # use_reloader=False to prevent double initialization/camera lock issues
    except Exception as e:
        print(f"Crash: {e}")
    finally:
        if camera:
            camera.release()
