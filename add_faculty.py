import cv2
import face_recognition
import os
import pickle
from tkinter import Tk, filedialog, messagebox

# ---------------- PATHS ----------------
BASE_DIR = "faculty_db"
IMG_DIR = os.path.join(BASE_DIR, "images")
ENC_FILE = os.path.join(BASE_DIR, "encodings.pkl")

os.makedirs(IMG_DIR, exist_ok=True)

# ---------------- LOAD EXISTING DATABASE ----------------
if os.path.exists(ENC_FILE):
    with open(ENC_FILE, "rb") as f:
        database = pickle.load(f)
else:
    database = {}

# ---------------- FILE PICKER ----------------
Tk().withdraw()
image_path = filedialog.askopenfilename(
    title="Select Faculty Photo",
    filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
)

if not image_path:
    messagebox.showinfo("Cancelled", "No image selected.")
    exit()

# ---------------- PROCESS IMAGE ----------------
image = face_recognition.load_image_file(image_path)
face_locations = face_recognition.face_locations(image)
encodings = face_recognition.face_encodings(image, face_locations)

if len(encodings) == 0:
    messagebox.showerror("Error", "No face detected in image.")
    exit()

encoding = encodings[0]

# ---------------- ASK NAME ----------------
faculty_name = os.path.splitext(os.path.basename(image_path))[0]

# ---------------- SAVE IMAGE ----------------
save_path = os.path.join(IMG_DIR, faculty_name + ".jpg")
cv2.imwrite(save_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

# ---------------- SAVE ENCODING ----------------
database[faculty_name] = encoding

with open(ENC_FILE, "wb") as f:
    pickle.dump(database, f)

messagebox.showinfo(
    "Success",
    f"Faculty '{faculty_name}' added successfully!"
)
