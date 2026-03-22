import cv2
import numpy as np
import math

# Colors
COLORS = [
    (255, 255, 255), # White
    (0, 0, 255),     # Red (BGR) -> No, OpenCV uses BGR, but we usually want nice colors. 
    (0, 255, 0),     # Green
    (255, 0, 0),     # Blue
    (0, 255, 255)    # Yellow
]
# BGR Definitions for OpenCV
COLORS_BGR = [
    (255, 255, 255), # White
    (0, 0, 255),     # Red
    (0, 255, 0),     # Green
    (255, 0, 0),     # Blue
    (0, 255, 255)    # Yellow
]
COLOR_NAMES = ["White", "Red", "Green", "Blue", "Yellow"]

class DrawingSystem:
    def __init__(self, width=1280, height=720):
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.ui_canvas = np.zeros((height, width, 3), dtype=np.uint8) # For ephemeral UI
        
        self.current_color_idx = 0
        self.brush_size = 10
        self.is_drawing = False
        self.is_paused = False
        self.last_point = None
        
        # Debounce/State
        self.mode = "NEUTRAL" # DRAW, ERASE, MOVE, PAUSE, NEUTRAL
        
        # Gesture Debouncing
        self.current_gesture = "NONE"
        self.gesture_history = []
        self.HISTORY_LEN = 5
        
    def get_active_color(self):
        return COLORS_BGR[self.current_color_idx]

    def clear(self):
        self.canvas[:] = 0

    def cycle_color(self):
        self.current_color_idx = (self.current_color_idx + 1) % len(COLORS)

    def change_size(self, delta):
        self.brush_size = max(2, min(50, self.brush_size + delta))

    def move_canvas(self, dx, dy):
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        self.canvas = cv2.warpAffine(self.canvas, M, (self.canvas.shape[1], self.canvas.shape[0]))

    def update_with_landmarks(self, frame, detection_result):
        if self.is_paused:
            # Only check for Unpause gesture
            pass

        height, width, _ = frame.shape
        self.ui_canvas[:] = 0 # Clear UI layer
        
        if not detection_result or not detection_result.hand_landmarks:
            self.last_point = None
            self.mode = "NEUTRAL"
            self.current_gesture = "NONE"
            return cv2.addWeighted(frame, 1, self.canvas, 1, 0), {
                "mode": self.mode,
                "color": self.get_active_color(),
                "size": self.brush_size,
                "gesture": self.current_gesture
            }
        
        # Logic to extract hand data
        hands = []
        for i, landmarks in enumerate(detection_result.hand_landmarks):
            handedness = detection_result.handedness[i][0].category_name # "Left" or "Right"
            # Normalize landmarks
            points = [(int(lm.x * width), int(lm.y * height)) for lm in landmarks]
            hands.append({'index': i, 'type': handedness, 'points': points})

        # --- GESTURE RECOGNITION ---
        detected_gesture = self.recognize_gesture(hands)
        self.current_gesture = detected_gesture # Simple for now, can add debouncing later if flickery
        
        # --- EXECUTE ACTIONS ---
        
        # Drawing Cursor (always show cursor on index tip of drawing hand if visible)
        # Find index finger tip
        index_tip = None
        for hand in hands:
             # Just grab the first hand's index tip for visualization or logic
             # In DRAW mode, we need the "Pointing" hand.
             pass

        status_text = f"Mode: {self.mode}"

        if detected_gesture == "DRAW":
            self.mode = "DRAW"
            # Find the pointing hand (Hand A)
            drawing_hand = self.get_drawing_hand(hands)
            if drawing_hand:
                idx_x, idx_y = drawing_hand['points'][8] # Index TIP
                
                # Smoother drawing?
                if self.last_point:
                    cv2.line(self.canvas, self.last_point, (idx_x, idx_y), self.get_active_color(), self.brush_size)
                
                self.last_point = (idx_x, idx_y)
                cv2.circle(frame, (idx_x, idx_y), self.brush_size // 2, self.get_active_color(), -1)
            else:
                 self.last_point = None

        elif detected_gesture == "CLEAR":
            self.clear()
            self.mode = "CLEAR"
            self.last_point = None
            status_text = "CLEARED!"

        elif detected_gesture == "COLOR":
            # Debounce color change? Needs to be "Triggered" once, not continuous
            # For now, simple continuous cycling might be too fast. 
            # We'll rely on "State Entry" or a slower rate.
            # Let's just create a cooldown or only do it on frame 1 of gesture?
            # Creating a simple counter for demo purposes:
            self.cycle_color() # This will be CHAOS at 30fps.
            # Only cycle if previous wasn't COLOR
            self.mode = "COLOR"
            self.last_point = None
            
        elif detected_gesture == "SIZE":
            # Find pinch distance
            dist = self.get_pinch_distance(hands)
            # Map distance to change? 
            # Or just "If gesture is size, increment/decrement"? 
            # Prompt: "Thumb + index pinch... Distance based control... Action: Increase/decrease stroke"
            # So, strictly map distance to size.
            target_size = int(max(2, min(50, dist / 2))) # rough heuristic
            self.brush_size = target_size
            self.mode = "SIZE"
            self.last_point = None
            
        elif detected_gesture == "MOVE":
            self.mode = "MOVE"
            # Track fist movement
            fist_hand = self.get_fist_hand(hands)
            if fist_hand:
                # Delta from last point?
                curr_pos = fist_hand['points'][0] # Wrist or center?
                # Complex to implement drag without state. Use wrist.
                if self.last_point:
                   dx = curr_pos[0] - self.last_point[0]
                   dy = curr_pos[1] - self.last_point[1]
                   self.move_canvas(dx, dy)
                self.last_point = curr_pos
            
        elif detected_gesture == "PAUSE":
             self.is_paused = not self.is_paused # Toggle? 
             # Prompt: "Gesture: Both Fists. Action: Freeze drawing state. Resume when gesture changes."
             # This implies "While Holding Fists -> Paused".
             self.mode = "PAUSED"
             self.last_point = None
        
        else:
            self.last_point = None
            self.mode = "NEUTRAL"

        # Fix Color Cycling Chaos:
        # We need a proper state machine for "Trigger" gestures vs "Hold" gestures.
        # But for this V1, let's just make it reasonably checking previous state.
        
        # Compositing
        result = cv2.addWeighted(frame, 1, self.canvas, 1, 0)
        
        # Draw UI Indicators on the frame (Text/HUD)
        # cv2.putText(result, f"FPS: --  Size: {self.brush_size}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

        
        # Return frame and current state info
        return result, {
            "mode": self.mode,
            "color": self.get_active_color(),
            "size": self.brush_size,
            "gesture": detected_gesture
        }

    # --- HELPERS ---
    def recognize_gesture(self, hands):
        # returns "DRAW", "CLEAR", "COLOR", "SIZE", "MOVE", "PAUSE", "NONE"
        if len(hands) == 0: return "NONE"
        
        # Analyze logical states of fingers for all hands
        hand_states = []
        for hand in hands:
            hand_states.append(self.get_finger_state(hand['points']))
            
        # PAUSE: Two fists
        # State: All fingers closed [0,0,0,0,0] (Thumb, Index, Middle, Ring, Pinky)
        fists = sum(1 for s in hand_states if self.is_fist(s))
        if fists == 2:
            return "PAUSE"
            
        # CLEAR: Both hands open
        opens = sum(1 for s in hand_states if self.is_open_palm(s))
        if opens == 2:
            return "CLEAR"
            
        # DRAW: Hand A Index, Hand B Fist. (1 Index, 1 Fist)
        # Check if we have one index-only and one fist
        has_index_only = any(self.is_index_pointing(s) for s in hand_states)
        has_fist = any(self.is_fist(s) for s in hand_states)
        if has_index_only and has_fist:
            return "DRAW"
            
        # COLOR: Index + Middle (V sign)
        # Any hand showing V
        if any(self.is_v_sign(s) for s in hand_states):
            return "COLOR"
            
        # SIZE: Thumb + Index pinch 
        # (This is tricky with just finger states, need distance check)
        # Assume "Pinch" gesture usually has other fingers open or closed? 
        # Let's check for "Two fingers" or specific pinch geometry.
        # Prompt: "Thumb + index pinch".
        if any(self.is_pinching(h['points']) for h in hands):
            return "SIZE"
            
        # MOVE: One closed fist (Only one fist detected, and total hands == 1 maybe? Or just dominant?)
        # "Gesture: One closed fist"
        if len(hands) == 1 and self.is_fist(hand_states[0]):
            return "MOVE"
            
        return "NONE"

    def get_finger_state(self, landmarks):
        # Returns list of 5 booleans (True=Open, False=Closed)
        # Thumb, Index, Middle, Ring, Pinky
        # Simple heuristic: y of tip < y of pip/mcp? 
        # Note: (0,0) is top-left. So Up means Lower Y.
        
        # wrist is 0
        wrist = landmarks[0]
        
        state = []
        # Thumb: Check x distance for separate mechanism or just use tip vs ip? 
        # Thumb is tricky. Use MCP vs Tip X/Y? 
        # Simple method: Check if Tip is "far" from Index MCP? 
        # Let's use standard: Tip distance from wrist > IP distance from wrist.
        # Vector geometry is better.
        
        tips = [4, 8, 12, 16, 20]
        pips = [3, 7, 11, 15, 19] # Using PIP or MCP for comparison
        mcps = [2, 5, 9, 13, 17]
        
        # Fingers 1-4 (Index to Pinky)
        # If Tip Y < PIP Y (for Upright hand). 
        # We need to handle Rotation? Assume upright for now.
        
        # Thumb (0):
        # Compare tip X to MCP X? Left/Right hand matters.
        # Distance from pinky mcp? 
        # Robust way: Tip to Wrist Distance > IP to Wrist Distance?
        
        def dist(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])
        
        # Thumb
        state.append(dist(landmarks[4], wrist) > dist(landmarks[3], wrist) + 20) # Margin
        
        # Others
        for i in range(1, 5):
            # Open if Tip is further from wrist than PIP? 
            # Or Tip Y < PIP Y? 
            # Vector dot product is best but lets stick to simpler dist logic which works for fists.
            
            # If Tip-Wrist > PIP-Wrist (Finger is likely extended)
            # Actually, when making a fist, Tip is CLOSE to wrist/MCP. 
            state.append(dist(landmarks[tips[i]], wrist) > dist(landmarks[pips[i]], wrist))
            
        return state

    def is_fist(self, state):
        # 0 or 1 finger open? Usually purely 0 open.
        return sum(state) == 0 or (sum(state) == 1 and state[0]) # Allow thumb to be whatever
        
    def is_open_palm(self, state):
        return sum(state) == 5

    def is_index_pointing(self, state):
        # Index Open, others closed. Thumb optional? 
        # "ONLY index finger raised"
        return state[1] and not state[2] and not state[3] and not state[4]
        
    def is_v_sign(self, state):
        # Index + Middle Open
        return state[1] and state[2] and not state[3] and not state[4]

    def is_pinching(self, landmarks):
        # Thumb tip (4) close to Index tip (8)
        d = math.hypot(landmarks[4][0] - landmarks[8][0], landmarks[4][1] - landmarks[8][1])
        return d < 40 # Threshold
        
    def get_drawing_hand(self, hands):
        # Return the hand that is pointing
        for hand in hands:
            if self.is_index_pointing(self.get_finger_state(hand['points'])):
                return hand
        return None

    def get_fist_hand(self, hands):
        for hand in hands:
             if self.is_fist(self.get_finger_state(hand['points'])):
                 return hand
        return None

    def get_pinch_distance(self, hands):
        # Find the hand pinching
        for hand in hands:
            if self.is_pinching(hand['points']):
                 return math.hypot(hand['points'][4][0] - hand['points'][8][0], hand['points'][4][1] - hand['points'][8][1])
        return 0

