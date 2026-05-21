import face_recognition
import os
import pickle

known_face_encodings = []
known_face_names = []

folder_path = "Dataset"

print("Encoding faces...")

for filename in os.listdir(folder_path):

    if filename.lower().endswith((".jpg", ".png", ".jpeg")):

        path = os.path.join(folder_path, filename)

        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:

            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(filename)[0])

            print(f"Encoded: {filename}")

# save encodings
data = {
    "encodings": known_face_encodings,
    "names": known_face_names
}

with open("encodings.pkl", "wb") as f:
    pickle.dump(data, f)

print("Encodings saved successfully!")