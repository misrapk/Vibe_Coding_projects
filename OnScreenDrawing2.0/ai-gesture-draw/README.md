# AI Gesture Draw 🎨

A futuristic, AI-powered web application that turns your webcam into a magical canvas. Draw in the air with hand gestures!

## 🚀 Features

- **Real-time Drawing**: Use your index finger to draw.
- **Gesture Control**:
  - ☝️ + ✊ **Draw**: Raising Index Finger (Hand A) + Making a Fist (Hand B).
  - 🖐️🖐️ **Clear**: Open both hands.
  - ✌️ **Color**: Show "Peace" sign (Index + Middle) to cycle colors.
  - 🤏 **Brush Size**: Pinch Thumb + Index to adjust size based on distance.
  - ✊ **Move**: Move a single closed fist to drag the canvas.
  - ✊✊ **Pause**: Hold two fists to freeze drawing.
- **Glassmorphism UI**: Modern, clean, dark-themed interface.
- **Performance**: Powered by MediaPipe and OpenCV with optimized Flask streaming.

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.9+
- Webcam

### Installation

1. **Clone/Navigate to the project**:
   ```bash
   cd ai-gesture-draw
   ```

2. **Backend Setup**:
   Navigate to the backend folder:
   ```bash
   cd backend
   ```

   Create virtual environment:
   ```bash
   python -m venv venv
   ```

   Activate virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

   Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   *Note: Validated with MediaPipe 0.10.14*

3. **Model Download**:
   The `hand_landmarker.task` model should already be in `backend/models/`. If not, download it from Google MediaPipe Task guide.

## 🏃 Running the App

1. Ensure the virtual environment is active.
2. Run the Flask app:
   ```bash
   python app.py
   ```
3. Open your browser and go to:
   **http://127.0.0.1:5000**

## 🎮 How to Use

1. **Allow Camera Access** when prompted.
2. **Stand back** slightly so the camera sees your hands clearly.
3. Check the **Side Panel** (?) for a quick gesture guide.
4. **Start Drawing**: Raise your right index finger ☝️ and close your left hand into a fist ✊.
5. Have fun!

## 📁 Project Structure

```
ai-gesture-draw/
├── backend/            # Python Flask & AI Logic
│   ├── app.py          # Main application entry
│   ├── hand_tracking.py# MediaPipe integration
│   ├── drawing_utils.py# Canvas & Gesture logic
│   └── models/         # AI Models
├── frontend/           # Web Interface
│   ├── templates/      # HTML
│   └── static/         # CSS & JS
└── README.md
```
