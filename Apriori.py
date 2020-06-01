from numpy import *
 
def loadDataSet():
    return [[1,3,4], [2,3,5], [1,2,3,5], [2,5]]
 
def createC1(dataSet):  # 创造候选项集C1，C1是大小为1的所有候选项集的集合
    C1 = []
    for transaction in dataSet:   
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    # C1.sort()     # 从大到小排序
    return list(map(frozenset,C1))
 
def scanD(D,Ck,minSupport):  # 此函数计算支持度,筛选满足要求的项集成为频繁项集Lk，D是数据集，Ck为候选项集C1或C2或C3 ...
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems    # 计算支持度
        if support >= minSupport:   # 如果支持度大于设定的最小支持度
           # retList.insert(0,key)
            retList.append(key)
        supportData[key] = support
    return retList, supportData
 
def aprioriGen(Lk, k):   # 新版aproriGen
    lenLk = len(Lk)
    temp_dict = {}  # 临时字典，存储
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = Lk[i]|Lk[j]  # 两两合并，执行了 lenLk！次
            if len(L1) == k:  # 如果合并后的子项元素有k个，满足要求
                if not L1 in temp_dict:  # 把符合的新项存到字典的键中，使用字典可以去重复，比如{1,2,3}和{3，1，2}是一样的项，使用了字典就可以达到去重的作用
                    temp_dict[L1] = 1
    return list(temp_dict)  # 把字典的键转化为列表
 
# def aprioriGen(Lk, k):  # 根据频繁项集Lk-1创造候选项集Ck
#     retList = []
#     lenLk = len(Lk)
#     for i in range(lenLk):
#         for j in range(i+1, lenLk):
#            L1 = list(Lk[i])[:k-2]
#             L2 = list(Lk[j])[:k-2]
#             L1.sort()     # 排序
#             L2.sort()
#            if L1 == L2:   # 比较前Lk-1中的两个项的k-2个元素是否相同，这样才能保证合成后只有k个元素
#                retList.append(Lk[i]|Lk[j])
#    return retList
 
def apriori(dataSet, minSupport = 0.5):  # 通过循环得出[L1,L2,L3..]频繁项集列表
    C1 = createC1(dataSet)     # 创造C1
    D = list(map(set,dataSet))
    L1,supportData = scanD(D, C1, minSupport)  筛选出L1
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):   # 创造Ck
        Ck = aprioriGen(L[k-2],k)
        Lk, supK = scanD(D,Ck,minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L,supportData
 
if __name__ == "__main__":
    dataSet = loadDataSet()
    L,suppData = apriori(dataSet)
    print(L)