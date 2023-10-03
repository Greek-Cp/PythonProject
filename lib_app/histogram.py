import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
class Histogram:
    @staticmethod
    def view_output_histogram_rgb(image):
        if image:
            Histogram.show_rgb_histogram(image, "RGB Histogram - Output")

    @staticmethod
    def view_input_histogram_rgb(image):
        if image:
            Histogram.show_rgb_histogram(image, "RGB Histogram - Input")

    @staticmethod
    def show_histogram_input(image):
        if image:
            Histogram.show_histogram(image, "Histogram - Input")

    @staticmethod
    def show_histogram_output(image):
        if image:
            Histogram.show_histogram(image, "Histogram - Output")

    @staticmethod
    def show_histogram_input_output(input_image, output_image):
        if input_image and output_image:
            fig, axs = plt.subplots(1, 2, figsize=(12, 6))
            Histogram.show_histogram(input_image, "Histogram - Input", axs[0])
            Histogram.show_histogram(output_image, "Histogram - Output", axs[1])

            plt.show()

    @staticmethod
    def show_histogram(image, title, ax=None):
        if not ax:
            fig, ax = plt.subplots()

        ax.set_title(title)
        ax.set_xlabel("Pixel value")
        ax.set_ylabel("Frequency")

        # Convert QImage to numpy array
        h = image.height()
        w = image.width()
        ptr = image.bits()
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

    @staticmethod
    def show_rgb_histogram(image, title, ax=None):
        if not ax:
            fig, ax = plt.subplots()

        ax.set_title(title)
        ax.set_xlabel("Pixel value")
        ax.set_ylabel("Frequency")

        # Convert QImage to numpy array
        h = image.height()
        w = image.width()
        ptr = image.bits()
        ptr.setsize(h * w * 4)
        arr = np.frombuffer(ptr, np.uint8).reshape((h, w, 4))

        for i, color in enumerate(["Red", "Green", "Blue"]):
            channel_data = arr[..., i]
            ax.hist(channel_data.ravel(), bins=256, range=(0, 256), alpha=0.7, color=color.lower(), label=color)
        
        ax.legend()

        if not ax:
            plt.show()

    @staticmethod
    def show_histogram_input_output_rgb(input_image, output_image):
        if input_image and output_image:
            fig, axs = plt.subplots(1, 2, figsize=(12, 6))
            Histogram.show_rgb_histogram(input_image, "RGB Histogram - Input", axs[0])
            Histogram.show_rgb_histogram(output_image, "RGB Histogram - Output", axs[1])

            plt.show()

