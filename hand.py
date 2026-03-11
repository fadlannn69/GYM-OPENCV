import cv2 as cv
import mediapipe as mp


class Detector():
    def __init__(self,mode = False , maxHands = 2 , detectionCon = 0.5 , trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw = True):
        rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition_hand(self,img,handNo=0,draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id , lm in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x * w) , int(lm.y * h)
                lmList.append([id,cx,cy])
                if draw:
                    cv.circle(img,(cx,cy),2,(255,0,0),cv.FILLED)
        return lmList

# def main():
#     cam = cv.VideoCapture(0)
#     detect = Detector()
#     th_id = [4,8,12,16,20]
#     while True:
#         _,img = cam.read()
#         img = detect.findHands(img)
#         lmList = detect.findPosition_hand(img)
#         if len(lmList) != 0 :
#                 jari = []
#                 # jempol
#                 if lmList[th_id[0]][1] > lmList[th_id[0] - 1][1]:
#                     jari.append(1)
#                 else:
#                     jari.append(0)
#                 for i in range(1,5):
#                     if lmList[th_id[i]][2] < lmList[th_id[i]-2][2]:
#                         jari.append(1)
#                     else:
#                         jari.append(0)
#                 hasil = jari.count(1)
#                 print(hasil)
                

#         cv.imshow("psychoo",img)
#         if cv.waitKey(1) & 0xFF == ord("q"):
#             break
#     cam.release()
#     cv.destroyAllWindows()
# if __name__ == "__main__":
#     main()


    