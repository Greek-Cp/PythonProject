from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QLabel, QWidget, QGridLayout, QAction, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import QPoint, Qt
import cv2
import numpy as np
import sys

class SelectableQLabel(QLabel):
    def __init__(self, mainWindow, parent=None):
        super(SelectableQLabel, self).__init__(parent)
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.show_rectangle = False
        self.mainWindow = mainWindow

    def mousePressEvent(self, event):
        if self.mainWindow.isCropMode:
            self.startPoint = event.pos()
            self.endPoint = self.startPoint
            self.show_rectangle = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.mainWindow.isCropMode:
            self.endPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.mainWindow.isCropMode:
            self.endPoint = event.pos()
            self.show_rectangle = False
            self.update()
            self.mainWindow.crop_image()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.show_rectangle:
            qp = QPainter(self)
            pen = QPen(Qt.red, 2)
            qp.setPen(pen)
            qp.drawRect(self.startPoint.x(), self.startPoint.y(), self.endPoint.x() - self.startPoint.x(),
                        self.endPoint.y() - self.startPoint.y())

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
        self.isCropMode = False
        self.cropped_image = None  # Store the cropped image

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.setMinimumSize(800, 600)  # Set the minimum size you desire

        grid_layout = QGridLayout()

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setLayout(grid_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = self.menuBar()

        self.menuFile = self.menubar.addMenu("File")
        self.menuCrop = self.menubar.addMenu("Crop")

        self.actionOpen = self.menuFile.addAction("Open Image")
        self.actionOpen.triggered.connect(self.open_image)

        self.actionSave = self.menuFile.addAction("Save Image")
        self.actionSave.triggered.connect(self.save_image)

        self.actionEnableCrop = self.menuCrop.addAction("Enable Crop")
        self.actionEnableCrop.setCheckable(True)
        self.actionEnableCrop.triggered.connect(self.toggle_crop_mode)

        self.beforeImageView = SelectableQLabel(self, self.centralwidget)
        self.beforeImageView.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.beforeImageView, 0, 0)

        self.afterImageView = QLabel(self.centralwidget)
        self.afterImageView.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.afterImageView, 0, 1)

        self.sharpen_button = QPushButton("Sharpen", self.centralwidget)
        self.sharpen_button.clicked.connect(self.sharpen_image)
        grid_layout.addWidget(self.sharpen_button, 1, 0, 1, 2)  # Add the sharpen button to the grid layout

        self.detect_edge_button = QPushButton("Detect Edge", self.centralwidget)
        self.detect_edge_button.clicked.connect(self.detect_edge)
        grid_layout.addWidget(self.detect_edge_button, 2, 0, 1, 2)  # Add the edge detection button to the grid layout

    def toggle_crop_mode(self):
        self.isCropMode = not self.isCropMode

    def open_image(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if filepath:
            self.image = cv2.imread(filepath)
            h, w, _ = self.image.shape
            # Resize the window to accommodate two images and padding
            self.resize(w ,h)
            self.show_image(self.image, 'before')

    def crop_image(self):
        if hasattr(self, 'image'):
            x1 = self.beforeImageView.startPoint.x()
            y1 = self.beforeImageView.startPoint.y()
            x2 = self.beforeImageView.endPoint.x()
            y2 = self.beforeImageView.endPoint.y()
            self.cropped_image = self.image[y1:y2, x1:x2]
            self.show_image(self.cropped_image, 'after')

    def sharpen_image(self):
        if self.cropped_image is not None:
            # Define a sharpening kernel (3x3)
            kernel = np.array([[-1, -1, -1],
                               [-1,  9, -1],
                               [-1, -1, -1]])

            # Create an empty image for the sharpened result
            sharpened_image = cv2.filter2D(self.cropped_image, -1, kernel)

            # Show the sharpened image
            self.show_image(sharpened_image, 'after')

    def detect_edge(self):
        if self.cropped_image is not None:
            # Apply Canny edge detection
            edges = cv2.Canny(self.cropped_image, 100, 200)

            # Convert single-channel edge image to three channels
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

            # Overlay the edges on the cropped image
            result = cv2.addWeighted(self.cropped_image, 0.7, edges_colored, 0.3, 0)

            # Show the edge-detected image
            self.show_image(result, 'after')

    def save_image(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Image")
        if filepath and hasattr(self, 'cropped_image'):
            cv2.imwrite(filepath, self.cropped_image)

    def show_image(self, image, pos='before'):
        h, w, ch = image.shape
        bytes_per_line = ch * w
        qt_img = QImage(image.data.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qt_img)
        if pos == 'before':
            self.beforeImageView.setPixmap(pixmap)
        else:
            self.afterImageView.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
