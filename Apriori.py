from numpy import *
 
def loadDataSet():
    return [[1,3,4], [2,3,5], [1,2,3,5], [2,5]]
 
def createC1(dataSet):  # �����ѡ�C1��C1�Ǵ�СΪ1�����к�ѡ��ļ���
    C1 = []
    for transaction in dataSet:   
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    # C1.sort()     # �Ӵ�С����
    return list(map(frozenset,C1))
 
def scanD(D,Ck,minSupport):  # �˺�������֧�ֶ�,ɸѡ����Ҫ������ΪƵ���Lk��D�����ݼ���CkΪ��ѡ�C1��C2��C3 ...
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
        support = ssCnt[key]/numItems    # ����֧�ֶ�
        if support >= minSupport:   # ���֧�ֶȴ����趨����С֧�ֶ�
           # retList.insert(0,key)
            retList.append(key)
        supportData[key] = support
    return retList, supportData
 
def aprioriGen(Lk, k):   # �°�aproriGen
    lenLk = len(Lk)
    temp_dict = {}  # ��ʱ�ֵ䣬�洢
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = Lk[i]|Lk[j]  # �����ϲ���ִ���� lenLk����
            if len(L1) == k:  # ����ϲ��������Ԫ����k��������Ҫ��
                if not L1 in temp_dict:  # �ѷ��ϵ�����浽�ֵ�ļ��У�ʹ���ֵ����ȥ�ظ�������{1,2,3}��{3��1��2}��һ�����ʹ�����ֵ�Ϳ��Դﵽȥ�ص�����
                    temp_dict[L1] = 1
    return list(temp_dict)  # ���ֵ�ļ�ת��Ϊ�б�
 
# def aprioriGen(Lk, k):  # ����Ƶ���Lk-1�����ѡ�Ck
#     retList = []
#     lenLk = len(Lk)
#     for i in range(lenLk):
#         for j in range(i+1, lenLk):
#            L1 = list(Lk[i])[:k-2]
#             L2 = list(Lk[j])[:k-2]
#             L1.sort()     # ����
#             L2.sort()
#            if L1 == L2:   # �Ƚ�ǰLk-1�е��������k-2��Ԫ���Ƿ���ͬ���������ܱ�֤�ϳɺ�ֻ��k��Ԫ��
#                retList.append(Lk[i]|Lk[j])
#    return retList
 
def apriori(dataSet, minSupport = 0.5):  # ͨ��ѭ���ó�[L1,L2,L3..]Ƶ����б�
    C1 = createC1(dataSet)     # ����C1
    D = list(map(set,dataSet))
    L1,supportData = scanD(D, C1, minSupport)  ɸѡ��L1
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):   # ����Ck
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