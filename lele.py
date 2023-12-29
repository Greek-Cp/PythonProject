import cv2
import numpy as np

# Membaca gambar dari disk
image = cv2.imread('kolam_lele.jpg')

# Mengubah gambar menjadi grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Menggunakan GaussianBlur untuk mengurangi noise dan memudahkan thresholding
blurred = cv2.GaussianBlur(gray, (15, 15), 0)

# Thresholding
_, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)

# Mencari kontur pada gambar threshold
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter kontur berdasarkan luas area untuk menghilangkan noise
fish_contours = [c for c in contours if cv2.contourArea(c) > 500]

# Menghitung jumlah ikan berdasarkan jumlah kontur yang tersisa
num_fish = len(fish_contours)

# Mencetak jumlah ikan
print(f"Jumlah ikan: {num_fish}")

# Untuk visualisasi
cv2.drawContours(image, fish_contours, -1, (0, 255, 0), 2)  # Menggambar kontur dengan warna hijau
cv2.imshow('Detected Fish', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
