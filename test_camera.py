import cv2

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if not ret:
    print("❌ Could not access camera")
else:
    cv2.imshow("Test Camera", frame)
    cv2.waitKey(0)  # press any key to close

cap.release()
cv2.destroyAllWindows()
