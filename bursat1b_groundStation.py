from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
import numpy as np
import cv2
from PyQt5.QtMultimediaWidgets import QVideoWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        cap = None
        out = None
        
        MainWindow.resize(1610, 883)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(80, 110, 921, 501))
        self.groupBox.setObjectName("grafikBox")

        self.graphicsView = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView.setGeometry(QtCore.QRect(30, 30, 281, 211))
        self.graphicsView.setObjectName("yukseklikGrafik")

        self.graphicsView_2 = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView_2.setGeometry(QtCore.QRect(330, 30, 281, 211))
        self.graphicsView_2.setObjectName("sicaklikGrafik")
        
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView_3.setGeometry(QtCore.QRect(630, 30, 281, 211))
        self.graphicsView_3.setObjectName("basincGrafik")

        self.graphicsView_4 = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView_4.setGeometry(QtCore.QRect(30, 280, 281, 211))
        self.graphicsView_4.setObjectName("inisHiziGrafik")

        self.graphicsView_5 = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView_5.setGeometry(QtCore.QRect(330, 280, 281, 211))
        self.graphicsView_5.setObjectName("pilGerilimiGrafik")

        self.graphicsView_6 = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView_6.setGeometry(QtCore.QRect(630, 280, 281, 211))
        self.graphicsView_6.setObjectName("gpsAltitudeGrafik")

        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(110, 10, 91, 16))
        self.label.setObjectName("yukseklikLabel")

        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(420, 10, 81, 16))
        self.label_2.setObjectName("sicaklikLabel")

        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(720, 10, 71, 16))
        self.label_3.setObjectName("basincLabel")

        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(120, 260, 81, 20))
        self.label_4.setObjectName("inisHiziLabel")

        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(420, 260, 81, 16))
        self.label_5.setObjectName("pilGerilimiLabel")

        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(710, 260, 101, 16))
        self.label_6.setObjectName("gpsAltitudeLabel")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1170, 10, 91, 16))
        self.label_7.setObjectName("anlikGoruntuLabel")

        self.graphicsView_8 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_8.setGeometry(QtCore.QRect(1170, 290, 311, 221))
        self.graphicsView_8.setObjectName("gyroGrafik")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1170, 270, 55, 16))
        self.label_8.setObjectName("gyroLabel")

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(30, 30, 111, 31))
        self.label_9.setObjectName("takimNoLabel")

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(240, 10, 191, 71))
        self.groupBox_2.setObjectName("ayrilmaKomutuBox")

        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(50, 30, 93, 28))
        self.pushButton.setObjectName("ayirButton")

        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(440, 10, 171, 71))
        self.groupBox_3.setObjectName("manuelTahrikKomutuBox")

        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 20, 71, 41))
        self.pushButton_2.setObjectName("baslaButton")

        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_3.setGeometry(QtCore.QRect(90, 20, 71, 41))
        self.pushButton_3.setObjectName("durButton")

        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(630, 10, 200, 81))
        self.groupBox_4.setObjectName("videoAktarimiBox")

        self.toolButton = QtWidgets.QToolButton(self.groupBox_4)
        self.toolButton.setGeometry(QtCore.QRect(140, 20, 45, 22))
        self.toolButton.setObjectName("dosyaSecButton")

        self.label_10 = QtWidgets.QLabel(self.groupBox_4)
        self.label_10.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.label_10.setObjectName("dosyaSecLabel")

        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_4.setGeometry(QtCore.QRect(50, 50, 81, 21))
        self.pushButton_4.setObjectName("gonderButton")

        self.graphicsView_9 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_9.setGeometry(QtCore.QRect(1170, 540, 311, 221))
        self.graphicsView_9.setObjectName("lokasyonGrafik")

        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(1170, 520, 55, 16))
        self.label_11.setObjectName("lokasyonLabel")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(80, 630, 921, 201))
        self.tableWidget.setObjectName("listViewPanel")

        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(1050, 120, 20, 461))
        self.progressBar.setProperty("value", 26)
        self.progressBar.setOrientation(QtCore.Qt.Vertical)
        self.progressBar.setObjectName("progressBar")

        self.video = QtWidgets.QLabel(self.centralwidget)
        self.video.setGeometry(QtCore.QRect(1170, 30, 311, 221))
        self.video.setText("")
        self.video.setObjectName("anlikGoruntu")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1610, 26))
        self.menubar.setObjectName("menubar")

        self.menuGrafikler = QtWidgets.QMenu(self.menubar)
        self.menuGrafikler.setObjectName("menuGrafikler")

        self.menuTelemetri_Verileri = QtWidgets.QMenu(self.menubar)
        self.menuTelemetri_Verileri.setObjectName("menuTelemetri_Verileri")

        self.menuHarita = QtWidgets.QMenu(self.menubar)
        self.menuHarita.setObjectName("menuHarita")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)
        self.menuTelemetri_Verileri.addSeparator()
        self.menubar.addAction(self.menuGrafikler.menuAction())
        self.menubar.addAction(self.menuTelemetri_Verileri.menuAction())
        self.menubar.addAction(self.menuHarita.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Grafikler"))
        self.label.setText(_translate("MainWindow", "Yükseklik (m)"))
        self.label_2.setText(_translate("MainWindow", "Sıcaklık (°C)"))
        self.label_3.setText(_translate("MainWindow", "Basınç (Pa)"))
        self.label_4.setText(_translate("MainWindow", "İniş Hızı (m/s)"))
        self.label_5.setText(_translate("MainWindow", "Pil Gerilimi (V)"))
        self.label_6.setText(_translate("MainWindow", "GPS Altitude (m)"))
        self.label_7.setText(_translate("MainWindow", "Anlık Görüntü"))
        self.label_8.setText(_translate("MainWindow", "Gyro"))
        self.label_9.setText(_translate("MainWindow", "Takım No: 39374"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Ayrılma Komutu"))
        self.pushButton.setText(_translate("MainWindow", "Ayır"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Manuel Tahrik Komutu"))
        self.pushButton_2.setText(_translate("MainWindow", "Başla"))
        self.pushButton_3.setText(_translate("MainWindow", "Dur"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Video Aktarımı"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.label_10.setText(_translate("MainWindow", "Dosya Seç:"))
        self.pushButton_4.setText(_translate("MainWindow", "Gönder"))
        self.label_11.setText(_translate("MainWindow", "Lokasyon"))
        self.menuGrafikler.setTitle(_translate("MainWindow", "Grafikler"))
        self.menuTelemetri_Verileri.setTitle(_translate("MainWindow", "Telemetri Verileri"))
        self.menuHarita.setTitle(_translate("MainWindow", "Harita"))
        self.tmp = None
        self.pushButton_2.clicked.connect(self.realTimeVideo)
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.setBackground)

#WebCam anlık gösterimi (Kamera geldiğinde ona göre güncellecek)
    def realTimeVideo(self):
        self.cap = cv2.VideoCapture(0)

        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        self.out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

        while (self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret == True:
                
                frame = cv2.flip(frame, 180)
                self.out.write(frame)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame,(311,221))
               
                image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
                self.video.setPixmap(QtGui.QPixmap.fromImage(image))
        
                if cv2.waitKey(1) and 0xFF == ord('q'):
                    break
            else:
                break
        
        cv2.destroyAllWindows()

    def close(self):
        self.cap.release()
        self.out.release()
    
    def setBackground(self):
        self.video.setText("                           Video Sonu")
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    




        
	