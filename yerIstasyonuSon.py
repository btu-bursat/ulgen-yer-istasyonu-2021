from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL
from threading import Thread
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import *
import datetime as dt
import matplotlib as plt
import OpenGL.GL as gl
from OpenGL import GLU
from OpenGL.arrays import vbo
import numpy as np
from MplWidget import *
import matplotlib
import sys
import os
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView
import io
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QHeaderView
import cv2
import socket

takim_no = 0
paket_numarasi = 0
basinc = 0
yukseklik = 0
inis_hizi = 0
sicaklik = 0
pil_gerilimi = 0
gps_latitude = gps_longitude = gps_altitude = 0
uydu_statusu = 0
pitch = roll = yaw = 0
donus_sayisi = 0
video_aktarim_bilgisi = ""
video = ""
xs = []
ys = []
xs2 = []
ys2 = []
xs3 = []
ys3 = []
xs4 = []
ys4 = []
xs5 = []
ys5 = []
xs6 = []
ys6 = []
cap = None
out = None
paketSayisi = 0

host = "192.168.104.229" # burasi statik ip ile degisecek
port = 5003

yer_istasyonu_socket = socket.socket()
yer_istasyonu_socket.connect((host, port))

index = 0 

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 255))  # initialize the screen to blue
        gl.glEnable(gl.GL_DEPTH_TEST)  # enable depth testing

        self.initGeometry()

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix()  # push the current matrix to the current stack

        gl.glTranslate(0.0, 0.0, -50.0)  # third, translate cube to specified depth
        gl.glScale(20.0, 20.0, 20.0)  # second, scale cube
        gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
        gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
        gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)
        gl.glTranslate(-0.5, -0.5, -0.5)  # first, translate cube center to origin

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vertVBO)
        gl.glColorPointer(3, gl.GL_FLOAT, 0, self.colorVBO)

        gl.glDrawElements(gl.GL_QUADS, len(self.cubeIdxArray), gl.GL_UNSIGNED_INT, self.cubeIdxArray)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glPopMatrix()  # restore the previous modelview matrix

    def initGeometry(self):
        self.cubeVtxArray = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]])
        self.vertVBO = vbo.VBO(np.reshape(self.cubeVtxArray,
                                          (1, -1)).astype(np.float32))
        self.vertVBO.bind()

        self.cubeClrArray = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]])
        self.colorVBO = vbo.VBO(np.reshape(self.cubeClrArray,
                                           (1, -1)).astype(np.float32))
        self.colorVBO.bind()

        self.cubeIdxArray = np.array(
            [0, 1, 2, 3,
             3, 2, 6, 7,
             1, 0, 4, 5,
             2, 1, 5, 6,
             0, 3, 7, 4,
             7, 6, 5, 4])

    def setRotX(self, val):
        self.rotX = np.pi * val

    def setRotY(self, val):
        self.rotY = np.pi * val

    def setRotZ(self, val):
        self.rotZ = np.pi * val

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1020)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1080))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1242, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.grafikler = QtWidgets.QGroupBox(self.centralwidget)
        self.grafikler.setGeometry(QtCore.QRect(260, 90, 1151, 671))
        self.grafikler.setStyleSheet("")
        self.grafikler.setObjectName("grafikler")
        self.MplWidget = MplWidget(self.grafikler)
        self.MplWidget.setGeometry(QtCore.QRect(10, 40, 371, 300))
        self.MplWidget.setStyleSheet("background-color: white;")
        self.MplWidget.setObjectName("MplWidget")
        self.label = QtWidgets.QLabel(self.grafikler)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.grafikler)
        self.label_2.setGeometry(QtCore.QRect(390, 20, 81, 16))
        self.label_2.setObjectName("label_2")
        self.hizWidget = hizWidget(self.grafikler)
        self.hizWidget.setGeometry(QtCore.QRect(10, 360, 371, 300))
        self.hizWidget.setStyleSheet("background-color: white;")
        self.hizWidget.setObjectName("hizWidget")
        self.pilGerilimiWidget = pilGerilimiWidget(self.grafikler)
        self.pilGerilimiWidget.setGeometry(QtCore.QRect(390, 360, 371, 300))
        self.pilGerilimiWidget.setStyleSheet("background-color: white;")
        self.pilGerilimiWidget.setObjectName("pilGerilimiWidget")
        self.gpsAltitudeWidget = gpsAltitudeWidget(self.grafikler)
        self.gpsAltitudeWidget.setGeometry(QtCore.QRect(770, 360, 371, 300))
        self.gpsAltitudeWidget.setStyleSheet("background-color: white;")
        self.gpsAltitudeWidget.setObjectName("gpsAltitudeWidget")
        self.basincWidget = basincWidget(self.grafikler)
        self.basincWidget.setGeometry(QtCore.QRect(770, 40, 371, 320))
        self.basincWidget.setStyleSheet("background-color: white;")
        self.basincWidget.setObjectName("basincWidget")
        self.sicaklikWidget = sicaklikWidget(self.grafikler)
        self.sicaklikWidget.setGeometry(QtCore.QRect(390, 40, 371, 300))
        self.sicaklikWidget.setStyleSheet("background-color: white;")
        self.sicaklikWidget.setObjectName("sicaklikWidget")
        self.label_5 = QtWidgets.QLabel(self.grafikler)
        self.label_5.setGeometry(QtCore.QRect(770, 20, 81, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.grafikler)
        self.label_6.setGeometry(QtCore.QRect(10, 340, 91, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.grafikler)
        self.label_7.setGeometry(QtCore.QRect(400, 340, 101, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.grafikler)
        self.label_8.setGeometry(QtCore.QRect(770, 340, 111, 16))
        self.label_8.setObjectName("label_8")
        self.anlikGoruntuWidget = QtWidgets.QWidget(self.centralwidget)
        self.anlikGoruntuWidget.setGeometry(QtCore.QRect(1420, 30, 391, 271))
        self.anlikGoruntuWidget.setStyleSheet("background-color: white;")
        self.anlikGoruntuWidget.setObjectName("anlikGoruntuWidget")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(1420, 10, 91, 16))
        self.label_9.setObjectName("label_9")
        # self.gyroWidget = QtWidgets.QWidget(self.centralwidget)
        # self.gyroWidget = QtWidgets.QOpenGLWidget(self.centralwidget)
        '''self.gyroWidget.setGeometry(QtCore.QRect(1420, 330, 391, 271))
        self.gyroWidget.setStyleSheet("background-color: white;")
        self.gyroWidget.setObjectName("gyroWidget")'''
        self.glWidget = GLWidget(self.centralwidget)
        self.glWidget.setGeometry(QtCore.QRect(1420, 330, 391, 271))
        self.glWidget.setStyleSheet("background-color: white;")
        self.glWidget.setObjectName("gyroWidget")

        sliderX = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))

        sliderY = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))

        sliderZ = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderZ.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))

        self.lokasyonWidget = QWebEngineView(self.centralwidget)
        self.lokasyonWidget.setGeometry(QtCore.QRect(1420, 660, 391, 271))
        self.lokasyonWidget.setStyleSheet("background-color: white;")
        self.lokasyonWidget.setObjectName("lokasyonWidget")

        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(1420, 310, 121, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(1420, 640, 111, 16))
        self.label_11.setObjectName("label_11")
        self.TakimBilgileriGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.TakimBilgileriGroup.setGeometry(QtCore.QRect(50, 20, 201, 201))
        self.TakimBilgileriGroup.setStyleSheet("background-color: white;border-radius:15px;")
        self.TakimBilgileriGroup.setObjectName("TakimBilgileriGroup")
        self.logoLabel = QtWidgets.QLabel(self.TakimBilgileriGroup)
        self.logoLabel.setGeometry(QtCore.QRect(50, 30, 101, 111))
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap("logo.png"))
        self.logoLabel.setScaledContents(False)
        self.logoLabel.setObjectName("logoLabel")
        self.takimAdiLabel = QtWidgets.QLabel(self.TakimBilgileriGroup)
        self.takimAdiLabel.setGeometry(QtCore.QRect(20, 140, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.takimAdiLabel.setFont(font)
        self.takimAdiLabel.setObjectName("takimAdiLabel")
        self.takimIdLabel = QtWidgets.QLabel(self.TakimBilgileriGroup)
        self.takimIdLabel.setGeometry(QtCore.QRect(20, 170, 131, 16))

        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.takimIdLabel.setFont(font)
        self.takimIdLabel.setObjectName("takimIdLabel")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(60, 250, 71, 16))

        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)

        self.label_15.setFont(font)
        self.label_15.setWordWrap(False)
        self.label_15.setObjectName("label_15")
        self.statuNoLabel = QtWidgets.QLabel(self.centralwidget)
        self.statuNoLabel.setGeometry(QtCore.QRect(130, 250, 91, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.statuNoLabel.setFont(font)
        self.statuNoLabel.setObjectName("statuNoLabel")

        self.videoAktarimLabel = QtWidgets.QLabel(self.centralwidget)
        self.videoAktarimLabel.setGeometry(QtCore.QRect(60, 320, 171, 16))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.videoAktarimLabel.setFont(font)
        self.videoAktarimLabel.setWordWrap(False)
        self.videoAktarimLabel.setObjectName("videoAktarimLabel")
        self.videoAktarimBilgisiLabel = QtWidgets.QLabel(self.centralwidget)
        self.videoAktarimBilgisiLabel.setGeometry(QtCore.QRect(80, 350, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.videoAktarimBilgisiLabel.setFont(font)
        self.videoAktarimBilgisiLabel.setObjectName("videoAktarimBilgisiLabel")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(50, 300, 201, 101))
        self.graphicsView.setStyleSheet("background-color: white;border-radius:15px;")
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(50, 240, 201, 41))
        self.graphicsView_2.setStyleSheet("background-color: white;border-radius:15px;")
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.tableWidget1 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget1.setGeometry(QtCore.QRect(80, 770, 1330, 192))
        self.tableWidget1.setObjectName("tableWidget")
        self.tableWidget1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget1.setColumnCount(18)
        self.tableWidget1.setHorizontalHeaderLabels(["takim_no","paket_numarasi","gonderme_tarihi","gonderme_saati","basinc","yukseklik","inis_hizi","sicaklik","pil_gerilimi","gps_altitude","gps_latitude","gps_longitude","uydu_statusu","pitch","roll","yaw","donus_sayisi","video_aktarim_bilgisi"])
        #self.tableWidget1.setRowCount(0)
        self.gyroLabel = QtWidgets.QLabel(self.centralwidget)
        self.gyroLabel.setGeometry(QtCore.QRect(1450, 610, 341, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.gyroLabel.setFont(font)
        self.gyroLabel.setStyleSheet("background-color: white;")
        self.gyroLabel.setObjectName("gyroLabel")
        self.lokasyonLabel = QtWidgets.QLabel(self.centralwidget)
        self.lokasyonLabel.setGeometry(QtCore.QRect(1450, 940, 341, 21))
        self.lokasyonLabel.setStyleSheet("background-color: white;")
        self.lokasyonLabel.setObjectName("lokasyonLabel")
        self.ayrilmaKomutuGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.ayrilmaKomutuGroup.setGeometry(QtCore.QRect(490, 10, 241, 81))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ayrilmaKomutuGroup.setFont(font)
        self.ayrilmaKomutuGroup.setStyleSheet("background-color: white;border-radius:15px;")
        self.ayrilmaKomutuGroup.setObjectName("ayrilmaKomutuGroup")
        self.ayrilButton = QtWidgets.QPushButton(self.ayrilmaKomutuGroup)
        self.ayrilButton.setGeometry(QtCore.QRect(70, 30, 111, 31))
        self.ayrilButton.setStyleSheet("background-color: black;color:white;")
        self.ayrilButton.setObjectName("ayrilButton")
        self.ayrilButton.clicked.connect(self.sendTwoCommand)
        self.manuelTahrikGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.manuelTahrikGroup.setGeometry(QtCore.QRect(760, 10, 271, 81))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.manuelTahrikGroup.setFont(font)
        self.manuelTahrikGroup.setStyleSheet("background-color: white;border-radius:15px;")
        self.manuelTahrikGroup.setObjectName("manuelTahrikGroup")
        self.baslatButton = QtWidgets.QPushButton(self.manuelTahrikGroup)
        self.baslatButton.setGeometry(QtCore.QRect(10, 30, 111, 31))
        self.baslatButton.setStyleSheet("background-color: black;color:white;")
        self.baslatButton.setObjectName("baslatButton")
        self.baslatButton.clicked.connect(self.sendThreeCommand)
        self.durdurButton = QtWidgets.QPushButton(self.manuelTahrikGroup)
        self.durdurButton.setGeometry(QtCore.QRect(150, 30, 111, 31))
        self.durdurButton.setStyleSheet("background-color: black;color:white;")
        self.durdurButton.setObjectName("durdurButton")
        self.durdurButton.clicked.connect(self.sendFourCommand)
        self.videoAktarimiGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.videoAktarimiGroup.setGeometry(QtCore.QRect(1060, 10, 301, 81))
        self.videoAktarimiGroup.setStyleSheet("background-color: white;border-radius:15px;")
        self.videoAktarimiGroup.setObjectName("videoAktarimiGroup")
        self.label_20 = QtWidgets.QLabel(self.videoAktarimiGroup)
        self.label_20.setGeometry(QtCore.QRect(10, 30, 71, 16))
        self.label_20.setObjectName("label_20")
        self.dosyaSecButton = QtWidgets.QToolButton(self.videoAktarimiGroup)
        self.dosyaSecButton.setGeometry(QtCore.QRect(80, 30, 27, 22))
        self.dosyaSecButton.setStyleSheet("background-color:black;color:white;")
        self.dosyaSecButton.setObjectName("dosyaSecButton")
        self.gonderButton = QtWidgets.QPushButton(self.videoAktarimiGroup)
        self.gonderButton.setGeometry(QtCore.QRect(170, 30, 111, 31))
        self.gonderButton.setStyleSheet("background-color: black;color:white;")
        self.gonderButton.setObjectName("gonderButton")
        self.gonderButton.clicked.connect(self.sendFiveCommand)
        self.donusGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.donusGroup.setGeometry(QtCore.QRect(50, 430, 201, 111))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.donusGroup.setFont(font)
        self.donusGroup.setStyleSheet("background-color:white;border-radius:15px;")
        self.donusGroup.setObjectName("donusGroup")
        self.donusSayisiLabel = QtWidgets.QLabel(self.donusGroup)
        self.donusSayisiLabel.setGeometry(QtCore.QRect(90, 40, 21, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.donusSayisiLabel.setFont(font)
        self.donusSayisiLabel.setObjectName("donusSayisiLabel")
        self.paketSayisiGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.paketSayisiGroup.setGeometry(QtCore.QRect(50, 560, 201, 111))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.paketSayisiGroup.setFont(font)
        self.paketSayisiGroup.setStyleSheet("background-color:white;border-radius:15px;")
        self.paketSayisiGroup.setObjectName("paketSayisiGroup")
        self.paketSayisiLabel = QtWidgets.QLabel(self.paketSayisiGroup)
        self.paketSayisiLabel.setGeometry(QtCore.QRect(75, 20, 100, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.paketSayisiLabel.setFont(font)
        self.paketSayisiLabel.setObjectName("paketSayisiLabel")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(310, 10, 161, 81))
        self.groupBox.setStyleSheet("background-color: white;border-radius:15px;")
        self.groupBox.setObjectName("groupBox")
        self.kalibreEtButton = QtWidgets.QPushButton(self.groupBox)
        self.kalibreEtButton.setGeometry(QtCore.QRect(30, 30, 111, 31))
        self.kalibreEtButton.setStyleSheet("background-color: black;color:white;border-radius:15px;")
        self.kalibreEtButton.setObjectName("kalibreEtButton")
        self.kalibreEtButton.clicked.connect(self.sendOneCommand)
        self.graphicsView_2.raise_()
        self.graphicsView.raise_()
        self.grafikler.raise_()
        self.anlikGoruntuWidget.raise_()
        self.label_9.raise_()
        self.glWidget.raise_()
        self.lokasyonWidget.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.TakimBilgileriGroup.raise_()
        self.label_15.raise_()
        self.statuNoLabel.raise_()
        self.videoAktarimLabel.raise_()
        self.videoAktarimBilgisiLabel.raise_()
        self.tableWidget1.raise_()
        self.gyroLabel.raise_()
        self.lokasyonLabel.raise_()
        self.ayrilmaKomutuGroup.raise_()
        self.manuelTahrikGroup.raise_()
        self.videoAktarimiGroup.raise_()
        self.donusGroup.raise_()
        self.paketSayisiGroup.raise_()
        self.groupBox.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
        self.menubar.setObjectName("menubar")
        self.menuAnaSayfa = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.menuAnaSayfa.setFont(font)
        self.menuAnaSayfa.setObjectName("menuAnaSayfa")
        self.menuGrafikler = QtWidgets.QMenu(self.menubar)
        self.menuGrafikler.setObjectName("menuGrafikler")
        self.menuHarita = QtWidgets.QMenu(self.menubar)
        self.menuHarita.setObjectName("menuHarita")
        self.menuAnlikGoruntu = QtWidgets.QMenu(self.menubar)
        self.menuAnlikGoruntu.setObjectName("menuAnlikGoruntu")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menubar.addAction(self.menuAnaSayfa.menuAction())
        self.menubar.addAction(self.menuGrafikler.menuAction())
        self.menubar.addAction(self.menuHarita.menuAction())
        self.menubar.addAction(self.menuAnlikGoruntu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BTÜ Ülgen Yer İstasyonu"))
        self.grafikler.setTitle(_translate("MainWindow", "GRAFİKLER"))
        self.label.setText(_translate("MainWindow", "Yükseklik (m)"))
        self.label_2.setText(_translate("MainWindow", "Sıcaklık (°C)"))
        self.label_5.setText(_translate("MainWindow", "Basınç (Pa)"))
        self.label_6.setText(_translate("MainWindow", "İniş Hızı (m/s)"))
        self.label_7.setText(_translate("MainWindow", "Pil Gerilimi (V)"))
        self.label_8.setText(_translate("MainWindow", "GPS Altitude (m) "))
        self.label_9.setText(_translate("MainWindow", "Anlık Görüntü"))
        self.label_10.setText(_translate("MainWindow", "Gyro Simülasyonu"))
        self.label_11.setText(_translate("MainWindow", "Lokasyon Bilgisi"))
        self.TakimBilgileriGroup.setTitle(_translate("MainWindow", "Takım Bilgileri"))
        self.takimAdiLabel.setText(_translate("MainWindow", "Takım Adı: BTÜ Ülgen"))
        self.takimIdLabel.setText(_translate("MainWindow", "Takım ID: 39374"))
        self.label_15.setText(_translate("MainWindow", "STATÜ:"))
        self.statuNoLabel.setText(_translate("MainWindow", "STATÜ NO"))
        self.videoAktarimLabel.setText(_translate("MainWindow", "VIDEO AKTARIM BİLGİSİ"))
        self.videoAktarimBilgisiLabel.setText(_translate("MainWindow", "Hayır"))
        self.gyroLabel.setText(_translate("MainWindow", "      X: 123123        Y: 12312312        Z: 12123123      "))
        self.lokasyonLabel.setText(
            _translate("MainWindow", "      X: 123123        Y: 12312312        Z: 12123123      "))
        self.ayrilmaKomutuGroup.setTitle(_translate("MainWindow", "Ayrılma Komutu"))
        self.ayrilButton.setText(_translate("MainWindow", "Ayır"))
        self.manuelTahrikGroup.setTitle(_translate("MainWindow", "Manuel Tahrik Komutu"))
        self.baslatButton.setText(_translate("MainWindow", "Başlat"))
        self.durdurButton.setText(_translate("MainWindow", "Durdur"))
        self.videoAktarimiGroup.setTitle(_translate("MainWindow", "Video Aktarımı"))
        self.label_20.setText(_translate("MainWindow", "Dosya Seç:"))
        self.dosyaSecButton.setText(_translate("MainWindow", "..."))
        self.dosyaSecButton.clicked.connect(self.chooseVideo)
        self.gonderButton.setText(_translate("MainWindow", "Gönder"))
        self.donusGroup.setTitle(_translate("MainWindow", "Dönüş Sayısı:"))
        self.donusSayisiLabel.setText(_translate("MainWindow", "3"))
        self.paketSayisiGroup.setTitle(_translate("MainWindow", "Paket Sayısı:"))
        self.paketSayisiLabel.setText(_translate("MainWindow", "9"))
        self.groupBox.setTitle(_translate("MainWindow", "Uydu Kalibresi"))
        self.kalibreEtButton.setText(_translate("MainWindow", "Kalibre Et"))
        self.menuAnaSayfa.setTitle(_translate("MainWindow", "Ana Sayfa"))
        self.menuGrafikler.setTitle(_translate("MainWindow", "Grafikler"))
        self.menuHarita.setTitle(_translate("MainWindow", "Harita"))
        self.menuAnlikGoruntu.setTitle(_translate("MainWindow", "Anlık Görüntü"))
        # self.baslatButton.clicked.connect(self.realTimeVideo)
        self.mapShowing()
        self.update_graph()
        self.update_graph2()
        self.update_graph3()
        self.update_graph4()
        self.update_graph5()
        self.update_graph6()
        self.timers()
        #self.createTable()

    def update_graph(self):
        global xs
        global ys

        global paketSayisi
        global yukseklik
        xs.append(paketSayisi)
        ys.append(yukseklik)

        xs = xs[-6:]
        ys = ys[-6:]

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(xs, ys, linewidth=2, label="{1}")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.MplWidget.canvas.draw()
        paketSayisi += 1


    def update_graph2(self):
        global xs2
        global ys2

        global paketSayisi
        global sicaklik
        xs2.append(paketSayisi)
        ys2.append(sicaklik)

        xs2 = xs2[-6:]
        ys2 = ys2[-6:]

        self.sicaklikWidget.canvas.axes.clear()
        self.sicaklikWidget.canvas.axes.plot(xs2, ys2, linewidth=2, label="{1}")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.sicaklikWidget.canvas.draw()

    def update_graph3(self):
        global xs3
        global ys3

        # Add x and y to lists
        global paketSayisi
        global basinc
        xs3.append(paketSayisi)
        ys3.append(basinc)

        # Limit x and y lists to 20 items
        xs3 = xs3[-6:]
        ys3 = ys3[-6:]

        self.basincWidget.canvas.axes.clear()
        self.basincWidget.canvas.axes.plot(xs3, ys3, linewidth=2, label="{1}")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.basincWidget.canvas.draw()
        print(basinc)
    def update_graph4(self):
        global xs4
        global ys4

        # Add x and y to lists
        global paketSayisi
        global inis_hizi
        xs4.append(paketSayisi)
        ys4.append(inis_hizi)

        # Limit x and y lists to 20 items
        xs4 = xs4[-6:]
        ys4 = ys4[-6:]

        self.hizWidget.canvas.axes.clear()
        self.hizWidget.canvas.axes.plot(xs4, ys4, linewidth=2, label="{1}")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.hizWidget.canvas.draw()

    def update_graph5(self):
        global xs5
        global ys5

        # Add x and y to lists
        global paketSayisi
        global pil_gerilimi
        xs5.append(paketSayisi)
        ys5.append(pil_gerilimi)

        # Limit x and y lists to 20 items
        xs5 = xs5[-6:]
        ys5 = ys5[-6:]

        self.pilGerilimiWidget.canvas.axes.clear()
        self.pilGerilimiWidget.canvas.axes.plot(xs5, ys5, linewidth=2, label="{1}")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.pilGerilimiWidget.canvas.draw()

    def update_graph6(self):
        global xs6
        global ys6

        # Add x and y to lists
        global paketSayisi
        global gps_altitude
        xs6.append(paketSayisi)
        ys6.append(gps_altitude)

        # Limit x and y lists to 20 items
        xs6 = xs6[-6:]
        ys6 = ys6[-6:]

        self.gpsAltitudeWidget.canvas.axes.clear()
        self.gpsAltitudeWidget.canvas.axes.plot(xs6, ys6, linewidth=2, label="{1}")
        # labellines.labelLines(self.MplWidget.canvas.axes.get_lines())
        self.gpsAltitudeWidget.canvas.draw()

    def sendOneCommand(self):
        global yer_istasyonu_socket
        komut = "1"
        yer_istasyonu_socket.send(komut.encode())

    def sendTwoCommand(self):
        global yer_istasyonu_socket
        komut = "2"
        yer_istasyonu_socket.send(komut.encode())

    def sendThreeCommand(self):
        global yer_istasyonu_socket
        komut = "3"
        yer_istasyonu_socket.send(komut.encode())

    def sendFourCommand(self):
        global yer_istasyonu_socket
        komut = "4"
        yer_istasyonu_socket.send(komut.encode())
    
    def sendFiveCommand(self):
        global yer_istasyonu_socket,video
        komut = "5 "+str(len(video))
        yer_istasyonu_socket.send(komut.encode())
        yer_istasyonu_socket.send(video)
        #dThread = Thread(target=self.download())
        #dThread.start()
        # download = DownloadVideo()
        # download.start()
        # download.dsignal.connect(self.downbitti)
    
    def download(self):
        global yer_istasyonu_socket,video
        komut = "5 "+str(len(video))
        yer_istasyonu_socket.send(komut.encode())
        yer_istasyonu_socket.send(video)
        #self.dsignal.emit(100)

    def downbitti(self):
         self.videoAktarimBilgisiLabel.setText("Evet")     

    def getData(self):
        global yer_istasyonu_socket,index
        global takim_no,paket_numarasi,basinc,yukseklik,inis_hizi,sicaklik,pil_gerilimi,gps_altitude,gps_latitude,gps_longitude,uydu_statusu,pitch,roll,yaw,donus_sayisi,video_aktarim_bilgisi
        komut = "0"
        yer_istasyonu_socket.send(komut.encode())
        telemetri_paketi = yer_istasyonu_socket.recv(1024).decode()
        
        #self.updTable.usignal.connect(self.bitti)
        
        print(telemetri_paketi)
        son_telemetri = telemetri_paketi.split(",")
        self.updTable = UpdateTable(self.tableWidget1,son_telemetri)
        self.updTable.start()
        self.tableWidget1.update()
        #self.tableWidget1.scrollToItem(self.tableWidget1.itemAt(index,0))
        self.tableWidget1.scrollToItem(self.tableWidget1.item(index,0))
        index +=1
        takim_no = int(son_telemetri[0])
        paket_numarasi = int(son_telemetri[1])
        basinc = float(son_telemetri[4])
        yukseklik = float(son_telemetri[5])
        inis_hizi = float(son_telemetri[6])
        sicaklik = float(son_telemetri[7])
        pil_gerilimi = float(son_telemetri[8])
        gps_latitude, gps_longitude, gps_altitude = float(son_telemetri[9]), float(son_telemetri[10]), float(
            son_telemetri[11])
        uydu_statusu = int(son_telemetri[12])
        pitch, roll, yaw = float(son_telemetri[13]), float(son_telemetri[15]), float(son_telemetri[14])
        self.glWidget.setRotX(pitch)
        self.glWidget.setRotY(roll)
        self.glWidget.setRotZ(yaw)
        donus_sayisi = int(son_telemetri[16])
        video_aktarim_bilgisi = str(son_telemetri[17])
        self.paketSayisiLabel.setText(str(paket_numarasi))
        self.statuNoLabel.setText(str(uydu_statusu))
        self.donusSayisiLabel.setText(str(donus_sayisi))


    def chooseVideo(self):
        global video
        file_filter = 'Data File (*.mkv *mp4 *.avi);; Video File (*.mkv *.avi)'
        response = QFileDialog.getOpenFileName(
            parent=self.dosyaSecButton,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Video File (*.mkv *.avi)'
        )
        print(response[0])
        
        with open(response[0],"rb") as f:
            video = f.read()
            print(len(video))

    
    def timers(self):

        self.timer0 = QtCore.QTimer()
        self.timer0.setInterval(1000)
        self.timer0.timeout.connect(self.getData)
        self.timer0.start()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start()

        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(1000)
        self.timer2.timeout.connect(self.update_graph2)
        self.timer2.start()

        self.timer3 = QtCore.QTimer()
        self.timer3.setInterval(1000)
        self.timer3.timeout.connect(self.update_graph3)
        self.timer3.start()

        self.timer4 = QtCore.QTimer()
        self.timer4.setInterval(1000)
        self.timer4.timeout.connect(self.update_graph4)
        self.timer4.start()

        self.timer5 = QtCore.QTimer()
        self.timer5.setInterval(1000)
        self.timer5.timeout.connect(self.update_graph5)
        self.timer5.start()

        self.timer6 = QtCore.QTimer()
        self.timer6.setInterval(1000)
        self.timer6.timeout.connect(self.update_graph6)
        self.timer6.start()

        self.timer7 = QtCore.QTimer()
        self.timer7.setInterval(20)
        self.timer7.timeout.connect(self.glWidget.updateGL)
        self.timer7.start()

        self.timer8 = QtCore.QTimer()
        self.timer8.setInterval(1000)
        self.timer8.timeout.connect(self.haritayiGuncelle)
        self.timer8.start()

    def bitti(self,val):
        print(val)    
        
    def haritayiGuncelle(self):
        global gps_latitude,gps_longitude
        folium.Marker([gps_latitude,gps_longitude]).add_to(self.m)

        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.lokasyonWidget.setHtml(data.getvalue().decode())
        return

    # def realTimeVideo(self):

    #     self.cap = cv2.VideoCapture(0)

    #     fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    #     self.out = cv2.VideoWriter('output.avi',fourcc, 25.0, (640,480))

    #     while(self.cap.isOpened()):
    #         ret, frame = self.cap.read()
    #         if ret==True:
    #             frame = cv2.flip(frame,180)

    #             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #             frame = cv2.resize(frame,(311,221))

    #             image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
    #             self.anlikGoruntuWidget.setPixmap(QtGui.QPixmap.fromImage(image))
    #             if cv2.waitKey(1) & 0xFF == ord('q'):
    #                 break
    #         else:
    #             break
    #         cv2.destroyAllWindows()

    
    def mapShowing(self):
        coordinate = (40.21799432168916, 28.847811135149378)
        self.m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=14,
            location=coordinate
        )
        folium.Marker([40.21795441621626, 28.847589029741034]).add_to(self.m)

        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.lokasyonWidget.setHtml(data.getvalue().decode())

    '''def createTable(self):
       # Create table
        # i=0
        
        for i in range(0,25):
            print(i)
            self.tableWidget1.setRowCount(100)
            self.tableWidget1.setColumnCount(18)
            self.tableWidget1.setItem(i,0, QTableWidgetItem(self.arr[0]))
            self.tableWidget1.setItem(i,1, QTableWidgetItem(self.arr[0]))
            self.tableWidget1.setItem(i,2, QTableWidgetItem(self.arr[0]))
            self.tableWidget1.setItem(i,3, QTableWidgetItem(self.arr[0]))
            self.tableWidget1.setItem(i,4, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,5, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,6, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,7, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,8, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,9, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,10, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,11, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,12, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,13, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,14, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,15, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,16, QTableWidgetItem("Cell (1,1)"))
            self.tableWidget1.setItem(i,17, QTableWidgetItem("Cell (1,1)"))
            # self.tableWidget1.move(0,i)'''
class UpdateTable(QtCore.QThread) :
    def __init__(self, table,arr):
        super(UpdateTable,self).__init__()
        self.table = table
        self.arr =arr
    usignal = QtCore.pyqtSignal(int)
    def run(self):
            global index
            self.table.setRowCount(10090)
            self.table.setItem(index,0, QTableWidgetItem(self.arr[0]))
            self.table.setItem(index,1, QTableWidgetItem(self.arr[1]))
            self.table.setItem(index,2, QTableWidgetItem(self.arr[2]))
            self.table.setItem(index,3, QTableWidgetItem(self.arr[3]))
            self.table.setItem(index,4, QTableWidgetItem(self.arr[4]))
            self.table.setItem(index,5, QTableWidgetItem(self.arr[5]))
            self.table.setItem(index,6, QTableWidgetItem(self.arr[6]))
            self.table.setItem(index,7, QTableWidgetItem(self.arr[7]))
            self.table.setItem(index,8, QTableWidgetItem(self.arr[8]))
            self.table.setItem(index,9, QTableWidgetItem(self.arr[9]))
            self.table.setItem(index,10, QTableWidgetItem(self.arr[10]))
            self.table.setItem(index,11, QTableWidgetItem(self.arr[11]))
            self.table.setItem(index,12, QTableWidgetItem(self.arr[12]))
            self.table.setItem(index,13, QTableWidgetItem(self.arr[13]))
            self.table.setItem(index,14, QTableWidgetItem(self.arr[14]))
            self.table.setItem(index,15, QTableWidgetItem(self.arr[15]))
            self.table.setItem(index,16, QTableWidgetItem(self.arr[16]))
            self.table.setItem(index,17, QTableWidgetItem(self.arr[17]))
            self.usignal.emit(100)
    
# class DownloadVideo(QtCore.QThread) :
#         def __init__(self):
#             super(DownloadVideo,self).__init__()
            
#         dsignal = QtCore.pyqtSignal(int)
#         def run(self):
                
#             global yer_istasyonu_socket,video
#             komut = "5 "+str(len(video))
#             yer_istasyonu_socket.send(komut.encode())
#             yer_istasyonu_socket.send(video)
#             self.dsignal.emit(100)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())