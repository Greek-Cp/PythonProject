from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QLabel, QWidget, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import cv2
import numpy as np
import sys

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        dark_stylesheet = '''
            QWidget {
                background-color: #3EBE2;
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
        # Setup timer for title animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_title)
        self.counter = 0
        self.timer.start(1000)  # Update every 1 second

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200,800)

        grid_layout = QGridLayout()

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setLayout(grid_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = self.menuBar()

        self.menuFile = self.menubar.addMenu("File")

        self.actionOpen = self.menuFile.addAction("Open Image")
        self.actionOpen.triggered.connect(self.open_image)

        self.actionSave = self.menuFile.addAction("Save Image")
        self.actionSave.triggered.connect(self.save_image)

        self.btnRemoveBg = QPushButton("Remove Background", self.centralwidget)
        self.btnRemoveBg.clicked.connect(self.remove_background)
        grid_layout.addWidget(self.btnRemoveBg, 1, 0, 1, 2)

        self.beforeImageView = QLabel(self.centralwidget)
        self.beforeImageView.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.beforeImageView, 0, 0)

        self.afterImageView = QLabel(self.centralwidget)
        self.afterImageView.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.afterImageView, 0, 1)
    
    def animate_title(self):
        titles = ["My Dark Mode App", "Welcome!", "Enjoy!", ""]
        self.setWindowTitle(titles[self.counter])
        self.counter = (self.counter + 1) % len(titles)

    def open_image(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if filepath:
            self.image = cv2.imread(filepath)
            h, w, _ = self.image.shape
            self.resize(w, h)
            self.show_image(self.image, 'before')

    def save_image(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Image")
        if filepath:
            cv2.imwrite(filepath, self.processed_image)

    def remove_background(self):
        # Assuming the top-left corner has background colour
        bg_colour = self.image[0, 0]

        lower = np.array([bg_colour[0]-40, bg_colour[1]-40, bg_colour[2]-40])
        upper = np.array([bg_colour[0]+40, bg_colour[1]+40, bg_colour[2]+40])

        mask = cv2.inRange(self.image, lower, upper)
        self.processed_image = np.copy(self.image)
        self.processed_image[mask != 0] = [0, 0, 0]
        
        self.show_image(self.processed_image, 'after')

    def show_image(self, image, pos='before'):
        h, w, ch = image.shape
        bytes_per_line = ch * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)

        if pos == 'before':
            self.beforeImageView.setPixmap(pixmap)
        else:
            self.afterImageView.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
