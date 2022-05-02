from PIL import Image, ImageColor, ImageDraw
import os

def check_dir(dir_path):
    '''检测路径是否存在，并创建对应文件夹'''
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

def colors_per_class(data='Indian'):
    '''
    保存不同数据集每种类别的颜色
    :param data: ['Indian', 'Pavia', 'Houston'] 换成你自己的数据集名称
    :return:
    '''
    # colors 记录每种数据集 不同类别的颜色表，索引[0]是类别名，索引[1]是十六进制颜色值
    if data == 'Indian':
        colors = {
            1: ['CornNotill', '#53ab48'],
            2: ['CornMintill', '#89ba43'],
            3: ['Corn', '#42845b'],
            4: ['GrassPature', '#3c8345'],
            5: ['GrassTrees', '#905236'],
            6: ['HayWindrow', '#69bcc8'],
            7: ['SoybeanNotill', '#ffffff'],
            8: ['SoybeanMintill', '#c7b0c9'],
            9: ['SoybeanClean', '#da332c'],
            10: ['Wheat', '#772324'],
            11: ['Woods', '#57585a'],
            12: ['BuilGraTrDri', '#e0db54'],
            13: ['StoSteTower', '#d98e34'],
            14: ['Alfalfa', '#54307e'],
            15: ['GrassPastMow', '#e3775b'],
            16: ['Oats', '#9d5796'],
        }
    elif data == 'Pavia':
        colors = {
            1: ['Asphalt', '#c7c9cb'],
            2: ['Meadows', '#6eb145'],
            3: ['Gravel', '#69bcc8'],
            4: ['Trees', '#3a7a42'],
            5: ['Metal Sheets', '#9d5796'],
            6: ['Bare Soil', '#945331'],
            7: ['Bitumen', '#752d79'],
            8: ['Bricks', '#da332c'],
            9: ['Shadows', '#e0db54'],
        }
    elif data == 'Houston':
        colors = {
            1: ['Healthy Grass', '#50ac48'],
            2: ['Stressed Grass', '#89bb43'],
            3: ['Synthetic Grass', '#3d855c'],
            4: ['Trees', '#368545'],
            5: ['Soil', '#915135'],
            6: ['Water', '#65bdc8'],
            7: ['Residential', '#ffffff'],
            8: ['Commercial', '#c7b0cb'],
            9: ['Road', '#db2f2b'],
            10: ['Highway', '#792223'],
            11: ['Railway', '#3265a7'],
            12: ['Parkinig Lot1', '#e0dd53'],
            13: ['Parkinig Lot2', '#db8e34'],
            14: ['Tennis Court', '#542f7d'],
            15: ['Running Track', '#e5775a'],
        }

    return colors


def create_image(data='Indian'):
    '''根据不同数据集创建不同尺寸的图像'''
    if data == 'Indian':
        w, h = 145, 145     # 图像尺寸
    elif data == 'Pavia':
        w, h = 610, 340
    elif data == 'Houston':
        w, h = 349, 1905

    image = Image.new('RGB', (w, h), (0,0,0))     # 创建黑色背景图
    return image


def draw_data(positions, predicts, data='Indian'):
    '''
    绘制不同数据集的预测类别颜色图
    :param predictions:
    :param data:
    :return:
    '''
    colors = colors_per_class(data)     # 获取颜色表
    image = create_image(data)          # 创建黑色背景颜色图
    draw = ImageDraw.Draw(image)
    '''
    ImageColor模块使用方法见以下连接
    https://www.jianshu.com/p/f63dc8b5445d?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation
    ImageColor.getrgb() 将十六进制颜色值转换为 RGB值
    '''
    for pos, pre in zip(positions, predicts):
        draw.point(pos, fill=ImageColor.getrgb(colors[pre][1]))     # 在对应索引位置处的像素上色

    check_dir(f'predict')
    image.save(os.path.join(f'predict/{data}.png'))
    image.show(title=f"{data}'s predict result")


if __name__ == '__main__':
    # 输入示例
    pos = [[1,3], [4,5], [6,6]]
    pre = [1,3,5]
    draw_data(pos, pre, data='Indian')
