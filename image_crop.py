# -*- coding:utf-8 -*-
import os
from PIL import Image
import matplotlib.pyplot as plt
import datetime


infor = {395: 91, 430: 93, 465: 95, 500: 92, 535: 93,
         570: 103, 605: 92, 710: 92, 850: 92}


def crop(image_read_dir, image_save_dir):
    img = Image.open(image_read_dir)  # 打开图像
    size = img.size
    if size[0] == 1200:
        if size[1] in infor.keys():
            box = (0, 0, size[0]/2, infor[size[1]])
            roi = img.crop(box)
            plt.imsave(image_save_dir, roi)
        else:
            box = (0, 0, size[0] / 2, 80)
            roi = img.crop(box)
            plt.imsave(image_save_dir, roi)
    else:
        box = (0, 0, size[0] / 2, 80)
        roi = img.crop(box)
        plt.imsave(image_save_dir, roi)


def main(image_read_dir, image_save_dir):
    # image_read_dir = 'C:\MyFile\Coding\Python\Rjb\Pictures'
    # image_save_dir = 'C:\MyFile\Coding\Python\Rjb\Image_crop2'
    for root, dirs, files in os.walk(image_read_dir):
        for file in files:
            names = os.path.splitext(file)
            if names[1] == '.png' or names[1] == '.jpg':
                crop(os.path.join(image_read_dir, file), os.path.join(image_save_dir, file))
        break


if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print(end-start)
