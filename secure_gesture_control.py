import cv2
import face_recognition
import mediapipe as mp
import pyautogui
import time

# -------------------------
# INITIAL SETUP
# -------------------------
camera = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

authorized = False
registered_face_encoding = None

last_action_time = 0
ACTION_DELAY = 1.2  # seconds

print("📸 Please look at the camera to register your face...")

# -------------------------
# FACE REGISTRATION
# -------------------------
while registered_face_encoding is None:
    ret, frame = camera.read()
    if not ret:
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_encodings(rgb)

    if len(faces) > 0:
        registered_face_encoding = faces[0]
        print("✅ Face registered successfully!")
        break

    cv2.imshow("Register Face", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        camera.release()
        cv2.destroyAllWindows()
        exit()

cv2.destroyAllWindows()

# -------------------------
# MAIN LOOP
# -------------------------
print("🎥 Secure Smart Lecture Control Started")

while True:
    ret, frame = camera.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ---------- FACE AUTH ----------
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    authorized = False

    for face_encoding in face_encodings:
        match = face_recognition.compare_faces(
            [registered_face_encoding],
            face_encoding,
            tolerance=0.5
        )
        if match[0]:
            authorized = True
            break

    if authorized:
        cv2.putText(frame, "AUTHORIZED", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "NOT AUTHORIZED", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # ---------- HAND CONTROL ----------
    if authorized:
        hand_results = hands.process(rgb)

        if hand_results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):

                mp_draw.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                hand_label = hand_results.multi_handedness[idx].classification[0].label
                current_time = time.time()

                if current_time - last_action_time > ACTION_DELAY:

                    # 🔁 INVERTED MAPPING (IMPORTANT FIX)
                    if hand_label == "Left":       # USER'S RIGHT HAND
                        pyautogui.press("right")
                        last_action_time = current_time
                        cv2.putText(frame, "RIGHT HAND → NEXT SLIDE",
                                    (20, 90), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8, (255, 255, 0), 2)

                    elif hand_label == "Right":    # USER'S LEFT HAND
                        pyautogui.press("left")
                        last_action_time = current_time
                        cv2.putText(frame, "LEFT HAND → PREVIOUS SLIDE",
                                    (20, 90), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8, (255, 255, 0), 2)

    cv2.imshow("Smart Lecture Control (Secure)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Exiting...")
        break

camera.release()
cv2.destroyAllWindows()
