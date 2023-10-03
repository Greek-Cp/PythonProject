from PyQt5.QtGui import QImage, QPixmap, QPainter, QTransform
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog

class GeometryOperation:
    
    @staticmethod
    def scaling_uniform(pixmap, afterImageView):
        if pixmap:
            img: QImage = pixmap.toImage()
            width, ok = QInputDialog.getInt(None, 'Input', 'Enter the width:', min=1, max=5000)
            if ok:
                height = int(width * img.height() / img.width())
                scaled_img = img.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                afterImageView.setPixmap(QPixmap.fromImage(scaled_img))

    @staticmethod
    def scaling_non_uniform(pixmap, afterImageView):
        if pixmap:
            img: QImage = pixmap.toImage()
            width, ok1 = QInputDialog.getInt(None, 'Input', 'Enter the width:', min=1, max=5000)
            height, ok2 = QInputDialog.getInt(None, 'Input', 'Enter the height:', min=1, max=5000)
            if ok1 and ok2:
                scaled_img = img.scaled(width, height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                afterImageView.setPixmap(QPixmap.fromImage(scaled_img))

    @staticmethod
    def rotate_image(pixmap, afterImageView):
        if pixmap:
            angle, ok = QInputDialog.getDouble(None, "Rotate", "Enter rotation angle:", 0, -360, 360, 2)
            if ok:
                transform = QTransform().rotate(angle)
                rotated_pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
                afterImageView.setPixmap(rotated_pixmap)

    @staticmethod
    def flip_horizontal(pixmap, afterImageView):
        if pixmap:
            img: QImage = pixmap.toImage()
            flipped_img = img.mirrored(True, False)
            afterImageView.setPixmap(QPixmap.fromImage(flipped_img))

    @staticmethod
    def flip_vertical(pixmap, afterImageView):
        if pixmap:
            img: QImage = pixmap.toImage()
            flipped_img = img.mirrored(False, True)
            afterImageView.setPixmap(QPixmap.fromImage(flipped_img))

    @staticmethod
    def custom_flip(pixmap, afterImageView):
        if pixmap:
            img: QImage = pixmap.toImage()
            flipped_img = img.mirrored(True, True)
            afterImageView.setPixmap(QPixmap.fromImage(flipped_img))

    @staticmethod
    def translate_image(pixmap, afterImageView, dx, dy):
        if pixmap:
            img: QImage = pixmap.toImage()
            new_img = QImage(img.width(), img.height(), QImage.Format_ARGB32)
            new_img.fill(Qt.transparent)
            
            painter = QPainter(new_img)
            painter.drawImage(dx, dy, img)
            painter.end()

            afterImageView.setPixmap(QPixmap.fromImage(new_img))

    @staticmethod
    def action_left(pixmap, afterImageView):
        GeometryOperation.translate_image(pixmap, afterImageView, -20, 0)

    @staticmethod
    def action_right(pixmap, afterImageView):
        GeometryOperation.translate_image(pixmap, afterImageView, 20, 0)

    @staticmethod
    def action_top(pixmap, afterImageView):
        GeometryOperation.translate_image(pixmap, afterImageView, 0, -20)

    @staticmethod
    def action_bottom(pixmap, afterImageView):
        GeometryOperation.translate_image(pixmap, afterImageView, 0, 20)
