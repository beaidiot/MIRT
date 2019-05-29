import os
import re
import math
import numpy as np

N = 4.0  # 文档集数量


# 扫描目录下文档集
def document_scanner(filePath):
    """
    扫描目录下所有文档
    文档映射字典：{doc_Name:doc]}
    字典字段含义：
    doc_Name：文档名
    doc：文档内容
    :param filePath:文档集目录
    :return documents_dic:文档映射字典
    """
    documents_dic = {}
    try:
        for doc_Name in os.listdir(filePath):
            f = open(filePath + doc_Name)
            # 按目录下文档顺序构建doc_Id
            documents_dic.setdefault(doc_Name, f.read().lower())
            f.close()
    except FileNotFoundError:
        print("ERROR：文档集路径有误！")
        exit(-1)

    # 返回文档映射字典
    return documents_dic


# 文档词项化
def text2words(text):
    # 文档分词
    words = re.sub(r'[^\w\'\s]', '', text).split(' ')

    # 返回文档的单词列表
    return words


# 倒排索引
def inverted_index(documents):
    """
    对文档集生成倒排索引
    :param documents: 文档集
    :return invert_index: 倒排索引
    """
    # 初始化倒排索引：{terms：[doc_ID]}
    invert_index = {}
    # 循环处理每个文档
    for doc_ID, doc in documents.items():
        # 将词项加入倒排索引
        for term in doc:
            # 如果倒排索引无词项term，则加入倒排索引中
            if term not in invert_index.keys():
                invert_index[term] = [doc_ID]
            elif doc_ID not in invert_index[term]:
                invert_index[term].extend([doc_ID])
    # 返回倒排索引
    return invert_index


# 生成词典，作为向量空间
def create_vocabulary(text):
    vacabulary = []
    for word in text.split(' '):
        if word not in vacabulary:
            vacabulary.append(word)
    return vacabulary


# 计算词项频率tf
def create_tf(text, vocabulary):
    # 词项频率字典
    tf = {}
    # 初始化词项频率字典
    for word in vocabulary:
        tf.setdefault(word, 0.0)
    # 构建词项频率
    for word in text:
        if word in vocabulary:
            tf[word] += 1.0
    # 返回词项频率
    return tf


# 计算逆文档频率idf
def create_idf(invertedIndex, vocabulary):
    df = {}  # 文档频率，单词w出现的文档数
    idf = {}  # 逆文档频率，log（N+1）/df

    # 计算df
    for word in vocabulary:
        if word in invertedIndex.keys():
            df.setdefault(word, len(invertedIndex[word]))
        else:
            df.setdefault(word, 0.0)
    # 计算idf
    for word, word_df in df.items():
        if df[word] != 0.0:
            idf.setdefault(word, math.log(float(N + 1.0) / df[word], 10))
        else:
            idf.setdefault(word, 0.0)
    # 返回idf
    return idf


# 基于TF生成空间向量
def create_Vector_TF(tf, vocabulary):
    v = []
    for word in vocabulary:
        if word in tf.keys():
            v.append(tf[word])
        else:
            v.append(0.0)
    return v


# 基于TF-IDF生成空间向量
def create_Vector_TF_IDF(tf, idf, vocabulary):
    v = []
    for word in vocabulary:
        if tf[word] != 0.0:
            v.append((1.0 + math.log(tf[word], 10)) * idf[word])
        else:
            v.append(0.0)
    return v


# 计算向量点积作为相似度
def compute_similarity(vector_1, vector_2):
    vector_1 = np.array(vector_1)
    vector_2 = np.array(vector_2)

    # 向量归一化
    len_1 = np.sqrt(np.dot(vector_1, vector_1))  # 向量长度
    unit_vector_1 = (vector_1 / len_1) if len_1 else vector_1  # 单位化

    len_2 = np.sqrt(np.dot(vector_2, vector_2))  # 向量长度
    unit_vector_2 = (vector_2 / len_2) if len_2 else vector_2  # 单位化

    # 返回向量点积
    return float('%.4f' % np.dot(unit_vector_1, unit_vector_2))


# 基于tf的VSM模型
def vsm_base_TF(query, documents, vocabulary):
    print('------------------VSM by TF---------------------')

    # 查询语句词项化
    q_tf = create_tf(query.split(' '), vocabulary)

    # 查询语句向量化
    q_vector = create_Vector_TF(q_tf, vocabulary)

    # print('查询向量：', q_vector) code for test

    # 对每个文档进行词项化
    docs = {}
    for doc_name, text in documents.items():
        docs.setdefault(doc_name, text2words(text))

    # 对每个文档计算词项频率
    doc_tf = {}
    for doc_name, text in docs.items():
        doc_tf.setdefault(doc_name, create_tf(text, vocabulary))

    # 对每个文档建立空间向量
    doc_vector = {}
    for doc_name, tf in doc_tf.items():
        doc_vector.setdefault(doc_name, create_Vector_TF(tf, vocabulary))

    # 计算查询与各文档文本相似度
    for doc_name, d_vector in doc_vector.items():
        print("[%s]" % doc_name, '相似度：', compute_similarity(q_vector, d_vector))


# 基于tf-idf的VSM模型
def vsm_base_TF_IDF(query, documents, vocabulary):
    print('-----------------VSM by TF-IDF--------------------')

    # 查询语句词项化
    q_tf = create_tf(query.split(' '), vocabulary)
    # print('q_tf:', q_tf)

    # 对每个文档进行词项化
    docs = {}
    for doc_name, text in documents.items():
        docs.setdefault(doc_name, text2words(text))

    # 对每个文档计算词项频率
    docs_tf = {}
    for doc_name, text in docs.items():
        docs_tf.setdefault(doc_name, create_tf(text, vocabulary))
    # print('d_tf:', docs_tf)

    # 生成倒排索引invertedIndex
    invertedIndex = inverted_index(docs)

    # 计算idf
    idf = create_idf(invertedIndex, vocabulary)
    # print('idf：', idf)

    # 查询语句向量化
    q_vector = create_Vector_TF_IDF(q_tf, idf, vocabulary)
    # print('q_vector：', q_vector)

    # 文档集向量化
    doc_vector = {}
    for doc_name, d_tf in docs_tf.items():
        doc_vector.setdefault(doc_name, create_Vector_TF_IDF(d_tf, idf, vocabulary))
    # print('doc_vector:', doc_vector)

    # 计算查询与各文档文本相似度
    for doc_name, d_vector in doc_vector.items():
        # print('[%s]' % doc_name, d_vector)
        print("[%s]" % doc_name, '相似度：', compute_similarity(q_vector, d_vector))


# 向量空间模型
def VSM():
    # 查询语句
    query = input('查询语句：').lower()

    # 构建词汇表
    vocabulary = create_vocabulary(query)

    # 扫描目录文档集
    documents = document_scanner('documents_en\\')

    # 基于词项频率tf的VSM模型
    vsm_base_TF(query, documents, vocabulary)

    # 基于tf-idf的VSM模型
    vsm_base_TF_IDF(query, documents, vocabulary)


if __name__ == '__main__':
    VSM()
