\# 🎓 SmartLectureControl

\### AI-Powered Gesture-Controlled Presentation System with Face Recognition



An AI-powered classroom presentation system that enables authorized faculty members to control presentation slides using hand gestures. The system combines Face Recognition and Hand Gesture Recognition to provide a secure and touch-free presentation experience.



\---



\## 📌 Project Overview



SmartLectureControl is designed to improve classroom teaching by allowing faculty members to control PowerPoint presentations without using a keyboard or mouse.



The system authenticates the faculty using Face Recognition. Once authorized, the faculty can navigate through presentation slides using simple hand gestures. Unauthorized users cannot control the presentation, making the system secure and suitable for classrooms.



\---



\## ✨ Features



\- 👤 Face Recognition based Faculty Authentication

\- ✋ Gesture-Based Slide Navigation

\- ➡️ Next Slide Gesture

\- ⬅️ Previous Slide Gesture

\- 🔒 Unauthorized User Detection

\- 🖥️ Simple GUI Interface

\- 📂 Faculty Registration Module

\- 💾 Encoded Face Database



\---



\## 🛠️ Technologies Used



| Technology | Purpose |

|------------|---------|

| Python | Programming Language |

| OpenCV | Image Processing |

| MediaPipe | Hand Detection |

| face\_recognition | Face Recognition |

| dlib | Facial Landmark Detection |

| Tkinter | GUI Development |

| PyAutoGUI | Keyboard Automation |

| NumPy | Numerical Operations |



\---



\## 📁 Project Structure



```

SmartLectureControl/

│

├── faculty\_db/

│   ├── encodings.pkl

│   ├── navya.jpg

│   └── pranathi.jpg

│

├── models/

│

├── add\_faculty.py

├── face\_login.py

├── gui.py

├── secure\_gesture\_control.py

├── secure\_gesture\_control\_db.py

├── test\_camera.py

├── voice.py

├── requirements.txt

├── .gitignore

└── README.md

```



\---



\## ⚙️ Installation



\### Clone Repository



```bash

git clone https://github.com/YOUR\_USERNAME/SmartLectureControl.git

```



Move into the project folder.



```bash

cd SmartLectureControl

```



Create a Conda Environment.



```bash

conda create -n pptctrl python=3.10 -y

conda activate pptctrl

```



Install dependencies.



```bash

pip install -r requirements.txt

```



\---



\## ▶️ Run the Project



Run the GUI.



```bash

python gui.py

```



or



```bash

python secure\_gesture\_control\_db.py

```



\---



\## 🔄 Workflow



1\. Start the application.

2\. Register faculty images.

3\. Generate facial encodings.

4\. Authenticate the faculty.

5\. Detect hand gestures.

6\. Navigate presentation slides.

7\. Prevent unauthorized access.



\---



\## 📸 Screenshots



Add screenshots of:



\- GUI

\- Face Authentication

\- Authorized User

\- Unauthorized User

\- Next Slide Gesture

\- Previous Slide Gesture



\---



\## 🚀 Future Enhancements



\- Voice Command Support

\- Laser Pointer Simulation

\- Digital Whiteboard

\- Attendance Management

\- Cloud Database Integration

\- Multi-Faculty Support

\- AI-based Gesture Personalization



\---



\## 👩‍💻 Team Members



\- B. Navya

\- Ch. Pranathi

\- Y. Manvitha



Department of Information Technology



Vignan's Foundation for Science, Technology and Research



\---



\## 📄 License



This project is developed for academic purposes.

