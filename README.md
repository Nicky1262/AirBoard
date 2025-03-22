### **AirBoard Application** 🎨✋

#### **Project Description:**
This project is a **virtual painting application** that uses **hand gesture recognition** to allow users to draw on a digital canvas without a physical brush or stylus. It utilizes **OpenCV**, **MediaPipe**, and **NumPy** to detect hand movements through a webcam and map them to drawing actions on the screen.

---

### **Key Features:**
✅ **Hand Tracking with MediaPipe**:  
- The application detects a single hand using **MediaPipe Hands** and tracks the movement of the **index finger**.

✅ **Gesture-Based Drawing**:  
- The **index finger** is used as a brush, and movements are mapped to strokes on the canvas.  
- The **thumb and index finger pinch** gesture creates a **new stroke**, preventing unintentional lines.

✅ **Color Selection**:  
- The user can switch between different colors (Blue, Green, Red, Yellow) by hovering over the respective color buttons.

✅ **Clear Canvas Feature**:  
- Hovering over the "CLEAR" button resets the entire drawing.

✅ **Real-Time Video Processing**:  
- The live webcam feed displays the user’s hand movements, the drawing interface, and the painted strokes.

✅ **Frame Flipping for Natural Interaction**:  
- The video feed is flipped horizontally to ensure intuitive drawing, mimicking a mirror effect.

---

### **How It Works:**
1. **Launch the Application**: The webcam starts capturing video.
2. **Detect Hand & Landmarks**: MediaPipe identifies the hand and marks key landmarks.
3. **Track the Forefinger**:  
   - If the **forefinger moves**, it draws on the canvas.  
   - If the **thumb is close to the forefinger**, a new stroke is started.
4. **Switch Colors & Clear Canvas**: Hovering over UI buttons changes colors or clears the drawing.
5. **Exit**: Press **'q'** to close the application.

---

### **Technologies Used:**
- **Python** 🐍  
- **OpenCV** (for image processing) 📷  
- **MediaPipe** (for hand tracking) ✋  
- **NumPy** (for matrix operations) 🔢  

---

### **Potential Enhancements:**
🚀 Add an **eraser tool** to remove parts of the drawing.  
🎨 Implement **more colors and brush sizes**.  
🖌️ Add **gesture-based undo/redo functionality**.  
📂 Save the drawing as an image file.  

---

This project is a fun and interactive way to explore **computer vision, hand tracking, and OpenCV**, creating a real-time virtual painting tool! 🎨✨
