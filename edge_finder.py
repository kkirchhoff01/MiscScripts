import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt
import os

class EdgeFinder:
    def __init__(self, folder):
        self.img_path = folder

    def list_files(self):
        for f in os.listdir(self.img_path):
            print(f)

    def get_file(self):
        self.list_files()
        img_file = os.path.join(self.img_path, raw_input('Enter file name: '))

        while not os.path.isfile(img_file):
            print('That is not a file')
            img_file = os.path.join(self.img_path, raw_input('Enter file name: '))

        return img_file

    def find_edge(self, img_file, lt=50, rt=150):
        img = cv2.imread(img_file, 0)
        edged_img = cv2.Canny(img, lt, rt)
        return edged_img

    def plot_image(self, edged_img):
        plt.imshow(edged_img, cmap = matplotlib.cm.Greys_r)
        plt.show()

if __name__ == "__main__":
    edge_finder = EdgeFinder('/home/kevin/Pictures')
    fname = edge_finder.get_file()
    img = edge_finder.find_edge(fname)
    edge_finder.plot_image(img)
