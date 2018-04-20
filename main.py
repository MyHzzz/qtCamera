import sys
import cv2
import datetime
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap


from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Pencerem(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('tasarim.ui',self)
        self.image=None
        self.startButton.clicked.connect(self.start_webcam)
        self.stopButton.clicked.connect(self.stop_webcam)
        self.btnTest.clicked.connect(self.test_et)
        self.sayac=0
        self.btnTest.setEnabled(False)
        #self.txtKayitAdi.setText('Kayıt Adı')

    def test_et(self):
        print (self.boxSure.value())

    def start_webcam(self):
        self.capture=cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

       #kamera için writer oluşturur ve hazır bekler, renkli kayıt için sondaki false true olmalı
        frame_width = int(self.capture.get(3))
        frame_height = int(self.capture.get(4))
        self.out = cv2.VideoWriter(self.txtKayitAdi.text()+'.avi', cv2.VideoWriter_fourcc(*'XVID'), 8, (frame_width, frame_height),False)
        self.zaman=datetime.datetime.now()

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)

    def update_frame(self):
        ret,self.image=self.capture.read()
        self.image=cv2.flip(self.image,1)


        self.image=cv2.cvtColor(self.image,cv2.COLOR_RGB2GRAY)
        #self.image=cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY)

        #writer ile avi dosyasına yazar.
        self.out.write(self.image)
        diff=datetime.datetime.now()- self.zaman

        #if (diff.seconds>93):
        if (diff.seconds > self.boxSure.value()):
           # print (diff.seconds)
            self.stop_webcam()
        print(diff.seconds)


        self.displayImage(self.image,1)


    def stop_webcam(self):
        self.timer.stop()
        self.out.release()

    def displayImage(self,img,window=1):
        #print (len(img.shape))
        qformat=QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        outImage=outImage.rgbSwapped()

        if window==1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)


app=QApplication(sys.argv)
window=Pencerem()
window.setWindowTitle('Hakan')
window.show()
app.exec_()
