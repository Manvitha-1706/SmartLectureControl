import face_recognition
import cv2
import subprocess

# Load registered face
known_image = face_recognition.load_image_file("navya.jpg")
known_encodings = face_recognition.face_encodings(known_image)

if not known_encodings:
    print("❌ No face found in navya.jpg. Please use a clearer image.")
    exit()

known_encoding = known_encodings[0]

# Start webcam
cap = cv2.VideoCapture(0)
access_granted = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)

    print(f"Detected {len(face_locations)} face(s)")

    if face_locations:
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            if face_encoding is not None:
                match = face_recognition.compare_faces([known_encoding], face_encoding)[0]
                if match:
                    print("✅ Access Granted")
                    access_granted = True
                    break

    cv2.imshow("Face Login", frame)
    if access_granted or cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Launch gesture control if access granted
if access_granted:
    subprocess.run(["python", "gesture_slide_control.py"])
