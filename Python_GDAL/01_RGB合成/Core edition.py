"""
time: 2020-03-28
coder: 一线毛衣
purpose：To familiarize yourself with the gdal library.

reference:
landsat 8常用合成：
Natural color(432)：真彩色。接近地物真实色彩，图像平淡，色调灰暗
Land/Water(564): 陆地/水体。 红外波段与红色波段合成，水体边界清晰，利于海岸识别；植被有较好的显示，但不便于区分拘役植被类别
Color Infrared (vegetation, 543): 红外彩色，又称标准假彩色。地物色彩鲜明，有利于植被（红色）分类，水体

"""

import sys
import cv2
from osgeo import gdal


def get_dataset_band(bandfile):
    """获取dataset并获取dataset的一个band"""
    input_dataset = gdal.Open(bandfile)
    if input_dataset is None:
        print('could not open')
        # sys.exit(0)    无错误退出
        # sys.exit(1)    有错误退出
        sys.exit(1)
    input_band = input_dataset.GetRasterBand(1)

    return [input_dataset, input_band]


def show_img():
    """
    图形展示


    读取图像，支持 bmp、jpg、png、tiff 等常用格式

    nameWindow第2个参数:
    WINDOW_NORMAL窗口可以被随意拖动改变大小;
    WINDOW_AUTOSIZE 窗口大小等于图片大小, 不可以被拖动改变大小。
    """

    img = cv2.imread("natural_color.tif", -1)
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", img)

    # 等待键盘输入，有输入才继续执行
    cv2.waitKey()
    print("按任意键退出！")

    # 销毁窗口，释放资源
    cv2.destroyAllWindows()


def main():
    # 1. 导入文件
    print("{:-^13}".format('run'))
    print("请依次输入RGB通道对应波段图像对应路径：")
    bandfile_1 = input("R:")
    bandfile_2 = input("G:")
    bandfile_3 = input("B:")
    bandfile = [bandfile_1, bandfile_2, bandfile_3]

    # 2. 读取dataset并获取band值
    inputdata = []
    for i in range(3):
        inputdata.append(get_dataset_band(bandfile[i]))
    inputdataset_1, inputband_1 = inputdata[0]

    # 3. 创建dataset（要输出的dataset）
    file_driver = gdal.GetDriverByName('Gtiff')
    output_dataset = file_driver.Create(
        'natural_color.tif', inputband_1.XSize, inputband_1.YSize, 3, inputband_1.DataType
    )
    output_dataset.SetProjection(inputdataset_1.GetProjection())
    output_dataset.SetGeoTransform(inputdataset_1.GetGeoTransform())

    # 4. 写入数据
    for i in range(3):
        inputband_data = inputdata[i][1].ReadAsArray()
        output_dataset.GetRasterBand(i + 1).WriteArray(inputband_data)

    # 5. 后续处理
    output_dataset.FlushCache()  # 刷新缓存，确保数据写入硬盘
    output_dataset.BuildOverviews('average', [2, 4, 8, 16, 32])  # 建立快速显示金字塔

    # 6. Add_展示
    control = input('请输入 "Y"or"N" 选择是否直接展示结果：')
    if control == "Y" or control == "y":
        show_img()
    else:
        print('done!')
        sys.exit(0)


if __name__ == '__main__':
    main()
