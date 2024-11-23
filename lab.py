import cv2

overlay = cv2.imread("logo.png")  # Make sure the path is correct
cap = cv2.VideoCapture(0)         # Change to 1 or 2 if 0 doesn't work

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Error: Could not read frame from webcam.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
            x, y, w, h = cv2.boundingRect(approx)
            resized_overlay = cv2.resize(overlay, (w, h))
            frame[y:y+h, x:x+w] = resized_overlay

    cv2.imshow("Basic AR", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()