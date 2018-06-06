from multiprocessing import Process, Pool
import os
from PIL import Image
import pytesseract



def get_image_name(image_dir):
    image = []
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            names = os.path.splitext(file)                      # 分离文件名与扩展名，返回一个元组
            if names[1] == '.png' or names[1] == '.jpg':
                image.append(file)
    return image


def main(i, image, image_dir, text_dir):
    text = pytesseract.image_to_string(Image.open(os.path.join(image_dir, image[i])), lang='chi_sim')
    # lang = 'chi_sim' 参数表示提取中文
    with open(os.path.join(text_dir, os.path.splitext(image[i])[0] + '.txt'), 'wb') as f:
        f.write(text.encode('utf-8'))  # 写入文件前要将字符串转码


def text_extraction(image_dir, text_dir):
    image = get_image_name(image_dir)
    p = Pool(4)
    for i in range(50):
        p.apply_async(main, args=(i, image, image_dir, text_dir))
    p.close()
    p.join()
