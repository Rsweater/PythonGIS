import os
import cv2
import numpy as np

os.chdir(r'F:\地城专业学习资料\大二上\遥感\ENVI\2016ENVI入门学习素材包-数据预处理\08.图像融合\数据\TM与spot')


def main():
    # 导入融合图像
    # src_matrix = cv2.imread('gs_sharpen.dat')
    src_matrix = np.array([[0, 0, 1, 1],
                           [0, 0, 1, 1],
                           [0, 2, 2, 2],
                           [2, 2, 3, 3]], dtype=np.uint8)

    # 设置权重
    xiejiao = 1 / 2 ** 0.5
    sizhou = 1.0

    kernel = np.array([[xiejiao, sizhou, xiejiao],
                       [sizhou,      -8, sizhou],
                       [xiejiao, sizhou, xiejiao]])
    dst_matrix = cv2.filter2D(src_matrix, -1, kernel)

    EVA_index = np.mean(dst_matrix)
    print("点锐度EVA值：{}".format(EVA_index))


if __name__ == '__main__':
    main()
