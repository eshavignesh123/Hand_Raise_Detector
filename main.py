

import mediapipe as mp
import cv2

cap = cv2.VideoCapture(0)

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

print(mp_pose)

with mp_pose.Pose(static_image_mode=False) as pose:

    while(1):
        
        ret, frame = cap.read()
        ret, frame2 = cap.read()
        result = pose.process(frame)

        
        
        tmp = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

        
        
        red_dot = mp_draw.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=1)
        
        big_red_dot = mp_draw.DrawingSpec(color=(0,0,255), thickness=10, circle_radius=1)

            
        with mp_hands.Hands(static_image_mode=False) as hands:
            result1 = hands.process(frame)
            
        
    
        font = cv2.FONT_HERSHEY_SIMPLEX 

        # org 
        org = (50,50) 
        
        # fontScale 
        fontScale = 1
        
        # Red color in BGR 
        color = (0, 0, 255) 
        
        # Line thickness of 2 px 
        thickness = 2
        

        mp_draw.draw_landmarks(frame, landmark_list = result.pose_landmarks, connections=mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=red_dot)
        
        if result1.multi_hand_landmarks:
            for hand_landmarks in result1.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame2, hand_landmarks, connections=mp_hands.HAND_CONNECTIONS, landmark_drawing_spec=big_red_dot)

        if result.pose_landmarks:

            if (result.pose_landmarks.landmark[16].visibility>0.8 and result.pose_landmarks.landmark[16].y<result.pose_landmarks.landmark[0].y) or (result.pose_landmarks.landmark[15].visibility>0.8 and result.pose_landmarks.landmark[15].y<result.pose_landmarks.landmark[0].y):
                
            
                frame = cv2.putText(frame, "Hand is raised", org, font, fontScale, color, thickness, cv2.LINE_AA, False) 
                if result1.multi_hand_landmarks:
                    org2 = (200, 50)
                    count = 0
                    if result1.multi_hand_landmarks[0].landmark[8].y < result1.multi_hand_landmarks[0].landmark[7].y:
                        count+=1
                    if result1.multi_hand_landmarks[0].landmark[12].y < result1.multi_hand_landmarks[0].landmark[11].y:
                        count+=1
                    if result1.multi_hand_landmarks[0].landmark[16].y < result1.multi_hand_landmarks[0].landmark[15].y:
                        count+=1
                    if result1.multi_hand_landmarks[0].landmark[20].y < result1.multi_hand_landmarks[0].landmark[9].y:
                        count=0
                    if result1.multi_hand_landmarks[0].landmark[4].y < result1.multi_hand_landmarks[0].landmark[9].y:
                        count=0
                    
                    if count ==3:              
                        frame2 = cv2.putText(frame2, "Tribute Volunteer", org2, font, fontScale, color, thickness, cv2.LINE_AA, False)

        cv2.imshow("landmarks", frame)
        cv2.imshow("frame", frame2)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        
        
    cap.release()
    cv2.destroyAllWindows()