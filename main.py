# -*- coding:utf-8 -*-

import datetime
import image_crop
import Process
import ReToExc

image_read_dir = r'C:\MyFile\Coding\Python\Rjb\Pictures'            # 测试图片的路径
image_save_dir = r'C:\MyFile\Coding\Python\Rjb\Image_crop2'          # 裁剪图片的路径
text_dir = r'C:\MyFile\Coding\Python\Rjb\information2'               # 提取的文字保存的路径
save_name = 'test.xls'                                              # Excel表保存的文件名
if __name__ == '__main__':
    begin = datetime.datetime.now()
    image_crop.main(image_read_dir, image_save_dir)
    Process.text_extraction(image_save_dir, text_dir)
    ReToExc.main(text_dir, save_name)
    print(datetime.datetime.now()-begin)
