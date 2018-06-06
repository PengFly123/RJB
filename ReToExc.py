# -*- coding:utf-8 -*-
import os
import xlwt


def main(text_dir, save_name):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建一个Excel对象
    sheet = book.add_sheet('sheet', cell_overwrite_ok=True)
    sheet.write(0, 1, '企 业 注 册 号'.replace(' ', ''))
    sheet.write(0, 0, '企 业 名 称'.replace(' ', ''))
    i = 1
    for roots, dirs, files in os.walk(text_dir):
        for file in files:
            with open(os.path.join(text_dir, file), 'rb') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.decode('utf-8')
                    if '号 :' in line:
                        sheet.write(i, 1, line[line.index(':') + 2:len(line)].replace(' ', ''))
                    elif '称 :' in line:
                        sheet.write(i, 0, line[line.index(':') + 2:len(line)].replace(' ', ''))
                        break
                i += 1
        break
    book.save(save_name)
