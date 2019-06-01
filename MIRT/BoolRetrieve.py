import re
import os


# 扫描目录下文档集
def document_scanner(filePath):
    """
    扫描目录下所有文档
    文档映射字典：{doc_Id:[doc_Name, doc]}
    字典字段含义：
    doc_Id：文档ID
    doc_Name：文档名
    doc：文档文件
    :param filePath:文档集目录
    :return documents_dic:文档映射字典
    """
    documents_dic = {}
    try:
        for doc_Id, doc_Name in enumerate(os.listdir(filePath), start=1):
            f = open(filePath + doc_Name)
            # 按目录下文档顺序构建doc_Id
            documents_dic.setdefault(doc_Id, [doc_Name, f.read()])
            # 关闭文件流
            f.close()
    except FileNotFoundError:
        print("ERROR：文档集路径有误！")
        exit(-1)
    # 返回文档映射字典
    return documents_dic


# 文本--->单词列表
def text2words(text):
    """
    单个文档生成词项列表
    :param text: 文档
    :return: 词项列表
    """
    words = re.sub(r'[^\w\s]', '', text.lower()).split(' ')

    return words


# 构建倒排索引
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
        # 文档词项化
        term_list = text2words(doc[1])
        # 将词项加入倒排索引
        for term in term_list:
            # 如果倒排索引无词项term，则加入倒排索引中
            if term not in invert_index.keys():
                invert_index[term] = [doc_ID]
            else:
                # 更新词项term的倒排列表
                if doc_ID not in invert_index[term]:
                    invert_index[term].extend([doc_ID])
    # 返回倒排索引
    return invert_index


# 布尔查询处理
def queries(inverted_Index, query):
    """
    对查询语句进行处理
    以[doc_Id]形式返回查询结果
    :param inverted_Index: 倒排索引
    :param query: 查询语句
    :return:
    """
    queryResult = []
    try:
        # 查询语句分割：词项1，联查运算OP，词项2
        cond1, option, cond2 = query.strip().split(' ')
        print("[cond1 = %s, option = %s, cond2 = %s]" % (cond1, option.upper(), cond2))

        cond1_result_list = set([])
        cond2_result_list = set([])

        # 操作符判断
        if option not in ['AND', 'OR']:
            raise RuntimeError('ERROR:啊哦，输入不规范哦~')

        # 词项1的查询结果
        if cond1 in inverted_Index.keys():
            cond1_result_list = set(inverted_Index[cond1.lower()])
        print("%s的倒排索引：" % cond1, list(cond1_result_list))

        # 词项2的查询结果
        if cond2 in inverted_Index.keys():
            cond2_result_list = set(inverted_Index[cond2.lower()])
        print("%s的倒排索引：" % cond2, list(cond2_result_list))

        # 交集
        if option == 'AND':
            queryResult = cond1_result_list & cond2_result_list
        # 并集
        if option == 'OR':
            queryResult = cond1_result_list | cond2_result_list
    # 异常处理
    except(ValueError, RuntimeError) as e:
        print(e)

    # 返回查询结果：文档id列表[doc_ID]
    return list(queryResult)


# 搜索结果-->文档映射
def queryResult2doc(queryResult, docmentsDIC):
    """
    将查询结果与文档名进行映射
    :param queryResult: 布尔查询处理结果列表
    :param docmentsDIC: 文档和文档ID映射表
    :return: 文档名列表
    """
    result = []
    for doc_Id in queryResult:
        result.append(docmentsDIC[doc_Id][0])
    return result


# 开始
def start():
    """
    功能入口
    :return:
    """
    # 文档集目录路径
    file_path = 'documents_en\\'
    '''
    documentDict：
    {doc_ID:[doc_Name,doc]}
    doc_ID：文档id
    doc_Name：文档名
    doc：文档
    '''
    # 扫描目录下文档集
    documentDict = document_scanner(file_path)
    # 生成倒排索引
    invertIndex = inverted_index(documentDict)
    # # 输出倒排索引
    # for each in invertIndex:
    #     print(each + ':', invertIndex[each])

    print('---' * 20)  # 分隔符

    # 布尔查询
    while True:
        seq = input("布尔查询语句：cond1 AND/OR cond2:")
        # 布尔查询处理
        query = queries(invertIndex, seq)
        # 查询结果映射文档
        query_result = queryResult2doc(query, documentDict)
        # 输出查询结果
        print("布尔查询结果：", query_result)

        print('---' * 30)  # 分隔符


if __name__ == '__main__':
    start()
