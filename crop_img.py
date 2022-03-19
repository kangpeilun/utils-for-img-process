# -*- coding: utf-8 -*-
# date: 2022/3/15
# Project: BovwSfaCD-pytorch
# File Name: process.py
# Description: 把val数据处理成需要的形状 (256, 256)
# Author: Anefuer_kpl
# Email: 374774222@qq.com

import os
from os.path import join
import PIL
from PIL import Image
import random
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


# ============ config =============
IF_RESIZE = True          # 裁剪前是否对图像进行resize
RESIZE = 286
CROP = (256, 256)         # 裁剪的大小 对应 h, w
DIR_NAME = 'test-ori'      # 原数据存放的文件夹名称
NEW_DIR_NAME = 'test'
CROP_NUM_EACH_PIC = 5     # 每张图片上随机裁剪多少张图片

SEED = 0                  # 随机种子，使得每次划分结果都一致
THREAD = 10               # 启用多线程划分数据, 线程数

random.seed(SEED)
# ============ config =============
DATA_DIR = join(os.path.dirname(os.path.realpath(__file__)), DIR_NAME)   # 获取 原始 数据存放文件夹完整路径
NEW_DIR = join(os.path.dirname(os.path.realpath(__file__)), NEW_DIR_NAME)   # 获取 新生成 数据存放文件夹完整路径


def get_img_size():
    '''获取待裁剪图片的尺寸，默认所有图片的尺寸大小都一致'''
    sub_dir = join(DATA_DIR, os.listdir(DATA_DIR)[0])   # 获取原数据文件夹第一个子文件夹
    img_file = join(sub_dir, os.listdir(sub_dir)[0])    # 获取 第一个文件
    img = Image.open(img_file)

    return img.size[0], img.size[1]


def check_dir(dir):
    '''检查文件夹是否存在，并创建不存在的文件夹'''
    if not os.path.exists(dir):
        os.mkdir(dir)


def make_dirs():
    '''
    保持新数据文件夹结构与原数据文件夹结构一致
    Args: 以我的数据文件为例，子文件夹的数量可以和我不一样，代码会自动处理
        DATA_DIR: 原数据存放文件夹结构
                data --|
                       A
                       B
                     label
        NEW_DIR: 新数据存放文件夹
            data-new --|
                       A
                       B
                     label
    Returns: 返回新数据 子文件夹 路径
    '''
    check_dir(NEW_DIR)  # 创建新数据文件夹
    ori_list_dir = [join(DATA_DIR, dir_name) for dir_name in os.listdir(DATA_DIR)]   # 获取原数据子文件夹完整路径
    new_dir_list = []  # 获取新数据子文件夹完整路径
    for dir in os.listdir(DATA_DIR):
        dir_sub = join(NEW_DIR, dir)  # 子文件夹完整路径
        new_dir_list.append(dir_sub)
        check_dir(dir_sub)  # 获取原始数据文件夹所有的 文件夹，并在新数据目录创建对应的文件夹

    return ori_list_dir, new_dir_list


def crop_one_img(file_path, save_path, crop_area):
    img = Image.open(file_path)
    if IF_RESIZE:   # 缩放
        img = img.resize((RESIZE, RESIZE), Image.BILINEAR)

    img = img.crop(crop_area)   # 获取裁剪后的图片
    img.save(save_path)


def process_data():
    ori_list_dir, new_dir_list = make_dirs()  # 获取新 原数据子文件夹完整路径
    h, w = get_img_size()   # 获取图片尺寸
    bar = tqdm(range(1, CROP_NUM_EACH_PIC+1), total=CROP_NUM_EACH_PIC, ascii=True)
    for crop_num in bar:
        if IF_RESIZE:
            h, w = RESIZE, RESIZE       # 启用resize，修改图片的高 宽
        crop_range_h, crop_range_w = h - CROP[0], w - CROP[1]  # 获取可以进行裁剪的区域,防止裁剪时越界
        x, y = random.randint(0, crop_range_h), random.randint(0, crop_range_w)  # 产生随机左上角裁剪坐标点
        crop_area = (x, y, x + CROP[0], y + CROP[1])  # 获取被裁减区域坐标

        bar.set_description('{}\tCrop_size:{}\tCrop_area:{}'.format(NEW_DIR, CROP, crop_area))

        for idx, (ori_dir_path, new_dir_path) in enumerate(zip(ori_list_dir, new_dir_list)):  # 一组一组的数据文件夹进行裁剪
            '''所有的子文件夹中的数据都在 相同的 crop_area 中被裁剪一次，总共重复CROP_NUM_EACH_PIC次
                exa: A_ori--|      A_new
                       xxx.png
                       xxx.png
            '''
            with ThreadPoolExecutor(THREAD) as t:
                for file in os.listdir(ori_dir_path):
                    file_path = join(ori_dir_path, file)  # 原数据文件路径
                    save_path = join(new_dir_path, file.rsplit('.')[0]+f'_{crop_num}.png')
                    t.submit(crop_one_img, file_path=file_path, save_path=save_path, crop_area=crop_area)
                    # img = Image.open(file_path)
                    # cropImg = img.crop(crop_area)   # 获取裁剪后的图片
                    # cropImg.save(join(new_dir_path, file.rsplit('.')[0]+f'_{crop_num}.png'))



if __name__ == '__main__':
    process_data()
