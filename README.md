# Automated Attendance System using Face Recognition

An intelligent, real-time classroom attendance system that leverages Deep Learning for facial biometric verification and features a modern desktop dashboard.

## Key Features
- **Deep Learning Core:** Uses a pre-trained ResNet-34 architecture to map facial features into a 128-dimensional embedding space.
- **Multithreaded Architecture:** Decouples the computational load of AI inference from the main UI thread using Python's `threading` module (as a Daemon Thread) to prevent GUI freezing.
- **Modern Dashboard:** Built using Tkinter with High-DPI scaling awareness and dynamic conditional formatting (highlighting low attendance <75%).
- **Data Persistence:** Managed via Pandas for real-time local updates without requiring application restarts.

##  Project Structure
- `app.py`: The main Tkinter Graphical User Interface (GUI).
- `camara.py`: Video streaming logic, face detection (HOG), and embedding matching.
- `encode_faces.py`: Script to pre-compute and save 128-D biometric vectors into a serialized format.

##  Technology Stack
- **Language:** Python
- **Libraries:** OpenCV, face_recognition (dlib), Tkinter, Pandas