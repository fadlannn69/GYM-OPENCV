import cv2 as cv
import mediapipe as mp
import model as ml
import numpy as np
from playsound import playsound as ps
import hand as hnd 


cam = cv.VideoCapture(0)
detect = ml.Detector() # import class model
detecta = hnd.Detector()

x = 0
y = 0
trigger = False
last_x = -2 # deteksi hitugan terakhir
pose_change = False # logika pengganti program dari hand ke pose

th_id = [4,8,12,16,20] # mediapipe untuk jari

while True:
        try:
            _,img = cam.read()
            if pose_change:
                img = detect.findpose(img)
                markList = detect.findPosition_pose(img, False)
                if len(markList) != 0:
                    kanan = detect.angle(img,12,14,16)
                    kiri = detect.angle(img,11,13,15) # menambahkan poin pada pipe
                    # hitung berapa banyak gerakan
                    posisi = np.interp(kanan,(90,160),(0,100)) # mengukur jarak (range) gerakan
                    bar = np.interp(kanan,(100,160),(100,400)) # membuat bar 
                    if posisi == 100 and not trigger:
                        if y  == 0:
                            x += 1
                            trigger = True
                            y = 1
                    elif posisi == 0 and trigger:
                        if y == 1:
                            trigger = False
                            y = 0
                    # suara penghitung gerakan
                    if  x != last_x:
                        last_x = x
                        x_int = str(last_x)
                        print(x_int)
                        hitung = {
                                    "1" : "satu.mp3",
                                    "2" : "dua.mp3",
                                    "3" : "tiga.mp3",
                                    "4" : "opat.mp3",
                                    "5" : "lima.mp3",
                                    "6" : "enam.mp3",
                                    "7" : "ania.mp3",
                                    "8" : "delapan.mp3",
                                    "9" : "sembilan.mp3",
                                    "10" : "sepuluh.mp3",
                                    "11" : "sebelas.mp3",
                                    "12" : "duabelas.mp3",
                                    "13" : "three.mp3",
                                    "14" : "forbelas.mp3",
                                    "15" : "pivbelas.mp3",
                                    "16" : "enamibelas.mp3",
                                    "17" : "seven.mp3",
                                    "18" : "delapanbelas.mp3",
                                    "19" : "nine.mp3",
                                    "20" : "duapuluh.mp3",
                                }

                        def suara (angka):
                            if angka in hitung:
                                file = hitung[angka]
                                ps(rf"/path/to/{file}")
                            else:
                                print("angka tidak ditemukan")
                        suara(x_int)
                        if x_int == "10": # jika sampai ke hitungan 10 maka program berakhir
                            ps(rf"/path/to/push_selesai.mp3")
                            ps(rf"/path/to/olga_selesai.mp3")
                            ps(rf"/path/to/penutup.mp3")
                            break
                    cv.rectangle(img,(100,80),(30,50),(255,0,0),2) # rectangle untuk bar
                    cv.rectangle(img,(100,int(bar)),(30,50),(255,0,0),cv.FILLED)
                    cv.putText(img,f"{int(posisi)} %" , (20,50),cv.FONT_HERSHEY_PLAIN,2,(0,255,0),4) 
    
            else:
                        # program untuk mendeteksi jari
                        img = detecta.findHands(img)
                        lmList = detecta.findPosition_hand(img)
                        if len(lmList) != 0 :
                            jari = []
                            # jari
                            if lmList[th_id[0]][1] > lmList[th_id[0] - 1][1]:
                                jari.append(1)
                            else:
                                jari.append(0)
                            for i in range(1,5):
                                if lmList[th_id[i]][2] < lmList[th_id[i]-2][2]:
                                    jari.append(1)
                                else:
                                    jari.append(0)
                            hasil = jari.count(1)
                            print(hasil)
                            if hasil == 5 :
                                ps(r"/path/to/perkenalan.mp3")
                                ps(r"/path/to/jenis_olahraga.mp3")
                            if hasil == 2:
                                ps(r"/path/to/laku_push.mp3")
                                ps(r"/path/to/bra_rep.mp3")
                            if hasil == 1:
                                ps(r"/path/to/se_rep.mp3")  
                                pose_change = True
            cv.imshow("psychoo", img)
            if cv.waitKey(1) & 0xFF == ord("q"):
                break
        except Exception as e:
            print(f"Error: {e}")

cam.release()
cv.destroyAllWindows()