import re
import numpy as np
import math


def compute_similarity(vector_1, vector_2):
    vector_1 = np.array(vector_1)
    vector_2 = np.array(vector_2)

    # 向量归一化
    len_1 = np.sqrt(np.dot(vector_1, vector_1))  # 向量长度
    unit_vector_1 = vector_1 / len_1  # 单位化

    len_2 = np.sqrt(np.dot(vector_2, vector_2))  # 向量长度
    unit_vector_2 = vector_2 / len_2  # 单位化

    print('unit_vector:', unit_vector_1, ',len_1=', len_1)
    print('unit_vector:', unit_vector_2, ',len_2=', len_2)

    # 返回单位化向量点积
    return np.dot(unit_vector_1, unit_vector_2)


def test():
    N = 7
    print(float(N+1)/2)


if __name__ == '__main__':
    test()
