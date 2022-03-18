# utils-for-img-process
本仓具用于收藏我在写代码期间使用到的图片处理工具类，你可以使用该脚本在外部生成用于训练的经过处理的数据

## crop_img.py
`默认要crop的图片的尺寸都一致`
本例中的数据文件夹结构为：
    data --|
           A
           B
         label
`子文件夹的数量可以和我不一样，代码会自动处理`
```python
# ============ config =============
CROP = (256, 256)         # 裁剪的大小 对应 h, w
DIR_NAME = 'val-ori'      # 原数据存放的文件夹名称
NEW_DIR_NAME = 'val'
CROP_NUM_EACH_PIC = 5     # 每张图片上随机裁剪多少张图片
THREAD = 10               # 启用多线程划分数据, 线程数
```
