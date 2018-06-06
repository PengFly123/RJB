# -*- coding:utf-8 -*-
import cv2
import os
import datetime
from PIL import Image


class WatermarkRemover(object):
    """"
    去除图片中的水印(Remove Watermark)
    """
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.watermark_template_gray_img = None
        self.watermark_template_mask_img = None
        self.watermark_template_h = 0
        self.watermark_template_w = 0
        self.watermark_start_x = 0
        self.watermark_start_y = 0

    def load_watermark_template(self, watermark_template_filename):
        """
        加载水印模板，以便后面批量处理去除水印
        :param watermark_template_filename:
        :return:
        """
        self.generate_template_gray_and_mask(watermark_template_filename)

    def generate_template_gray_and_mask(self, watermark_template_filename):
        """
        处理水印模板，生成对应的检索位图和掩码位图
        检索位图
            即处理后的灰度图，去除了非文字部分

        :param watermark_template_filename: 水印模板图片文件名称
        :return: x1, y1, x2, y2
        """

        # 水印模板原图
        img = cv2.imread(watermark_template_filename)

        # 灰度图、掩码图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

        # 后面修图时需要用到三个通道
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        self.watermark_template_gray_img = gray
        self.watermark_template_mask_img = mask

        self.watermark_template_h = img.shape[0]
        self.watermark_template_w = img.shape[1]

        # cv2.imwrite('watermark-template-gray.jpg', gray)
        # cv2.imwrite('watermark-template-mask.jpg', mask)

        return gray, mask

    def find_watermark(self, filename):
        """
        从原图中寻找水印位置
        :param filename:
        :return: x1, y1, x2, y2
        """
        # Load the images in gray scale
        gray_img = cv2.imread(filename, 0)
        return self.find_watermark_from_gray(gray_img, self.watermark_template_gray_img)

    def find_watermark_from_gray(self, gray_img, watermark_template_gray_img):
        """
        从原图的灰度图中寻找水印位置
        :param gray_img: 原图的灰度图
        :param watermark_template_gray_img: 水印模板的灰度图
        :return: x1, y1, x2, y2
        """
        # Load the images in gray scale

        method = cv2.TM_CCOEFF
        # Apply template Matching
        res = cv2.matchTemplate(gray_img, watermark_template_gray_img, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            x, y = min_loc
        else:
            x, y = max_loc

        return x, y, x + self.watermark_template_w, y + self.watermark_template_h

    def remove_watermark_raw(self, img, watermark_template_gray_img, watermark_template_mask_img):
        """
        去除图片中的水印
        :param img: 待去除水印图片位图
        :param watermark_template_gray_img: 水印模板的灰度图片位图，用于确定水印位置
        :param watermark_template_mask_img: 水印模板的掩码图片位图，用于修复原始图片
        :return: 去除水印后的图片位图
        """
        # 寻找水印位置
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        x1, y1, x2, y2 = self.find_watermark_from_gray(img_gray, watermark_template_gray_img)
        self.watermark_start_x = x1
        self.watermark_start_y = y1
        # 制作原图的水印位置遮板
        # mask = np.zeros(img.shape, np.uint8)
        # watermark_template_mask_img = cv2.cvtColor(watermark_template_gray_img, cv2.COLOR_GRAY2BGR)
        # mask[y1:y1 + self.watermark_template_h, x1:x1 + self.watermark_template_w] = watermark_template_mask_img
        return watermark_template_mask_img

    def remove_watermark(self, filename, output_filename=None):
        """
        去除图片中的水印
        :param filename: 待去除水印图片文件名称
        :param output_filename: 去除水印图片后的输出文件名称
        :return: 去除水印后的图片位图
        """

        # 读取原图
        img = cv2.imread(filename)

        dst = self.remove_watermark_raw(img,
                                        self.watermark_template_gray_img,
                                        self.watermark_template_mask_img
                                        )
        if output_filename is not None:
            cv2.imwrite(output_filename, dst)
        return dst


def main():
    image_dir = r'C:\MyFile\Coding\Python\Rjb\image_crop2'  # 识别图片的路径
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            infor = os.path.splitext(file)  # 分离文件名与扩展名，返回一个元组
            if infor[1] == '.png' or infor[1] == '.jpg':
                watermark_template_filename = os.path.join(image_dir, file)
                im = Image.open(watermark_template_filename)
                x, y = im.size
                try:
                    p = Image.new('RGBA', im.size, (255, 255, 255))
                    p.paste(im, (0, 0, x, y), im)           # 填充背景色
                    p.save(watermark_template_filename)
                    remover = WatermarkRemover()
                    remover.load_watermark_template(watermark_template_filename)
                    remover.remove_watermark(watermark_template_filename, watermark_template_filename)

                except:
                    continue
        break


if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print(end-start)
