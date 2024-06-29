import HandGesture as hand
import mediapipe as mp
import EyeGesture as eye
import HandTrackingModule as htm
import tkinter as tk
import pyautogui
import threading
import cv2
import sys


try:
    cam = cv2.VideoCapture(0)

    #checks if the camera is opened and if not generates error and code exits
    if not cam.isOpened():
        raise Exception("Could not open camera.")

except Exception as e:
    print(f"Error: {e}")
    exit()

screen_w, screen_h = pyautogui.size()



def enable_eye_control():
    hand_control_var.set(False)
    eye_control_var.set(True)
    last_click_time=0
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    
    def eye_control_loop():
        print("Eye control enabled")
        while eye_control_var.get():
            eye.EyeCaptureMovement(cam, mp, pyautogui, cv2, last_click_time, face_mesh, screen_h, screen_w)
        print("Eye control disabled")

    eye_thread = threading.Thread(target=eye_control_loop)
    eye_thread.start()

def enable_hand_control():
    eye_control_var.set(False)
    hand_control_var.set(True)

    try:
       detector = htm.handDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)
    except Exception as e:
        print(e)
        exit()
    pTime = 0
    cTime = 0

    def hand_control_loop():
        print("Hand control enabled")
        mpHands=mp.solutions.hands
        screen_w, screen_h = pyautogui.size()
        hands=mpHands.Hands(min_detection_confidence=0.7,min_tracking_confidence=0.7)
        mpDraw=mp.solutions.drawing_utils
        mode = ''
        active = 0

        print("hey")
        try:
            while hand_control_var.get():
                hand.HandTracker(cam,pTime,cTime,detector,active,mode)
            print("Hand control disabled")

        except Exception as e:
             print(e)
             exit()

    hand_thread = threading.Thread(target=hand_control_loop)
    hand_thread.start()

def exit_application():
    # Stop eye control thread if running
    if 'eye_thread' in globals() and eye_thread.is_alive():
        eye_control_var.set(False)
        eye_thread.join()  # Wait for eye_thread to finish
    
    # Stop hand control thread if running
    if 'hand_thread' in globals() and hand_thread.is_alive():
        hand_control_var.set(False)
        hand_thread.join()  # Wait for hand_thread to finish
    
    root.destroy()  # Close the Tkinter window
    sys.exit(0) 

# Create the main window
root = tk.Tk()
root.title("Gesture Control Options")
# try:
#     print(root.tk.call('info', 'patchlevel'))
# except Exception as e:
#     print(e)


# Variables to track the control modes
eye_control_var = tk.BooleanVar()
hand_control_var = tk.BooleanVar()

# Create buttons to enable eye and hand control
eye_control_button = tk.Radiobutton(root, text="Enable Eye Control", variable=eye_control_var, value=True, command=enable_eye_control)

hand_control_button = tk.Radiobutton(root, text="Enable Hand Control", variable=hand_control_var, value=True, command=enable_hand_control)

spacer_frame = tk.Frame(root, height=15) 

exit_button = tk.Button(root, text="Exit", command=exit_application, bg="red", fg="white", font=("Arial", 12, "bold"), relief="raised")

spacer_frame1 = tk.Frame(root, height=15) 


# Place the buttons in the window
eye_control_button.pack()
hand_control_button.pack()
spacer_frame.pack()
exit_button.pack()
spacer_frame1.pack()

# Start the main event loop
root.mainloop()
