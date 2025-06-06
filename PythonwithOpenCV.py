# import cv2
# import tkinter as tk
# from PIL import Image, ImageTk
# import cvzone
# from cvzone.HandTrackingModule import HandDetector

# root = tk.Tk()
# root.title("Webcam Preview with Hand Landmark Detection")

# video_label = tk.Label(root)
# video_label.pack()

# exit_button = tk.Button(root, text="Exit", command=root.destroy)
# exit_button.pack(pady=10)
# exit_button.config(font=("Arial", 12))

# cap = cv2.VideoCapture(0) 

# # Check if webcam is opened correctly
# if not cap.isOpened():
#     print("Error: Could not access the webcam.")
#     exit()

# detector = HandDetector()

# def update_frame():
#     ret, frame = cap.read() 
#     if ret:        
#         frame = cv2.flip(frame, 1)
#         hands, frame = detector.findHands(frame)
#         if hands:
#             hand = hands[0] 
#             landmarks = hand['lmList']

#             for lm in landmarks:
#                 x, y = lm[0], lm[1]
#                 cv2.circle(frame, (x, y), 5, (0, 255, 0), cv2.FILLED)

#         frame = cv2.resize(frame, (700, 500))
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         img = Image.fromarray(frame)
#         imgtk = ImageTk.PhotoImage(image=img)

#         video_label.imgtk = imgtk
#         video_label.configure(image=imgtk)
#     video_label.after(10, update_frame)

# update_frame()
# root.mainloop()

# cap.release()
# cv2.destroyAllWindows()



# import cv2
# import tkinter as tk
# from PIL import Image, ImageTk
# from cvzone.HandTrackingModule import HandDetector

# # Initialize main window
# root = tk.Tk()
# root.title("Hand Landmark & Gesture Detection")

# # Video display label
# video_label = tk.Label(root)
# video_label.pack()

# # Exit button
# exit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=root.destroy)
# exit_button.pack(pady=10)

# # Webcam capture
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Error: Could not access the webcam.")
#     root.destroy()

# # Hand detector
# detector = HandDetector()

# # Gesture detection functions
# def is_thumb_up(lm):
#     # Check if the thumb tip is significantly above the thumb base
#     thumb_extended = lm[4][1] < lm[2][1] - 15  # Adjust -15 as needed

#     # Check if the thumb is generally pointing upwards (y-coordinate lower than wrist)
#     thumb_upward = lm[4][1] < lm[0][1] - 10  # Adjust -10 as needed

#     # Check if other fingers are generally curled down (their tips are above their PIP joints)
#     fingers_curled = all(lm[i][1] > lm[i - 2][1] + 10 for i in [8, 12, 16, 20]) # Adjust +10 as needed

#     return thumb_extended and thumb_upward and fingers_curled

# def is_peace_sign(lm):
#     return lm[8][1] < lm[6][1] and lm[12][1] < lm[10][1] and \
#             lm[16][1] > lm[14][1] and lm[20][1] > lm[18][1]

# def is_fist(lm, hand_info):  # Accept hand_info as an argument
#     fingers_curled = all(lm[i][1] > lm[i - 2][1] + 8 for i in [8, 12, 16, 20])
#     thumb_curled = lm[4][1] > lm[2][1] - 5
#     thumb_across = lm[4][0] > min(lm[5][0], lm[17][0]) and lm[4][0] < max(lm[5][0], lm[17][0])
#     if hand_info['type'] == "Left":  # Use hand_info
#         thumb_across = lm[4][0] < max(lm[5][0], lm[17][0]) and lm[4][0] > min(lm[5][0], lm[17][0])
#     return fingers_curled and (thumb_curled or thumb_across)

# def is_ok_sign(lm):
#     thumb_index_close = abs(lm[4][0] - lm[8][0]) < 30 and abs(lm[4][1] - lm[8][1]) < 30
#     other_fingers_up = all(lm[i][1] < lm[i - 2][1] for i in [12, 16, 20])
#     return thumb_index_close and other_fingers_up

