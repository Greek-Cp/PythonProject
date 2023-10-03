from PyQt5.QtWidgets import QFileDialog ,QApplication
from PyQt5.QtGui import QPixmap


class FileUtil:
    @staticmethod
    def open_image(ui_instance):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(ui_instance, "Open Image", "", "Images (*.png *.jpg *.jpeg)", options=options)
        if filepath:
            ui_instance.pixmap = QPixmap(filepath)
            ui_instance.beforeImageView.setPixmap(ui_instance.pixmap)
            

    @staticmethod
    def save_image(ui_instance):
        filepath, _ = QFileDialog.getSaveFileName(ui_instance, "Save Image", "", "PNG (*.png);;JPEG (*.jpg *.jpeg);;All Files (*)")
        if filepath:
            pixmap = ui_instance.afterImageView.pixmap()
            if pixmap:
                pixmap.save(filepath)

            
    @staticmethod
    def exit_application(ui_instance=None):
        QApplication.quit()
