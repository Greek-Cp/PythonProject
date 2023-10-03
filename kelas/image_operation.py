from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap

class ImageOperations:
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
