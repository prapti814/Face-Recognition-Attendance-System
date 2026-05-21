import cv2
import face_recognition
import numpy as np
import pandas as pd
import os
import pickle

def run_camera(selected_subject, hours, update_callback=None):

    attendance_file = f"attendance_{selected_subject}.csv"
    total_file = f"total_{selected_subject}.txt"

    # ---------------- TOTAL CLASSES ----------------
    if not os.path.exists(total_file):
        with open(total_file, "w") as f:
            f.write("0")

    with open(total_file, "r") as f:
        total_classes = int(f.read())

    total_classes += int(hours)

    with open(total_file, "w") as f:
        f.write(str(total_classes))

    # ---------------- LOAD ENCODINGS ----------------
    with open("encodings.pkl", "rb") as f:
        data = pickle.load(f)

    known_face_encodings = data["encodings"]
    known_face_names = data["names"]

    # ---------------- LOAD CSV ----------------
    df = pd.read_csv(attendance_file)

    marked_attendance = []

    # ---------------- CAMERA ----------------
    video_capture = cv2.VideoCapture(0)
    cv2.namedWindow("Smart Attendance System", cv2.WINDOW_AUTOSIZE)
    cv2.setWindowProperty("Smart Attendance System", cv2.WND_PROP_TOPMOST, 1)

    # reduce lag
    process_this_frame = True

    while True:

        ret, frame = video_capture.read()

        if not ret:
            continue

        # mirror effect (feels natural)
        frame = cv2.flip(frame, 1)

        # resize for speed
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # process alternate frames
        if process_this_frame:

            face_locations = face_recognition.face_locations(
                rgb_small_frame,
                model="hog"
            )

            face_encodings = face_recognition.face_encodings(
                rgb_small_frame,
                face_locations
            )

        process_this_frame = not process_this_frame

        # ---------------- FACE MATCHING ----------------
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            # scale back face locations
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            name = ""

            distances = face_recognition.face_distance(
                known_face_encodings,
                face_encoding
            )

            best_match = np.argmin(distances)

            # less strict threshold
            if distances[best_match] < 0.60:
                name = known_face_names[best_match]

            # ---------------- ATTENDANCE ----------------
            if name != "":

                if name not in marked_attendance:

                    if name in df["Name"].values:
                        
                        df.loc[df["Name"] == name, "Attended"] += int(hours)

                        #df.loc[df["Name"] == name, "Percentage"] = (
                            #df.loc[df["Name"] == name, "Attended"] / total_classes
                        #) * 100
                        
                        #df.to_csv(attendance_file, index=False)

                        marked_attendance.append(name)

                        #if update_callback:
                            #update_callback(f"{name} marked ✅")

                #else:
                    #if update_callback:
                        #update_callback(f"{name} already marked ⚠️")

                # green rectangle only for recognized faces
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom),
                              (0, 255, 0), cv2.FILLED)

                cv2.putText(frame, name, (left + 6, bottom - 8),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (255, 255, 255), 2)
            df.loc[df["Name"] == name, "Percentage"] = (
                            df.loc[df["Name"] == name, "Attended"] / total_classes
                        ) * 100  
            df.to_csv(attendance_file, index=False)
      

        # ---------------- SHOW WINDOW ----------------
        cv2.imshow("Smart Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # ---------------- CLEANUP ----------------
    video_capture.release()
    cv2.destroyAllWindows()