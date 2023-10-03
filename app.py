from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QLabel, QWidget, QGridLayout , QInputDialog,QAction, QMenu 
from PyQt5.QtGui import QPixmap , QImage , QPainter, QTransform , QColor
from PyQt5.QtCore import QTimer, Qt, QRect
import matplotlib.pyplot as plt
import sys
import numpy as np 
from matplotlib import cm
import cv2
from scipy import signal
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
            
        # Add new 'View Histogram' menu
        self.menuHistogram = QMenu(self.menubar)
        self.menuHistogram.setTitle("View Histogram")
        
        self.histogramInput = QAction("Histogram Input", self)
        self.histogramOutput = QAction("Histogram Output", self)
        self.histogramInputOutput = QAction("Histogram Input Output", self)

        self.menuColors = self.menubar.addMenu("Colors")
        self.actionBrightness = QAction("Brightness", self)
        self.actionContrast = QAction("Contrast", self)
        self.actionThreshold = QAction("Threshold", self)
        self.actionInvers = QAction("Invers", self)
        
        self.menuColors.addAction(self.actionBrightness)
        self.menuColors.addAction(self.actionContrast)
        self.menuColors.addAction(self.actionThreshold)
        self.menuColors.addAction(self.actionInvers)

        # Bit-Depth Menu
        self.menuBitDepth = self.menubar.addMenu("Bit-Depth")
        self.action1Bit = QAction("1 Bit", self)
        self.action2Bit = QAction("2 Bit", self)
        self.action3Bit = QAction("3 Bit", self)
        self.action4Bit = QAction("4 Bit", self)
        self.action5Bit = QAction("5 Bit", self)
        self.action6Bit = QAction("6 Bit", self)
        self.action7Bit = QAction("7 Bit", self)
        
        self.menuBitDepth.addAction(self.action1Bit)
        self.menuBitDepth.addAction(self.action2Bit)
        self.menuBitDepth.addAction(self.action3Bit)
        self.menuBitDepth.addAction(self.action4Bit)
        self.menuBitDepth.addAction(self.action5Bit)
        self.menuBitDepth.addAction(self.action6Bit)
        self.menuBitDepth.addAction(self.action7Bit)
        # Connect actions to methods (replace with your own methods)
    
        
        # Add actions to 'View Histogram' menu
        self.menuHistogram.addAction(self.histogramInput)
        self.menuHistogram.addAction(self.histogramOutput)
        self.menuHistogram.addAction(self.histogramInputOutput)
        
        # Add 'View Histogram' menu to menubar
        self.menubar.addMenu(self.menuHistogram)
        self.menuImageProcessing = self.menubar.addMenu("Image Processing")

        # Tambahkan submenu "Histogram Equalization" ke dalam "Image Processing"
        self.actionHistogramEqualization = QAction("Histogram Equalization", self)
        self.menuImageProcessing.addAction(self.actionHistogramEqualization)

        # Tambahkan submenu "FHE RGB" ke dalam "Image Processing"
        self.actionFHERGB = QAction("FHE RGB", self)
        self.menuImageProcessing.addAction(self.actionFHERGB)

        # Tambahkan submenu "FHE Grayscale" ke dalam "Image Processing"
        self.actionFHEGrayscale = QAction("FHE Grayscale", self)
        self.menuImageProcessing.addAction(self.actionFHEGrayscale)

        # Tambahkan submenu "Filter" ke dalam "Image Processing"
        self.menuFilter = self.menuImageProcessing.addMenu("Filter")

        # Tambahkan submenu "Low Pass Filter" ke dalam "Filter"
        self.actionLowPassFilter = QAction("Low Pass Filter", self)
        self.menuFilter.addAction(self.actionLowPassFilter)

        # Tambahkan submenu "High Pass Filter" ke dalam "Filter"
        self.actionHighPassFilter = QAction("High Pass Filter", self)
        self.menuFilter.addAction(self.actionHighPassFilter)
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
        #Histogram Fungsi
        self.histogramInput.triggered.connect(self.show_histogram_input)
        self.histogramOutput.triggered.connect(self.show_histogram_output)
        self.histogramInputOutput.triggered.connect(self.show_histogram_input_output)
        self.menuHistogram.addAction("RGB Histogram Output", self.view_output_histogram_rgb)
        self.menuHistogram.addAction("RGB Histogram Input and Output", self.show_histogram_input_output_rgb)
        
        self.menuKonvolusi = self.menuBar().addMenu("Konvolusi")

        # Create the "Identity" submenu item
        self.actionIdentity = QAction("Identity", self)
        self.actionIdentity.triggered.connect(self.apply_identity_filter)
        self.menuKonvolusi.addAction(self.actionIdentity)

        # Create the "Edge Detection" submenu
        self.submenuEdgeDetection = QMenu("Edge Detection", self)

        # Create the "Sobel" submenu item
        self.actionSobel = QAction("Sobel", self)
        self.actionSobel.triggered.connect(self.apply_sobel_edge_detection)
        self.submenuEdgeDetection.addAction(self.actionSobel)

        # Create the "Prewit" submenu item
        self.actionPrewit = QAction("Prewit", self)
        self.actionPrewit.triggered.connect(self.apply_prewit_edge_detection)
        self.submenuEdgeDetection.addAction(self.actionPrewit)

        # Create the "Robert" submenu item
        self.actionRobert = QAction("Robert", self)
        self.actionRobert.triggered.connect(self.apply_robert_edge_detection)
        self.submenuEdgeDetection.addAction(self.actionRobert)

        # Add the "Edge Detection" submenu to "Konvolusi"
        self.menuKonvolusi.addMenu(self.submenuEdgeDetection)

        # Create the "Sharpen" submenu item
        self.actionSharpen = QAction("Sharpen", self)
        self.actionSharpen.triggered.connect(self.apply_sharpen_filter)
        self.menuKonvolusi.addAction(self.actionSharpen)

        # Create the "Gaussian Blur" submenu
        self.submenuGaussianBlur = QMenu("Gaussian Blur", self)

        # Create the "3 x 3" submenu item
        self.actionGaussian3x3 = QAction("3 x 3", self)
        self.actionGaussian3x3.triggered.connect(self.apply_gaussian_blur_3x3)
        self.submenuGaussianBlur.addAction(self.actionGaussian3x3)

        # Create the "5 x 5" submenu item
        self.actionGaussian5x5 = QAction("5 x 5", self)
        self.actionGaussian5x5.triggered.connect(self.apply_gaussian_blur_5x5)
        self.submenuGaussianBlur.addAction(self.actionGaussian5x5)

        # Add the "Gaussian Blur" submenu to "Konvolusi"
        self.menuKonvolusi.addMenu(self.submenuGaussianBlur)
          # Create the "Filter Gabor" submenu item
        self.menuSegmentasiCitra = self.menuBar().addMenu("Segmentasi Citra")
        self.actionFilterGabor = QAction("Filter Gabor", self)
        self.actionFilterGabor.triggered.connect(self.apply_filter_gabor)
        self.menuSegmentasiCitra.addAction(self.actionFilterGabor)

        # Create the "Fuzzy C-Means Clustering" submenu item
        self.actionFuzzyCMeans = QAction("Fuzzy C-Means Clustering", self)
        self.actionFuzzyCMeans.triggered.connect(self.apply_fuzzy_cmeans)

        # Create the "K-Means Clustering" submenu item
        self.actionKMeans = QAction("K-Means Clustering", self)
        self.actionKMeans.triggered.connect(self.apply_kmeans)

        # Create the "Ruang Warna HSV" submenu item
        self.actionHSVColorSpace = QAction("Ruang Warna HSV", self)
        self.actionHSVColorSpace.triggered.connect(self.apply_hsv_color_space)
        self.menuSegmentasiCitra.addAction(self.actionHSVColorSpace)

        # Create the "Multi Thresholding dan K-Means Clustering" submenu item
        self.actionMultiThresholdKMeans = QAction("Multi Thresholding dan K-Means Clustering", self)
        self.actionMultiThresholdKMeans.triggered.connect(self.apply_multi_threshold_kmeans)
        self.menuSegmentasiCitra.addAction(self.actionMultiThresholdKMeans)

        # Create the "Grayscale metode K-Means Clustering" submenu item
        self.actionGrayscaleKMeans = QAction("Grayscale metode K-Means Clustering", self)
        self.actionGrayscaleKMeans.triggered.connect(self.apply_grayscale_kmeans)

        # Create the "Unsharp Masking" submenu item
        self.actionUnsharpMasking = QAction("Unsharp Masking", self)
        self.actionUnsharpMasking.triggered.connect(self.apply_unsharp_masking)
        self.menuKonvolusi.addAction(self.actionUnsharpMasking)
        roi_menu = self.menubar.addMenu("ROI")
        
        # Add actions for Region Of Interest and Background Removal in the "ROI" menu
        self.actionRegionOfInterest = QAction("Region Of Interest", self)
        roi_menu.addAction(self.actionRegionOfInterest)
        
        self.actionBackgroundRemoval = QAction("Background Removal", self)
        roi_menu.addAction(self.actionBackgroundRemoval)
        # Create the "Morfologi" menu
        morfologi_menu = self.menubar.addMenu("Morfologi")

        # Add submenus for Dilasi, Erosi, Opening, and Closing in the "Morfologi" menu
        dilasi_submenu = QMenu("Dilasi", self)
        morfologi_menu.addMenu(dilasi_submenu)

        erosi_submenu = QMenu("Erosi", self)
        morfologi_menu.addMenu(erosi_submenu)

        opening_submenu = QMenu("Opening", self)
        morfologi_menu.addMenu(opening_submenu)

        closing_submenu = QMenu("Closing", self)
        morfologi_menu.addMenu(closing_submenu)

        # Add actions for Dilasi, Erosi, Opening, and Closing submenus
        square3_dilasi_action = QAction("Square 3", self)
        square3_dilasi_action.triggered.connect(lambda: self.apply_dilasi(3))
        dilasi_submenu.addAction(square3_dilasi_action)

        square5_dilasi_action = QAction("Square 5", self)
        square5_dilasi_action.triggered.connect(lambda: self.apply_dilasi(5))
        dilasi_submenu.addAction(square5_dilasi_action)

        cross3_dilasi_action = QAction("Cross 3", self)
        cross3_dilasi_action.triggered.connect(lambda: self.apply_dilasi(0))  # 0 to use the default 3x3 kernel
        dilasi_submenu.addAction(cross3_dilasi_action)

        square3_erosi_action = QAction("Square 3", self)
        square3_erosi_action.triggered.connect(lambda: self.apply_erosi(3))
        erosi_submenu.addAction(square3_erosi_action)

        square5_erosi_action = QAction("Square 5", self)
        square5_erosi_action.triggered.connect(lambda: self.apply_erosi(5))
        erosi_submenu.addAction(square5_erosi_action)

        cross3_erosi_action = QAction("Cross 3", self)
        cross3_erosi_action.triggered.connect(lambda: self.apply_erosi(0))  # 0 to use the default 3x3 kernel
        erosi_submenu.addAction(cross3_erosi_action)

        square9_opening_action = QAction("Square 9", self)
        square9_opening_action.triggered.connect(self.apply_opening)
        opening_submenu.addAction(square9_opening_action)

        square9_closing_action = QAction("Square 9", self)
        square9_closing_action.triggered.connect(self.apply_closing)
        closing_submenu.addAction(square9_closing_action)
        self.actionBrightness.triggered.connect(self.adjust_brightness)
        self.actionContrast.triggered.connect(self.adjust_contrast)
        self.actionThreshold.triggered.connect(self.apply_threshold)
        self.actionInvers.triggered.connect(self.apply_inversion)
        self.action1Bit.triggered.connect(lambda: self.apply_bit_depth(1))
        self.action2Bit.triggered.connect(lambda: self.apply_bit_depth(2))
        self.action3Bit.triggered.connect(lambda: self.apply_bit_depth(3))
        self.action4Bit.triggered.connect(lambda: self.apply_bit_depth(4))
        self.action5Bit.triggered.connect(lambda: self.apply_bit_depth(5))
        self.action6Bit.triggered.connect(lambda: self.apply_bit_depth(6))
        self.action7Bit.triggered.connect(lambda: self.apply_bit_depth(7))
        self.actionHistogramEqualization.triggered.connect(self.manual_histogram_equalization)
        self.actionFHERGB.triggered.connect(self.fuzzy_histogram_equalization_rgb)  # Connect it to the function
        self.actionFHEGrayscale.triggered.connect(self.fuzzy_histogram_equalization_grayscale)  # Connect it to the function
        self.actionLowPassFilter.triggered.connect(self.apply_low_pass_filter)  # Connect it to the function
        self.actionHighPassFilter.triggered.connect(self.apply_high_pass_filter)  # Connect it to the function

    def apply_filter_gabor(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to grayscale
            grayscale_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

            # Define the Gabor kernel
            kernel_size = 5
            theta = 0.8
            sigma = 5.0
            lambda_ = 15.0
            gamma = 0.02
            gabor_kernel = cv2.getGaborKernel((kernel_size, kernel_size), sigma, theta, lambda_, gamma, 0, ktype=cv2.CV_32F)

            # Apply Gabor filter
            filtered_image = cv2.filter2D(grayscale_image, cv2.CV_32F, gabor_kernel)

            # Normalize the output to the [0, 255] range
            filtered_image = cv2.normalize(filtered_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

            # Convert the result back to QPixmap
            q_image = QImage(filtered_image, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the filtered image in afterImageView
            self.afterImageView.setPixmap(pixmap)


    def apply_dilasi(self, kernel_size):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to grayscale
            grayscale_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

            # Define the kernel for Dilasi
            if kernel_size == 3:
                kernel = np.ones((3, 3), np.uint8)
            elif kernel_size == 5:
                kernel = np.ones((5, 5), np.uint8)
            else:  # Default to a 3x3 square kernel
                kernel = np.ones((3, 3), np.uint8)

            # Apply Dilasi operation
            dilated_image = cv2.dilate(grayscale_image, kernel, iterations=1)

            # Convert the result back to QPixmap
            q_image = QImage(dilated_image, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the processed image in afterImageView
            self.afterImageView.setPixmap(pixmap)

    def apply_erosi(self, kernel_size):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to grayscale
            grayscale_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

            # Define the kernel for Erosi
            if kernel_size == 3:
                kernel = np.ones((3, 3), np.uint8)
            elif kernel_size == 5:
                kernel = np.ones((5, 5), np.uint8)
            else:  # Default to a 3x3 square kernel
                kernel = np.ones((3, 3), np.uint8)

            # Apply Erosi operation
            eroded_image = cv2.erode(grayscale_image, kernel, iterations=1)

            # Convert the result back to QPixmap
            q_image = QImage(eroded_image, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the processed image in afterImageView
            self.afterImageView.setPixmap(pixmap)

    def apply_opening(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to grayscale
            grayscale_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

            # Define a 9x9 square kernel for Opening
            kernel = np.ones((9, 9), np.uint8)

            # Apply Opening operation
            opened_image = cv2.morphologyEx(grayscale_image, cv2.MORPH_OPEN, kernel)

            # Convert the result back to QPixmap
            q_image = QImage(opened_image, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the processed image in afterImageView
            self.afterImageView.setPixmap(pixmap)

    def apply_closing(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to grayscale
            grayscale_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

            # Define a 9x9 square kernel for Closing
            kernel = np.ones((9, 9), np.uint8)

            # Apply Closing operation
            closed_image = cv2.morphologyEx(grayscale_image, cv2.MORPH_CLOSE, kernel)

            # Convert the result back to QPixmap
            q_image = QImage(closed_image, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the processed image in afterImageView
            self.afterImageView.setPixmap(pixmap)
    def apply_fuzzy_cmeans(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to BGR
            bgr_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

            # Apply Fuzzy C-Means Clustering
            num_clusters = 3  # Adjust as needed
            max_iterations = 100
            epsilon = 0.2
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iterations, epsilon)
            pixels = bgr_image.reshape((-1, 3)).astype(np.float32)
            
            # Use cv2.kmeans to perform clustering
            _, labels, centers = cv2.kmeans(pixels, num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

            # Convert the labels back to the original image shape
            segmented_image = labels.reshape(bgr_image.shape[:2]).astype(np.uint8)

            # Convert the result back to QPixmap
            q_image = QImage(segmented_image, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the segmented image in afterImageView
            self.afterImageView.setPixmap(pixmap)
    def apply_kmeans(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to grayscale
            grayscale_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

            # Apply K-Means Clustering
            num_clusters = 3  # Adjust as needed
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
            _, labels, centers = cv2.kmeans(grayscale_image.reshape(-1, 1).astype(np.float32), num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

            # Reshape the labels to the original image shape
            segmented_image = labels.reshape(grayscale_image.shape).astype(np.uint8)

            # Convert the result back to QPixmap
            q_image = QImage(segmented_image, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the segmented image in afterImageView
            self.afterImageView.setPixmap(pixmap)

    def apply_hsv_color_space(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to BGR
            bgr_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

            # Convert BGR to HSV
            hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

            # Convert the result back to QPixmap
            q_image = QImage(hsv_image.data, width, height, width * 3, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)

            # Display the HSV image in afterImageView
            self.afterImageView.setPixmap(pixmap)

    def apply_multi_threshold_kmeans(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to grayscale
            grayscale_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

            # Apply Multi-Thresholding
            _, segmented_image = cv2.threshold(grayscale_image, 128, 255, cv2.THRESH_BINARY)

            # Apply K-Means Clustering (optional)

            # Convert the result back to QPixmap
            q_image = QImage(segmented_image, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the segmented image in afterImageView
            self.afterImageView.setPixmap(pixmap)

    def apply_grayscale_kmeans(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to grayscale
            grayscale_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

            # Apply K-Means Clustering
            num_clusters = 3  # Adjust as needed
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
            _, labels, centers = cv2.kmeans(grayscale_image.reshape(-1, 1).astype(np.float32), num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

            # Reshape the labels to the original image shape
            segmented_image = labels.reshape(grayscale_image.shape).astype(np.uint8)

            # Convert the result back to QPixmap
            q_image = QImage(segmented_image, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the segmented image in afterImageView
            self.afterImageView.setPixmap(pixmap)

    def fuzzy_histogram_equalization_grayscale(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to grayscale
            grayscale_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

            # Apply Fuzzy Histogram Equalization
            equalized_grayscale_image = self.fuzzy_histogram_equalization_grayscale_channel(grayscale_image)
            # Convert the result back to QPixmap
            q_image = QImage(equalized_grayscale_image.data, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the equalized grayscale image in afterImageView
            self.afterImageView.setPixmap(pixmap)

 
    def manual_histogram_equalization(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width = image.width()
            height = image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert to grayscale
            gray_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

            # Compute the histogram
            histogram = [0] * 256
            for row in gray_image:
                for pixel in row:
                    histogram[pixel] += 1

            # Compute the cumulative distribution function (CDF)
            cdf = [0] * 256
            cdf[0] = histogram[0]
            for i in range(1, 256):
                cdf[i] = cdf[i - 1] + histogram[i]

            # Compute the equalized image
            equalized_image = np.zeros_like(gray_image)
            total_pixels = width * height
            for i in range(256):
                equalized_value = int((cdf[i] / total_pixels) * 255)
                equalized_image[gray_image == i] = equalized_value

            # Convert the result back to QPixmap
            height, width = equalized_image.shape
            bytes_per_line = 1 * width
            q_image = QImage(equalized_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the equalized image in afterImageView
            self.afterImageView.setPixmap(pixmap)        
    def apply_bit_depth(self, n_bits):
        if self.pixmap:
            img = self.pixmap_to_numpy(self.pixmap)
            max_val = 2**n_bits - 1
            img = np.round(img * max_val / 255) * 255 / max_val
            self.update_after_image(img)

    def adjust_brightness(self):
        value, ok = QInputDialog.getInt(self, "Brightness", "Enter the brightness value:", 0, -255, 255, 1)
        if ok:
            img = self.pixmap_to_numpy(self.pixmap)
            img = self.adjust_brightness_numpy(img, value)
            self.update_after_image(img)

    def adjust_contrast(self):
        value, ok = QInputDialog.getDouble(self, "Contrast", "Enter the contrast value:", 1.0, 0.0, 10.0, 2)
        if ok:
            img = self.pixmap_to_numpy(self.pixmap)
            img = self.adjust_contrast_numpy(img, value)
            self.update_after_image(img)

    def apply_threshold(self):
        if self.pixmap:
            img = self.pixmap_to_numpy(self.pixmap)
            img = self.apply_threshold_numpy(img)
            self.update_after_image(img)

    def apply_inversion(self):
        if self.pixmap:
            img = self.pixmap_to_numpy(self.pixmap)
            img = self.apply_inversion_numpy(img)
            self.update_after_image(img)

    def adjust_brightness_numpy(self, img, value):
        return np.clip(img + value, 0, 255)

    def adjust_contrast_numpy(self, img, factor):
        return np.clip(128 + factor * (img - 128), 0, 255)

    def apply_threshold_numpy(self, img, threshold=128):
        return np.where(img < threshold, 0, 255)

    def apply_inversion_numpy(self, img):
        return 255 - img

    def pixmap_to_numpy(self, pixmap):
        image = pixmap.toImage()
        h, w = image.height(), image.width()
        array = np.zeros((h, w, 3), dtype=np.uint8)
        for x in range(w):
            for y in range(h):
                color = QColor(image.pixel(x, y))
                array[y, x] = (color.red(), color.green(), color.blue())
        return array

    def numpy_to_pixmap(self, array):
        h, w, _ = array.shape
        image = QImage(w, h, QImage.Format_RGB32)
        for x in range(w):
            for y in range(h):
                r, g, b = array[y, x]
                image.setPixel(x, y, QColor(r, g, b).rgb())
        return QPixmap.fromImage(image)

    def update_after_image(self, img):
        pixmap = self.numpy_to_pixmap(img.astype('uint8'))
        self.afterImageView.setPixmap(pixmap)


    #Histogram Fungsi   
    def view_output_histogram_rgb(self):
        if self.afterImageView.pixmap():
            img: QImage = self.afterImageView.pixmap().toImage()
            self.show_rgb_histogram(img, "RGB Histogram - Output")
    def view_input_histogram_rgb(self):
        if self.pixmap:
            img: QImage = self.pixmap.toImage()
            self.show_rgb_histogram(img, "RGB Histogram - Input")
    def show_histogram_input(self):
        if self.pixmap:
            img: QImage = self.pixmap.toImage()
            self.show_histogram(img, "Histogram - Input")

    def show_histogram_output(self):
        if self.afterImageView.pixmap():
            img: QImage = self.afterImageView.pixmap().toImage()
            self.show_histogram(img, "Histogram - Output")

    def show_histogram_input_output(self):
        if self.pixmap and self.afterImageView.pixmap():
            img_input: QImage = self.pixmap.toImage()
            img_output: QImage = self.afterImageView.pixmap().toImage()

            fig, axs = plt.subplots(1, 2, figsize=(12, 6))
            self.show_histogram(img_input, "Histogram - Input", axs[0])
            self.show_histogram(img_output, "Histogram - Output", axs[1])

            plt.show()

    def show_histogram(self, img, title, ax=None):
        if not ax:
            fig, ax = plt.subplots()

        ax.set_title(title)
        ax.set_xlabel("Pixel value")
        ax.set_ylabel("Frequency")

        # Convert QImage to numpy array
        h = img.height()
        w = img.width()
        ptr = img.bits()
        ptr.setsize(h * w * 4)
        arr = np.frombuffer(ptr, np.uint8).reshape((h, w, 4))  # Copies the data
        grey_image = np.dot(arr[...,:3], [0.2989, 0.5870, 0.1140])  # To greyscale

        n, bins, patches = ax.hist(grey_image.ravel(), bins=256, range=(0, 256), alpha=0.7)

        # Set colour using colormap
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        col = bin_centers - min(bin_centers)
        col /= max(col)

        for c, p in zip(col, patches):
            plt.setp(p, 'facecolor', cm.viridis(c))

        if not ax:
            plt.show()

    def show_rgb_histogram(self, img, title, ax=None):
        if not ax:
            fig, ax = plt.subplots()

        ax.set_title(title)
        ax.set_xlabel("Pixel value")
        ax.set_ylabel("Frequency")

        # Convert QImage to numpy array
        h = img.height()
        w = img.width()
        ptr = img.bits()
        ptr.setsize(h * w * 4)
        arr = np.frombuffer(ptr, np.uint8).reshape((h, w, 4))

        for i, color in enumerate(["Red", "Green", "Blue"]):
            channel_data = arr[..., i]
            ax.hist(channel_data.ravel(), bins=256, range=(0, 256), alpha=0.7, color=color.lower(), label=color)
        
        ax.legend()

        if not ax:
            plt.show()

    def show_histogram_input_output_rgb(self):
        if self.pixmap and self.afterImageView.pixmap():
            img_input: QImage = self.pixmap.toImage()
            img_output: QImage = self.afterImageView.pixmap().toImage()

            fig, axs = plt.subplots(1, 2, figsize=(12, 6))
            self.show_rgb_histogram(img_input, "RGB Histogram - Input", axs[0])
            self.show_rgb_histogram(img_output, "RGB Histogram - Output", axs[1])

            plt.show()

    def animate_title(self):
        titles = ["My Dark Mode App", "Welcome!", "Enjoy!", ""]
        self.setWindowTitle(titles[self.counter])
        self.counter = (self.counter + 1) % len(titles)

    def resize_images(self, event):
        size = self.size()
        # Resize the image based on the window size, or do some other adjustments.
        # This function is called every time the window is resized.


    def fuzzy_histogram_equalization_rgb(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to BGR (OpenCV format)
            bgr_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

            # Apply Fuzzy Histogram Equalization
            equalized_bgr_image = self.fuzzy_histogram_equalization_bgr(bgr_image)

            # Convert the result back to QPixmap
            q_image = QImage(equalized_bgr_image.data, width, height, width * 3, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)

            # Display the equalized RGB image in afterImageView
            self.afterImageView.setPixmap(pixmap)
    def apply_low_pass_filter(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to grayscale
            grayscale_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

            # Define a low-pass filter kernel (e.g., a simple 3x3 averaging filter)
            kernel = np.array([[1, 1, 1],
                               [1, 1, 1],
                               [1, 1, 1]]) / 9

            # Apply the low-pass filter using convolution
            filtered_image = signal.convolve2d(grayscale_image, kernel, mode='same', boundary='wrap')

            # Convert the result back to QPixmap
            q_image = QImage(filtered_image.astype(np.uint8), width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the filtered image in afterImageView
            self.afterImageView.setPixmap(pixmap)

    def apply_high_pass_filter(self):
        if hasattr(self, 'pixmap'):
            # Convert the QPixmap to a numpy array
            image = self.pixmap.toImage()
            width, height = image.width(), image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

            # Convert RGBA to grayscale
            grayscale_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

            # Define a high-pass filter kernel (e.g., Laplacian with proper scaling)
            kernel = np.array([[-1, -1, -1],
                            [-1,  8, -1],
                            [-1, -1, -1]])

            # Apply the high-pass filter using convolution
            filtered_image = signal.convolve2d(grayscale_image, kernel, mode='same', boundary='wrap')

            # Clip values to ensure they are in the valid range [0, 255]
            filtered_image = np.clip(filtered_image, 0, 255)

            # Convert the result back to QPixmap
            q_image = QImage(filtered_image.astype(np.uint8), width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Display the filtered image in afterImageView
            self.afterImageView.setPixmap(pixmap)

    def fuzzy_histogram_equalization_bgr(self, bgr_image):
        # Convert BGR image to LAB color space
        lab_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2LAB)

        # Split LAB image into L, A, and B channels
        l_channel, a_channel, b_channel = cv2.split(lab_image)

        # Apply Fuzzy Histogram Equalization to the L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        equalized_l_channel = clahe.apply(l_channel)

        # Merge equalized L channel with original A and B channels
        equalized_lab_image = cv2.merge((equalized_l_channel, a_channel, b_channel))

        # Convert LAB image back to BGR color space
        equalized_bgr_image = cv2.cvtColor(equalized_lab_image, cv2.COLOR_LAB2BGR)

        return equalized_bgr_image
    def fuzzy_histogram_equalization_grayscale_channel(self, channel):
        # Apply Fuzzy Histogram Equalization using OpenCV
        clahe = cv2.createCLAHE(clipLimit=0.03, tileGridSize=(8, 8))
        equalized_channel = clahe.apply(channel)
        return equalized_channel

    def apply_convolution(self, kernel):
            if hasattr(self, 'pixmap'):
                # Convert the QPixmap to a numpy array
                image = self.pixmap.toImage()
                width, height = image.width(), image.height()
                ptr = image.bits()
                ptr.setsize(image.byteCount())
                arr = np.array(ptr).reshape(height, width, 4)  # RGBA image

                # Convert RGBA to grayscale
                grayscale_image = cv2.cvtColor(arr, cv2.COLOR_RGBA2GRAY)

                # Apply the convolution filter using scipy's signal.convolve2d
                filtered_image = signal.convolve2d(grayscale_image, kernel, mode='same', boundary='wrap')

                # Clip values to ensure they are in the valid range [0, 255]
                filtered_image = np.clip(filtered_image, 0, 255)

                # Convert the result back to QPixmap
                q_image = QImage(filtered_image.astype(np.uint8), width, height, width, QImage.Format_Grayscale8)
                pixmap = QPixmap.fromImage(q_image)

                # Display the filtered image in afterImageView
                self.afterImageView.setPixmap(pixmap)

        # Implement functions for various convolution operations
    def apply_identity_filter(self):
        # Implement the Identity filter kernel (3x3)
        kernel = np.array([[0, 0, 0],
                           [0, 1, 0],
                           [0, 0, 0]])
        self.apply_convolution(kernel)

    def apply_sobel_edge_detection(self):
        # Implement the Sobel edge detection filter (3x3)
        kernel = np.array([[-1, 0, 1],
                           [-2, 0, 2],
                           [-1, 0, 1]])
        self.apply_convolution(kernel)

    def apply_prewit_edge_detection(self):
        # Implement the Prewitt edge detection filter (3x3)
        kernel = np.array([[-1, 0, 1],
                           [-1, 0, 1],
                           [-1, 0, 1]])
        self.apply_convolution(kernel)

    def apply_robert_edge_detection(self):
        # Implement the Robert edge detection filter (2x2)
        kernel = np.array([[1, 0],
                           [0, -1]])
        self.apply_convolution(kernel)

    def apply_sharpen_filter(self):
        # Implement a sharpening filter kernel (3x3)
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        self.apply_convolution(kernel)

    def apply_gaussian_blur_3x3(self):
        # Implement a 3x3 Gaussian blur filter kernel
        kernel = (1/16) * np.array([[1, 2, 1],
                                    [2, 4, 2],
                                    [1, 2, 1]])
        self.apply_convolution(kernel)

    def apply_gaussian_blur_5x5(self):
        # Implement a 5x5 Gaussian blur filter kernel
        kernel = (1/256) * np.array([[1, 4, 6, 4, 1],
                                     [4, 16, 24, 16, 4],
                                     [6, 24, 36, 24, 6],
                                     [4, 16, 24, 16, 4],
                                     [1, 4, 6, 4, 1]])
        self.apply_convolution(kernel)

    def apply_unsharp_masking(self):
        # Implement unsharp masking filter (3x3)
        kernel = np.array([[-1, -1, -1],
                           [-1,  9, -1],
                           [-1, -1, -1]])
        self.apply_convolution(kernel)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
