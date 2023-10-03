import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class ROIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROI Selection App")
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.roi_label = QLabel(self)
        self.roi_label.setAlignment(Qt.AlignCenter)

        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image)

        self.process_button = QPushButton("Process ROI", self)
        self.process_button.clicked.connect(self.process_roi)

        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.image_label)
        layout.addWidget(self.process_button)
        layout.addWidget(self.roi_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image = None

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        
        if file_name:
            self.image = cv2.imread(file_name)
            self.display_image(self.image)

    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def process_roi(self):
        if self.image is not None:
            # Implement ROI processing here
            # For example, you can draw a rectangle and extract ROI
            roi_image = self.image.copy()  # Create a copy of the image
            cv2.rectangle(roi_image, (100, 100), (300, 300), (0, 255, 0), 2)  # Draw a green rectangle
            roi = self.image[100:300, 100:300]  # Extract ROI using numpy slicing

            # Display the processed ROI image
            self.display_image(roi_image)
            self.display_image(roi)  # Display ROI separately in the ROI Label

    def save_image(self):
        if self.image is not None:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Processed Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
            if file_name:
                cv2.imwrite(file_name, self.image)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ROIApp()
    window.show()
    sys.exit(app.exec_())
