from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QLabel, QWidget, QGridLayout , QInputDialog
from PyQt5.QtGui import QPixmap , QImage , QPainter, QTransform
from PyQt5.QtCore import QTimer, Qt, QRect
import sys
sys.path.append('./lib_app')  # Assuming lib_app is in the same directory level as your main script
from lib_app.file_util import FileUtil
from geometry_operation import GeometryOperation
class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.setStyleSheet("background-color: lightgrey;")
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
        self.actionOpen.triggered.connect(lambda: FileUtil.open_image(self))

        self.actionSave = self.menuFile.addAction("Save Image")
        self.actionSave.triggered.connect(lambda: FileUtil.save_image(self))
        
        self.actionExit = self.menuFile.addAction("Exit")
        self.actionExit.triggered.connect(FileUtil.exit_application)
        
            # New Geometric Operation Menu
        self.menuGeomOp = self.menubar.addMenu("Geometric Operation")
        
        # Scalling Uniform
        self.actionScalingUniform = self.menuGeomOp.addAction("Scaling Uniform")
        
        # Scaling Non Uniform
        self.actionScalingNonUniform = self.menuGeomOp.addAction("Scaling Non Uniform")
        

        # Cropping
        self.actionCropping = self.menuGeomOp.addAction("Cropping")
        
        # Flipping Submenu
        self.menuFlipping = self.menuGeomOp.addMenu("Flipping")
        self.actionFlipHorizontal = self.menuFlipping.addAction("Flip Horizontal")
        self.actionFlipVertical = self.menuFlipping.addAction("Flip Vertical")
        self.actionCustomFlip = self.menuFlipping.addAction("Custom Flip")
        
        # Translasi Submenu
        self.menuTranslasi = self.menuGeomOp.addMenu("Translasi")
        self.actionLeft = self.menuTranslasi.addAction("Left")
        self.actionRight = self.menuTranslasi.addAction("Right")
        self.actionTop = self.menuTranslasi.addAction("Top")
        self.actionBottom = self.menuTranslasi.addAction("Bottom")
        
        # Rotasi Submenu
        self.menuRotasi = self.menuGeomOp.addMenu("Rotasi")
        self.actionCustomRotasi = self.menuRotasi.addAction("Custom Rotasi")
        self.beforeImageView = QLabel(self.centralwidget)
        self.beforeImageView.setStyleSheet("border: 2px solid black;")
        self.beforeImageView.setScaledContents(True)
        grid_layout.addWidget(self.beforeImageView, 0, 0)

        self.afterImageView = QLabel(self.centralwidget)
        self.afterImageView.setStyleSheet("border: 2px solid black;")
        self.afterImageView.setScaledContents(True)
        grid_layout.addWidget(self.afterImageView, 0, 1)
        
        # Replace your existing QAction connections with these
        self.actionScalingUniform.triggered.connect(lambda: GeometryOperation.scaling_uniform(self.pixmap, self.afterImageView))
        self.actionScalingNonUniform.triggered.connect(lambda: GeometryOperation.scaling_non_uniform(self.pixmap, self.afterImageView))
        self.actionFlipHorizontal.triggered.connect(lambda: GeometryOperation.flip_horizontal(self.pixmap, self.afterImageView))
        self.actionFlipVertical.triggered.connect(lambda: GeometryOperation.flip_vertical(self.pixmap, self.afterImageView))
        self.actionCustomFlip.triggered.connect(lambda: GeometryOperation.custom_flip(self.pixmap, self.afterImageView))
        self.actionLeft.triggered.connect(lambda: GeometryOperation.action_left(self.pixmap, self.afterImageView))
        self.actionRight.triggered.connect(lambda: GeometryOperation.action_right(self.pixmap, self.afterImageView))
        self.actionTop.triggered.connect(lambda: GeometryOperation.action_top(self.pixmap, self.afterImageView))
        self.actionBottom.triggered.connect(lambda: GeometryOperation.action_bottom(self.pixmap, self.afterImageView))
        self.menuRotasi.addAction("Rotate Image", lambda: GeometryOperation.rotate_image(self.pixmap, self.afterImageView))



        # Add this new method
    def scaling_uniform(self):
        if self.pixmap:
            img: QImage = self.pixmap.toImage()
            width, ok = QInputDialog.getInt(self, 'Input', 'Enter the width:', min=1, max=5000)
            if ok:
                height = int(width * img.height() / img.width())  # Maintain aspect ratio
                scaled_img = img.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.afterImageView.setPixmap(QPixmap.fromImage(scaled_img))

    def scaling_non_uniform(self):
        if self.pixmap:
            img: QImage = self.pixmap.toImage()
            width, ok1 = QInputDialog.getInt(self, 'Input', 'Enter the width:', min=1, max=5000)
            height, ok2 = QInputDialog.getInt(self, 'Input', 'Enter the height:', min=1, max=5000)
            if ok1 and ok2:
                scaled_img = img.scaled(width, height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                self.afterImageView.setPixmap(QPixmap.fromImage(scaled_img))


    def rotate_image(self):
        if self.pixmap:
            # Get the rotation angle from user
            angle, ok = QInputDialog.getDouble(self, "Rotate", "Enter rotation angle:", 0, -360, 360, 2)
            
            if ok:
                # Perform rotation
                transform = QTransform().rotate(angle)
                rotated_pixmap = self.pixmap.transformed(transform, Qt.SmoothTransformation)
                
                # Update the QLabel with the rotated image
                self.afterImageView.setPixmap(rotated_pixmap)


    def animate_title(self):
        titles = ["My Dark Mode App", "Welcome!", "Enjoy!", ""]
        self.setWindowTitle(titles[self.counter])
        self.counter = (self.counter + 1) % len(titles)

    def resize_images(self, event):
        size = self.size()
        # Resize the image based on the window size, or do some other adjustments.
        # This function is called every time the window is resized.

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
