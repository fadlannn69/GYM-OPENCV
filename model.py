import cv2 as cv
import mediapipe as mp
import math

class Detector:
    def __init__(self, mode=False, upBody=False, smooth=True, detectCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectCon = detectCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        model_complexity = 0 if self.upBody else 1  # 0 untuk tubuh atas, 1 untuk tubuh penuh
        
        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode, 
            model_complexity=model_complexity,  # Menggunakan model_complexity untuk deteksi tubuh bagian atas
            smooth_landmarks=self.smooth, 
            min_detection_confidence=self.detectCon, 
            min_tracking_confidence=self.trackCon
        )

    def findpose(self, img, draw=True):
        rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.hasil = self.pose.process(rgb)
        if self.hasil.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.hasil.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition_pose(self, img, handNo=0, draw=True):
        self.markList = []
        if self.hasil.pose_landmarks:
            for id, lm in enumerate(self.hasil.pose_landmarks.landmark): 
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.markList.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 2, (255, 0, 0), cv.FILLED)
        return self.markList
    
    def angle(self,img,p1,p2,p3 , draw = True):
        x1,y1 = self.markList[p1][1:]
        x2,y2 = self.markList[p2][1:]
        x3,y3 = self.markList[p3][1:]
       

        # angle
        sudut = math.degrees(math.atan2(y3-y2 , x3-x2) - math.atan2(y1-y2,x1-x2))
        if sudut < 0:
            sudut += 360
 
        if draw:
            cv.line(img,(x1,y1),(x2,y2),(255,255,255),3)
            cv.line(img,(x3,y3),(x2,y2),(255,255,255),3)
            cv.circle(img, (x1, y1), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x1, y1), 15, (255, 0, 0),2)
            cv.circle(img, (x2, y2), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x2, y2), 15, (255, 0, 0),2)
            cv.circle(img, (x3, y3), 10, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x3, y3), 15, (255, 0, 0), 2)
            cv.putText(img,str(int(sudut)),(x2-50, y2+50),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        return sudut
# def main():
#     cam = cv.VideoCapture(0)
#     detect = Detector()
#     while True:
#         try:
#             _, img = cam.read()
#             img = detect.findpose(img)
#             lmList = detect.findPosition(img, draw=False)
#             if len(lmList) != 0:
#                 print(lmList[14])  # Print data for a specific landmark (for example, landmark 14)
#                 cv.circle(img, (lmList[14][1], lmList[14][2]), 15, (255, 0, 0), cv.FILLED)

#             cv.imshow("psychoo", img)
#             if cv.waitKey(1) & 0xFF == ord("q"):
#                 break
#         except Exception as e:
#             print(f"Error: {e}")

#     cv.destroyAllWindows()

# if __name__ == "__main__":
#     main()
