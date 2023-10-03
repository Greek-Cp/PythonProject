import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QLabel, QWidget, QGridLayout, QMenu
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import QTimer
import cv2
import numpy as np
import sys
import subprocess


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        dark_stylesheet = '''
            QWidget {
                background-color: #1F1F1F;
                color: #FFFFFF;
            }
            QLabel {
                border: 2px solid #FFFFFF;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #C147E9, stop:1 #8823D5);
                color: #FFFFFF;
            }
            QMenuBar::item:selected {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #C147E9, stop:1 #8823D5);
                color: #FFFFFF;
                border-radius: 8px;
                border: 1px solid #FFFFFF;
            }
            QMenuBar::item {
                padding: 5px 10px;
            }
            '''

        self.setStyleSheet(dark_stylesheet)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(200,200)
        self.setMinimumSize(100, 100)  # Set the minimum size you desire
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
        self.beforeImageView.setScaledContents(True)  # Make it resizable
        grid_layout.addWidget(self.beforeImageView, 0, 0)

        self.afterImageView = QLabel(self.centralwidget)
        self.afterImageView.setStyleSheet("border: 2px solid black;")
        self.afterImageView.setScaledContents(True)  # Make it resizable
        grid_layout.addWidget(self.afterImageView, 0, 1)

        self.hasilPerhitunganAritmatika = QLabel(self.centralwidget)
        self.hasilPerhitunganAritmatika.setStyleSheet("border: 2px solid black;")
        self.hasilPerhitunganAritmatika.setScaledContents(True)  # Make it resizable
        grid_layout.addWidget(self.hasilPerhitunganAritmatika, 0, 2)
        self.actionAdd.triggered.connect(self.perform_addition)
        self.actionSubtract.triggered.connect(self.perform_subtraction)
        self.actionMultiply.triggered.connect(self.perform_multiplication)
        self.actionDivide.triggered.connect(self.perform_division)
        self.actionAnd.triggered.connect(self.perform_and_operation)
        self.actionXor.triggered.connect(self.perform_xor_operation)
        self.actionNot.triggered.connect(self.perform_not_operation)
        
    def perform_addition(self):
        if hasattr(self, 'image1') and hasattr(self, 'image2'):
            height1, width1, _ = self.image1.shape
            height2, width2, _ = self.image2.shape
            width = min(width1, width2)
            height = min(height1, height2)
            result = np.zeros((height, width, 3), dtype=np.uint8)

            for x in range(width):
                for y in range(height):
                    color1 = self.image1[y, x]
                    color2 = self.image2[y, x]

                    r_result = min(int(color1[0]) + int(color2[0]), 255)
                    g_result = min(int(color1[1]) + int(color2[1]), 255)
                    b_result = min(int(color1[2]) + int(color2[2]), 255)

                    result[y, x] = [r_result, g_result, b_result]

            self.show_image(result, 'Addition Result')
            self.display_arithmetic_result(result)

    def perform_subtraction(self):
        if hasattr(self, 'image1') and hasattr(self, 'image2'):
            height1, width1, _ = self.image1.shape
            height2, width2, _ = self.image2.shape
            width = min(width1, width2)
            height = min(height1, height2)
            result = np.zeros((height, width, 3), dtype=np.uint8)

            for x in range(width):
                for y in range(height):
                    color1 = self.image1[y, x]
                    color2 = self.image2[y, x]

                    r_result = max(int(color1[0]) - int(color2[0]), 0)
                    g_result = max(int(color1[1]) - int(color2[1]), 0)
                    b_result = max(int(color1[2]) - int(color2[2]), 0)

                    result[y, x] = [r_result, g_result, b_result]

            self.show_image(result, 'Subtraction Result')
            self.display_arithmetic_result(result)

    def perform_multiplication(self):
        if hasattr(self, 'image1') and hasattr(self, 'image2'):
            height1, width1, _ = self.image1.shape
            height2, width2, _ = self.image2.shape
            width = min(width1, width2)
            height = min(height1, height2)
            result = np.zeros((height, width, 3), dtype=np.uint8)

            for x in range(width):
                for y in range(height):
                    color1 = self.image1[y, x]
                    color2 = self.image2[y, x]

                    r_result = min(int(color1[0]) * int(color2[0]) // 255, 255)
                    g_result = min(int(color1[1]) * int(color2[1]) // 255, 255)
                    b_result = min(int(color1[2]) * int(color2[2]) // 255, 255)

                    result[y, x] = [r_result, g_result, b_result]

            self.show_image(result, 'Multiplication Result')
            self.display_arithmetic_result(result)

    def perform_division(self):
        if hasattr(self, 'image1') and hasattr(self, 'image2'):
            height1, width1, _ = self.image1.shape
            height2, width2, _ = self.image2.shape
            width = min(width1, width2)
            height = min(height1, height2)
            result = np.zeros((height, width, 3), dtype=np.uint8)

            for x in range(width):
                for y in range(height):
                    color1 = self.image1[y, x]
                    color2 = self.image2[y, x]

                    r_result = 0 if int(color2[0]) == 0 else min(int(color1[0]) * 255 // int(color2[0]), 255)
                    g_result = 0 if int(color2[1]) == 0 else min(int(color1[1]) * 255 // int(color2[1]), 255)
                    b_result = 0 if int(color2[2]) == 0 else min(int(color1[2]) * 255 // int(color2[2]), 255)

                    result[y, x] = [r_result, g_result, b_result]

            self.show_image(result, 'Division Result')
            self.display_arithmetic_result(result)

    def perform_and_operation(self):
        if hasattr(self, 'image1') and hasattr(self, 'image2'):
            height1, width1, _ = self.image1.shape
            height2, width2, _ = self.image2.shape
            width = min(width1, width2)
            height = min(height1, height2)
            result = np.zeros((height, width, 3), dtype=np.uint8)

            for x in range(width):
                for y in range(height):
                    color1 = self.image1[y, x]
                    color2 = self.image2[y, x]

                    r_result = int(color1[0]) & int(color2[0])
                    g_result = int(color1[1]) & int(color2[1])
                    b_result = int(color1[2]) & int(color2[2])

                    result[y, x] = [r_result, g_result, b_result]

            self.show_image(result, 'AND Result')
            self.display_arithmetic_result(result)

    def perform_xor_operation(self):
        if hasattr(self, 'image1') and hasattr(self, 'image2'):
            height1, width1, _ = self.image1.shape
            height2, width2, _ = self.image2.shape
            width = min(width1, width2)
            height = min(height1, height2)
            result = np.zeros((height, width, 3), dtype=np.uint8)

            for x in range(width):
                for y in range(height):
                    color1 = self.image1[y, x]
                    color2 = self.image2[y, x]

                    r_result = int(color1[0]) ^ int(color2[0])
                    g_result = int(color1[1]) ^ int(color2[1])
                    b_result = int(color1[2]) ^ int(color2[2])

                    result[y, x] = [r_result, g_result, b_result]

            self.show_image(result, 'XOR Result')
            self.display_arithmetic_result(result)

    def perform_not_operation(self):
        if hasattr(self, 'image1'):
            height1, width1, _ = self.image1.shape
            result = np.zeros((height1, width1, 3), dtype=np.uint8)

            for x in range(width1):
                for y in range(height1):
                    color1 = self.image1[y, x]

                    r_result = 255 - int(color1[0])
                    g_result = 255 - int(color1[1])
                    b_result = 255 - int(color1[2])

                    result[y, x] = [r_result, g_result, b_result]

            self.show_image(result, 'NOT Result')
            self.display_arithmetic_result(result)

    def display_arithmetic_result(self, result):
        result_image = QImage(result.data, result.shape[1], result.shape[0], result.shape[1] * 3, QImage.Format_RGB888)
        self.hasilPerhitunganAritmatika.setPixmap(QPixmap.fromImage(result_image))
        self.hasilPerhitunganAritmatika.setScaledContents(True)

            
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
        if filepath and hasattr(self, 'hasilPerhitunganAritmatika'):
            result_pixmap = self.hasilPerhitunganAritmatika.pixmap()
            result_image = result_pixmap.toImage()
            result_image.save(filepath)

     

    def show_image(self, image, pos='before'):
        h, w, ch = image.shape
        bytes_per_line = ch * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)

        # Set gambar pada QLabel
        if pos == 'before':
            self.beforeImageView.setPixmap(pixmap)
        elif pos == 'after':
            self.afterImageView.setPixmap(pixmap)
        else:
            self.hasilPerhitunganAritmatika.setPixmap(pixmap)

        # Agar QLabel menyesuaikan ukuran gambar
        if pos == 'before':
            self.beforeImageView.setScaledContents(True)
        elif pos == 'after':
            self.afterImageView.setScaledContents(True)
        else:
            self.hasilPerhitunganAritmatika.setScaledContents(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
