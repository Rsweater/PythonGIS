"""
time: 2020-03-28
coder: 一线毛衣
purpose：To familiarize yourself with the gdal library.
documents:
知乎专栏：https://zhuanlan.zhihu.com/p/126130709/
个人博客：https://bwchen1223.xyz/2020/03/29/01-multiband_image_synthesis/

reference:
landsat 8常用合成：
Natural color(432)：真彩色。接近地物真实色彩，图像平淡，色调灰暗
Land/Water(564): 陆地/水体。 红外波段与红色波段合成，水体边界清晰，利于海岸识别；植被有较好的显示，但不便于区分拘役植被类别
Color Infrared (vegetation, 543): 红外彩色，又称标准假彩色。地物色彩鲜明，有利于植被（红色）分类，水体

"""

import os
from osgeo import gdal


def get_dataset_band(bandfile):
    """获取dataset并获取dataset的一个band"""
    input_dataset = gdal.Open(bandfile)
    input_band = input_dataset.GetRasterBand(1)

    return [input_dataset, input_band]


def main():
    # 1. 定义默认路径并导入文件
    os.chdir(r'F:\PythonProjection\PythonGIS\Python_GDAL\LC81660522019274LGN00')
    bandfile_1 = 'LC08_L1TP_166052_20191001_20191001_01_RT_B4.TIF'
    bandfile_2 = 'LC08_L1TP_166052_20191001_20191001_01_RT_B3.TIF'
    bandfile_3 = 'LC08_L1TP_166052_20191001_20191001_01_RT_B2.TIF'
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


if __name__ == '__main__':
    main()
