import numpy as np
import pandas as pd


def get_entropy(data_df, columns=None):
    """pandas"""
    if (columns is None) and (data_df.shape[1] > 1):
        raise Exception("the dim of data_df more than 1, the columns must be not empty!")
        # 信息值
    pe_value_array = data_df[columns].unique()
    ent = 0.0
    for x_value in pe_value_array:
        p = float(data_df[data_df[columns] == x_value].shape[0]) / data_df.shape[0]
        logp = np.log2(p)
        ent -= p * logp

    return ent


from math import log


def calcShannonEnt(dataSet):
    numEntries = len(dataSet)   # 样本数

    # 该数据集每个类别的频数
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0

    # 计算
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt
