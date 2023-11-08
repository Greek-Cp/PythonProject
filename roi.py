from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QLabel, QWidget, QGridLayout, QAction, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt
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
        MainWindow.resize(1600, 800)

        main_layout = QVBoxLayout()
        self.setMinimumSize(800, 600)  # Set the minimum size you desire
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setLayout(main_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = self.menuBar()

        self.menuFile = self.menubar.addMenu("File")

        self.actionOpen = self.menuFile.addAction("Open Image")
        self.actionOpen.triggered.connect(self.open_image)

        self.actionSave = self.menuFile.addAction("Save Image")
        self.actionSave.triggered.connect(self.save_image)

        self.actionROI = self.menuFile.addAction("Region Of Interest")
        self.actionROI.triggered.connect(self.apply_roi)

        # Label untuk tampilan hasil ekstraksi data
        self.resultLabel = QLabel("Hasil Ekstraksi Data", self.centralwidget)
        main_layout.addWidget(self.resultLabel)

        # Grid layout untuk tampilan gambar sebelum, setelah ekstraksi, dan deteksi tepi
        grid_layout = QGridLayout()
        self.centralwidget.setLayout(main_layout)

        # Label untuk gambar sebelum
        self.beforeImageView = QLabel(self.centralwidget)
        self.beforeImageView.setAlignment(Qt.AlignCenter)  # Gambar di tengah
        self.beforeImageView.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.beforeImageView, 0, 0)

        # Label untuk gambar setelah ekstraksi
        self.afterImageView = QLabel(self.centralwidget)
        self.afterImageView.setAlignment(Qt.AlignCenter)  # Gambar di tengah
        self.afterImageView.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.afterImageView, 0, 1)

        # Label untuk hasil ekstraksi dari ROI
        self.resultImageView = QLabel(self.centralwidget)
        self.resultImageView.setAlignment(Qt.AlignCenter)  # Gambar di tengah
        self.resultImageView.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.resultImageView, 1, 0)

        # Label untuk hasil deteksi tepi
        self.edgeImageView = QLabel(self.centralwidget)
        self.edgeImageView.setAlignment(Qt.AlignCenter)  # Gambar di tengah
        self.edgeImageView.setStyleSheet("border: 2px solid black;")
        grid_layout.addWidget(self.edgeImageView, 1, 1)

        main_layout.addLayout(grid_layout)

        self.roi_active = False
        self.image = None
        self.processed_image = None
        self.roi_list = []  # Daftar ROI yang akan digunakan

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
            self.roi_active = False

    def save_image(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Image")
        if filepath and self.processed_image is not None:
            cv2.imwrite(filepath, self.processed_image)

    def show_image(self, image, pos='before', resize_mode=Qt.IgnoreAspectRatio):
        h, w, ch = image.shape
        bytes_per_line = ch * w
        image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)

        if pos == 'before':
            label = self.beforeImageView
        elif pos == 'after':
            label = self.afterImageView
        elif pos == 'result':
            label = self.resultImageView
        elif pos == 'edge':
            label = self.edgeImageView

        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)  # Gambar di tengah
        label.setScaledContents(True)  # Gambar akan diubah ukuran untuk mengisi seluruh label

    def apply_roi(self):
        self.roi_active = False
        self.processed_image = self.image.copy()
        self.roi_list = []
        self.show_image(self.processed_image, 'after')
        if self.image is not None:
            self.processed_image = self.image.copy()
            extracted_regions = []  # Daftar ekstraksi dari ROI

            for i in range(5):  # Buat 5 area ROI sebagai contoh
                # Tentukan koordinat ROI secara acak
                x = np.random.randint(0, self.processed_image.shape[1] - 100)
                y = np.random.randint(0, self.processed_image.shape[0] - 100)
                w = np.random.randint(50, 200)
                h = np.random.randint(50, 200)

                roi = self.processed_image[y:y+h, x:x+w]

                # Deteksi tepi pada ROI menggunakan Canny
                roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                roi_edges = cv2.Canny(roi_gray, threshold1=30, threshold2=100)

                # Konversi gambar tepi ke BGR untuk ditampilkan bersama dengan gambar asli
                roi_edges_bgr = cv2.cvtColor(roi_edges, cv2.COLOR_GRAY2BGR)

                # Gabungkan gambar tepi dengan ROI
                roi_with_edges = cv2.addWeighted(roi, 1, roi_edges_bgr, 1, 0)

                # Gambar ROI yang sudah diubah dengan deteksi tepi
                self.processed_image[y:y+h, x:x+w] = roi_with_edges

                # Tambahkan informasi ROI ke daftar ROI
                self.roi_list.append((x, y, w, h))
                extracted_regions.append(roi)  # Tambahkan ROI yang diekstrak ke daftar

            # Tampilkan gambar dengan area ROI yang sudah ditandai
            for (x, y, w, h) in self.roi_list:
                cv2.rectangle(self.processed_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            self.show_image(self.processed_image, 'after')
            self.roi_active = True

            # Tampilkan hasil ekstraksi hanya di label ketiga
            result_image = np.zeros_like(self.image)
            for i, roi in enumerate(extracted_regions):
                (x, y, w, h) = self.roi_list[i]
                result_image[y:y+h, x:x+w] = roi
            self.show_image(result_image, 'result')

            # Deteksi tepi pada hasil ekstraksi
            result_gray = cv2.cvtColor(result_image, cv2.COLOR_BGR2GRAY)
            result_edges = cv2.Canny(result_gray, threshold1=30, threshold2=100)

            # Konversi gambar tepi ke BGR untuk ditampilkan bersama dengan gambar asli
            result_edges_bgr = cv2.cvtColor(result_edges, cv2.COLOR_GRAY2BGR)

            # Gabungkan gambar tepi dengan hasil ekstraksi
            result_with_edges = cv2.addWeighted(result_image, 1, result_edges_bgr, 1, 0)

            # Tampilkan hasil deteksi tepi di label keempat
            self.show_image(result_with_edges, 'edge')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
