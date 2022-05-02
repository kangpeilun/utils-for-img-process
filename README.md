# utils-for-img-process
`本仓库会不断更新，只要我还在Coding`

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
```

## draw_data.py
`像素级分类，按照每个像素的类别对背景图像进行上色`

**需要注意的是，预测数据集的像素坐标 和 PIL生成的像素的坐标可能是对称的，如果出现这个问题你需要做一些改变。
比如预测像素的坐标为(x1, y1), 若出现像素坐标对称的问题，则在draw.point中坐标修改为(y1, x1)，即可生成正确的图像**

本例中的数据输入方式按照 __main__中给出的示例进行输入

每个函数的作用都有相应注释
```python
positions = [
    [x1,y1],
    [x2,y2],
    ...
]   # 原像素的坐标位置

predictions = [class_id1, class_id2, ...]   # 预测类别的标签
```
效果图

![Indian](https://user-images.githubusercontent.com/57496061/166199733-6799364e-c89f-43e3-bae2-e42e74ceb9d4.png)