# def is_open_palm(lm, hand_type="Right"):
#     fingers_extended = all(lm[tip][1] < lm[tip - 2][1] for tip in [8, 12, 16, 20])
#     if hand_type == "Right":
#         thumb_extended = lm[4][0] > lm[3][0]
#     else:
#         thumb_extended = lm[4][0] < lm[3][0]
#     return fingers_extended and thumb_extended

# def is_yo_sign(lm, hand_type="Right"):
#     # Check if index finger is extended
#     index_extended = lm[8][1] < lm[6][1] - 10  # Tip above PIP (adjust -10)

#     # Check if pinky finger is extended
#     pinky_extended = lm[20][1] < lm[18][1] - 10  # Tip above PIP (adjust -10)

#     # Check if middle and ring fingers are curled
#     middle_curled = lm[12][1] > lm[10][1] + 5  # Tip below PIP (adjust +5)
#     ring_curled = lm[16][1] > lm[14][1] + 5    # Tip below PIP (adjust +5)

#     # Optional: Check thumb position (can be extended or slightly curled)
#     if hand_type == "Right":
#         thumb_extended = lm[4][0] > lm[2][0] - 10 # Thumb to the right of base (adjust -10)
#     else:  # Left hand
#         thumb_extended = lm[4][0] < lm[2][0] + 10 # Thumb to the left of base (adjust +10)
#     thumb_slightly_curled = lm[4][1] > lm[2][1] - 5 # Thumb tip slightly below base (adjust -5)

#     return index_extended and pinky_extended and middle_curled and ring_curled and (thumb_extended or thumb_slightly_curled)

# # Update video frame
# def update_frame():
#     ret, frame = cap.read()
#     if ret:
#         frame = cv2.flip(frame, 1)
#         hands, frame = detector.findHands(frame)

#         if hands:
#             hand = hands[0]
#             lm = hand['lmList']
#             hand_type = hand['type']

#             # Draw landmarks
#             for point in lm:
#                 cv2.circle(frame, (point[0], point[1]), 5, (0, 255, 0), cv2.FILLED)

#             # Gesture detection (order matters!)
#             gesture = ""
#             if is_yo_sign(lm, hand_type):
#                 gesture = "Yo"
#             elif is_thumb_up(lm):
#                 gesture = "Thumbs Up"
#             elif is_fist(lm,hand):
#                 gesture = "Fist"
#             elif is_peace_sign(lm):
#                 gesture = "Peace"
#             elif is_ok_sign(lm):
#                 gesture = "OK"
#             elif is_open_palm(lm, hand_type):
#                 gesture = "Open Palm"

#             if gesture:
#                 cv2.putText(frame, gesture, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
#                             1.2, (255, 0, 255), 3)
#             else:
#                 cv2.putText(frame, "Can't Detect", (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
#                             1.2, (0, 0, 255), 3)

#         # Display frame in tkinter
#         frame = cv2.resize(frame, (700, 500))
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         imgtk = ImageTk.PhotoImage(Image.fromarray(frame))
#         video_label.imgtk = imgtk
#         video_label.configure(image=imgtk)

#     video_label.after(10, update_frame)

# # Handle closing properly
# def on_close():
#     cap.release()
#     cv2.destroyAllWindows()
#     root.destroy()

# root.protocol("WM_DELETE_WINDOW", on_close)
# update_frame()
# root.mainloop()
# cap.release()
# cv2.destroyAllWindows()


# import cv2
# import tkinter as tk
# from PIL import Image, ImageTk
# from cvzone.HandTrackingModule import HandDetector

# # Initialize main window
# root = tk.Tk()
# root.title("Finger Counting using Hand Landmarks")

# # Video display label
# video_label = tk.Label(root)
# video_label.pack()

# # Exit button
# exit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=root.destroy)
# exit_button.pack(pady=10)

# # Webcam capture
# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Error: Could not access the webcam.")
#     root.destroy()

# # Hand detector (track multiple hands)
# detector = HandDetector(maxHands=2, detectionCon=0.8, minTrackCon=0.5)

