from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QLabel, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt
import sys

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.setStyleSheet("background-color: lightgrey;")
        
        # Setup timer for title animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_title)
        self.counter = 0
        self.timer.start(1000)  # Update every 1 second

        # Connect window resize event to image resize function
        self.resizeEvent = self.resize_images

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 900)

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
        
        
        self.actionExit = self.menuFile.addAction("Exit")
        self.actionExit.triggered.connect(self.exit_application)
        
        self.beforeImageView = QLabel(self.centralwidget)
        self.beforeImageView.setStyleSheet("border: 2px solid black;")
        self.beforeImageView.setScaledContents(True)
        grid_layout.addWidget(self.beforeImageView, 0, 0)

        self.afterImageView = QLabel(self.centralwidget)
        self.afterImageView.setStyleSheet("border: 2px solid black;")
        self.afterImageView.setScaledContents(True)
        grid_layout.addWidget(self.afterImageView, 0, 1)
        # Add this new method
    def exit_application(self):
        QApplication.quit()
        
    def animate_title(self):
        titles = ["My Dark Mode App", "Welcome!", "Enjoy!", ""]
        self.setWindowTitle(titles[self.counter])
        self.counter = (self.counter + 1) % len(titles)

    def open_image(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if filepath:
            self.pixmap = QPixmap(filepath)
            self.beforeImageView.setPixmap(self.pixmap)

    def save_image(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG (*.png);;JPEG (*.jpg *.jpeg);;All Files (*)")
        if filepath:
            self.pixmap.save(filepath)

    def resize_images(self, event):
        size = self.size()
        # Resize the image based on the window size, or do some other adjustments.
        # This function is called every time the window is resized.

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
