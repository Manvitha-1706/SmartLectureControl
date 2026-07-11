import face_recognition
import face_recognition_models
print("Working")

import cv2
import face_recognition
import mediapipe as mp
import pyautogui
import time
import os

# =========================
# GLOBAL VARIABLES
# =========================

running = True
screen_width, screen_height = pyautogui.size()

drawing = False
last_action_time = 0
ACTION_DELAY = 1.2

# =========================
# STOP SYSTEM FUNCTION
# =========================

def stop_system():
    global running
    running = False
    print("System stopped safely")

# =========================
# LOAD FACULTY DATABASE
# =========================

FACULTY_DB_PATH = "faculty_db"
known_face_encodings = []

print("Loading faculty database...")

if not os.path.exists(FACULTY_DB_PATH):
    print("faculty_db folder not found")
    exit()

for file in os.listdir(FACULTY_DB_PATH):

    if file.endswith(".jpg") or file.endswith(".png"):

        path = os.path.join(FACULTY_DB_PATH, file)

        image = face_recognition.load_image_file(path)

        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_face_encodings.append(encodings[0])
            print("Loaded:", file)

print("Total authorized faculty:", len(known_face_encodings))

# =========================
# CAMERA SETUP
# =========================

camera = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

print("Smart Lecture Control Running...")

# =========================
# MAIN LOOP
# =========================

while running:

    ret, frame = camera.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # =========================
    # FACE AUTHENTICATION
    # =========================

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    authorized = False
    authorized_face_center = None

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        matches = face_recognition.compare_faces(
            known_face_encodings,
            face_encoding,
            tolerance=0.5
        )

        if True in matches:

            authorized = True

            cx = (left + right) // 2
            cy = (top + bottom) // 2

            authorized_face_center = (cx, cy)

            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            cv2.putText(frame,"AUTHORIZED",(left, top-10),
                        cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

        else:

            cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
            cv2.putText(frame,"UNAUTHORIZED",(left, top-10),
                        cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    # =========================
    # HAND GESTURE CONTROL
    # =========================

    if authorized:

        results = hands.process(rgb)

        if results.multi_hand_landmarks:

            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                current_time = time.time()

                index_tip = hand_landmarks.landmark[8]
                middle_tip = hand_landmarks.landmark[12]

                hand_x = int(index_tip.x * frame.shape[1])
                hand_y = int(index_tip.y * frame.shape[0])

                # =========================
                # HAND NEAR AUTHORIZED FACE CHECK
                # =========================

                if authorized_face_center is not None:

                    face_x, face_y = authorized_face_center

                    distance = ((hand_x - face_x)**2 + (hand_y - face_y)**2) ** 0.5

                    if distance > 250:
                        continue

                # =========================
                # SLIDE CONTROL
                # =========================

                if current_time - last_action_time > ACTION_DELAY:

                    hand_label = results.multi_handedness[idx].classification[0].label

                    if hand_label == "Left":
                        pyautogui.press("right")
                        last_action_time = current_time

                    elif hand_label == "Right":
                        pyautogui.press("left")
                        last_action_time = current_time

                # =========================
                # PPT DRAWING
                # =========================

                x = int(index_tip.x * screen_width)
                y = int(index_tip.y * screen_height)

                if index_tip.y < middle_tip.y:

                    pyautogui.moveTo(x, y)

                    if not drawing:
                        pyautogui.mouseDown()
                        drawing = True

                else:

                    if drawing:
                        pyautogui.mouseUp()
                        drawing = False

    else:

        if drawing:
            pyautogui.mouseUp()
            drawing = False

    cv2.imshow("Secure Smart Lecture Control", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        stop_system()

# =========================
# CLEANUP
# =========================

camera.release()
cv2.destroyAllWindows()
pyautogui.mouseUp()

print("System exited successfully")
