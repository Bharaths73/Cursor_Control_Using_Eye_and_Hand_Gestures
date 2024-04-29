import time

# Initialize face mesh model
def EyeCaptureMovement(cam,mp,pyautogui,cv2,last_click_time,face_mesh,screen_h,screen_w):
        
        _, frame = cam.read()
         
          #flip the input image frame horizontally
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)#converts the color space of the input image frame from BGR (Blue-Green-Red) to RGB (Red-Green-Blue)

        #process the frame with the face mesh model to perform facial landmark detection on the input rgb_frame
        output = face_mesh.process(rgb_frame)
        # print("output is ",output)

         
        #extracts the facial landmark points from the output variable
        landmark_points = output.multi_face_landmarks
        print("output is ",landmark_points)
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark# extracting the landmark coordinates of the first detected face from the landmark_points variable.

             #draws circles on the image (frame) at specific landmark points. 
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0)) 

                 #it calculates the screen coordinates (screen_x and screen_y) to move the mouse cursor to the specified screen coordinates.
                if id == 1:
                    screen_x = screen_w * landmark.x
                    screen_y = screen_h * landmark.y
                    pyautogui.moveTo(screen_x, screen_y)

            left = [landmarks[145], landmarks[159]]
        #right=[landmarks[145],landmarks[159]]

            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255)) 

            if (left[0].y - left[1].y) < 0.004:
                print("0.04 inside")
                current_time = time.time()
                time_since_last_click = current_time - last_click_time

                if time_since_last_click < 0.5:  
                    pyautogui.doubleClick()
                    print("double click")
             
                else:
                    pyautogui.click()
                    print("single click")

                last_click_time = current_time 

        else:
            error_message='No faces detected'
            cv2.putText(frame,error_message,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

        # cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow('Eye Controlled Mouse', frame)
        cv2.waitKey(1) 
         
#releasing camera
