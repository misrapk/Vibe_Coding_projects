import mediapipe as mp
import numpy as np
import os

class HandTracker:
    def __init__(self, model_path='models/hand_landmarker.task'):
        self.result = None
        
        # Verify model exists
        if not os.path.exists(model_path):
             # Try absolute path fallback if relative doesn't work
             abs_path = os.path.join(os.getcwd(), 'ai-gesture-draw', 'backend', 'models', 'hand_landmarker.task')
             if os.path.exists(abs_path):
                 model_path = abs_path
             else:
                 # Last ditch: check if we are already in backend
                 abs_path_2 = os.path.join(os.getcwd(), 'models', 'hand_landmarker.task')
                 if os.path.exists(abs_path_2):
                     model_path = abs_path_2
                 else:
                     raise FileNotFoundError(f"Could not find model at {model_path} or fallbacks")

        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        # Create a landmarker instance with the video mode:
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.landmarker = HandLandmarker.create_from_options(options)

    def process_frame(self, frame_bgr, timestamp_ms):
        # Convert openCV BGR to RGB MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_bgr) # MediaPipe expects RGB or SRGB? Actually it expects RGB for mp.Image usually but let's double check. 
        # mp.Image docs: "The data in the numpy array must be in RGB format."
        # So we MUST convert BGR to RGB before creating mp.Image
        
        frame_rgb = frame_bgr[:, :, ::-1].copy() # BGR to RGB
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        
        # Detect asynchronously not needed for this flow? WE will use process_video (sync) or process_async.
        # process_video returns the result synchronously (for batch processing) but for live streaming usually we might want async? 
        # Actually the documented way for VIDEO mode is `detect_for_video` (in python solutions, but this is TASKS).
        # In Tasks API: method is `landmarker.detect_for_video(mp_image, timestamp_ms)`
        
        result = self.landmarker.detect_for_video(mp_image, timestamp_ms)
        return result