# def count_fingers(hand):
#     fingers = []
#     # Thumb (special case: depends on hand orientation)
#     if hand['type'] == "Right":
#         if hand['lmList'][4][0] > hand['lmList'][3][0]:
#             fingers.append(1)
#         else:
#             fingers.append(0)
#     else:  # Left hand
#         if hand['lmList'][4][0] < hand['lmList'][3][0]:
#             fingers.append(1)
#         else:
#             fingers.append(0)

#     # Other 4 fingers
#     for id in range(8, 21, 4):
#         if hand['lmList'][id][1] < hand['lmList'][id - 2][1]:
#             fingers.append(1)
#         else:
#             fingers.append(0)

#     return sum(fingers)

# # Update video frame
# def update_frame():
#     ret, frame = cap.read()
#     if ret:
#         frame = cv2.flip(frame, 1)
#         hands, frame = detector.findHands(frame, draw=True)  # Draw landmarks and connections

#         total_fingers = 0
#         if hands:
#             for hand in hands:
#                 fingers_count = count_fingers(hand)
#                 total_fingers += fingers_count
#                 h, w, c = frame.shape
#                 cx, cy = hand['center']
#                 cv2.putText(frame,"", (cx - 50, cy + 50), cv2.FONT_HERSHEY_PLAIN,
#                             4, (255, 0, 255), 4)

#             cv2.putText(frame, f"Total Fingers: {total_fingers}", (10, 70), cv2.FONT_HERSHEY_PLAIN,
#                         3, (255, 0, 255), 3)
#         else:
#             cv2.putText(frame, "No Hands Detected", (10, 70), cv2.FONT_HERSHEY_PLAIN,
#                         3, (0, 0, 255), 3)

#         # Display frame in tkinter
#         frame = cv2.resize(frame, (700, 500))
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         imgtk = ImageTk.PhotoImage(Image.fromarray(frame))
#         video_label.imgtk = imgtk
#         video_label.configure(image=imgtk)

#     video_label.after(10, update_frame)

# # Handle closing properly
# def on_close():
#     cap.release()
#     cv2.destroyAllWindows()
#     root.destroy()

# root.protocol("WM_DELETE_WINDOW", on_close)
# update_frame()
# root.mainloop()
# cap.release()
# cv2.destroyAllWindows()



import cv2
import tkinter as tk
from PIL import Image, ImageTk
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc

# Tkinter setup
root = tk.Tk()
root.title("Gesture Volume & Brightness Control")

video_label = tk.Label(root)
video_label.pack()
tk.Button(root, text="Exit", command=root.destroy).pack(pady=10)

# Webcam
cap = cv2.VideoCapture(0)

# Hand detector
detector = HandDetector(maxHands=2, detectionCon=0.8, minTrackCon=0.5)

# Volume setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minVol, maxVol = volume.GetVolumeRange()[0:2]

def update_frame():
    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.flip(frame, 1)
    hands, _ = detector.findHands(frame, draw=False)

    if hands:
        for hand in hands:
            lmList = hand['lmList']
            handType = hand['type']
            thumb_tip, index_tip = lmList[4], lmList[8]

            cv2.circle(frame, thumb_tip[:2], 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(frame, index_tip[:2], 10, (0, 255, 0), cv2.FILLED)
            cv2.line(frame, thumb_tip[:2], index_tip[:2], (0, 255, 0), 3)

            distance = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])

            if handType == "Left":
                vol = np.interp(distance, [20, 200], [minVol, maxVol])
                volume.SetMasterVolumeLevel(vol, None)
                vol_display = int(np.interp(distance, [20, 200], [0, 100]))
                cv2.putText(frame, f"Volume: {vol_display}%", (10, 60),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

            elif handType == "Right":
                bright = int(np.interp(distance, [20, 200], [10, 100]))
                sbc.set_brightness(bright)
                cv2.putText(frame, f"Brightness: {bright}%", (10, 90),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
    else:
        cv2.putText(frame, "No Hands Detected", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    frame = cv2.resize(frame, (700, 500))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgtk = ImageTk.PhotoImage(Image.fromarray(frame))
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    video_label.after(10, update_frame)

def on_close():
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
update_frame()
root.mainloop()