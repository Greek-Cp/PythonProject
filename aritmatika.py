from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QLabel, QWidget, QGridLayout, QMenu
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import cv2
import numpy as np
import sys

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.setStyleSheet("background-color: lightgrey;")
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_title)
        self.counter = 0
        self.timer.start(1000)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200,800)

        grid_layout = QGridLayout()

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setLayout(grid_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = self.menuBar()

        self.menuFile = self.menubar.addMenu("File")
        self.actionOpen = self.menuFile.addAction("Open Images")
        self.actionOpen.triggered.connect(self.open_images)
        self.actionSave = self.menuFile.addAction("Save Image")
        self.actionSave.triggered.connect(self.save_image)

        self.menuOperasiAritmatik = self.menubar.addMenu("Operasi Aritmatik")
        self.actionAdd = self.menuOperasiAritmatik.addAction("Penjumlahan")
        self.actionSubtract = self.menuOperasiAritmatik.addAction("Pengurangan")
        self.actionMultiply = self.menuOperasiAritmatik.addAction("Perkalian")
        self.actionDivide = self.menuOperasiAritmatik.addAction("Pembagian")
        self.actionAnd = self.menuOperasiAritmatik.addAction("AND")
        self.actionXor = self.menuOperasiAritmatik.addAction("XOR")
        self.actionNot = self.menuOperasiAritmatik.addAction("NOT")

        self.beforeImageView = QLabel(self.centralwidget)
        self.beforeImageView.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.beforeImageView, 0, 0)

        self.afterImageView = QLabel(self.centralwidget)
        self.afterImageView.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.afterImageView, 0, 1)

        self.hasilPerhitunganAritmatika = QLabel(self.centralwidget)
        self.hasilPerhitunganAritmatika.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.hasilPerhitunganAritmatika, 0, 2)

    def animate_title(self):
        titles = ["My Dark Mode App", "Welcome!", "Enjoy!", ""]
        self.setWindowTitle(titles[self.counter])
        self.counter = (self.counter + 1) % len(titles)

    def open_images(self):
        options = QFileDialog.Options()
        filepaths, _ = QFileDialog.getOpenFileNames(self, "Open Images", "", "Images (*.png *.jpg *.jpeg)", options=options)
        
        if len(filepaths) >= 2:
            self.image1 = cv2.imread(filepaths[0])
            self.show_image(self.image1, 'before')

            self.image2 = cv2.imread(filepaths[1])
            self.show_image(self.image2, 'after')

    def save_image(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Image")
        if filepath:
            cv2.imwrite(filepath, self.processed_image)

    def show_image(self, image, pos='before'):
        h, w, ch = image.shape
        bytes_per_line = ch * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)

        if pos == 'before':
            self.beforeImageView.setPixmap(pixmap)
        elif pos == 'after':
            self.afterImageView.setPixmap(pixmap)
        else:
            self.hasilPerhitunganAritmatika.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
