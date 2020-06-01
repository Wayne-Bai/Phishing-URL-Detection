from sklearn.datasets import make_blobs
from matplotlib import pyplot
import numpy as np
import random
 
 
class KMediod():
    """
    实现简单的k-medoid算法
    """
    def __init__(self, n_points, k_num_center):
        self.n_points = n_points
        self.k_num_center = k_num_center
        self.data = None
 
    def get_test_data(self):
        """
        产生测试数据, n_samples表示多少个点, n_features表示几维, centers
        得到的data是n个点各自坐标
        target是每个坐标的分类比如说我规定好四个分类，target长度为n范围为0-3，主要是画图颜色区别
        :return: none
        """
        self.data, target = make_blobs(n_samples=self.n_points, n_features=2, centers=self.n_points)
        np.put(self.data, [self.n_points, 0], 500, mode='clip')
        np.put(self.data, [self.n_points, 1], 500, mode='clip')
        pyplot.scatter(self.data[:, 0], self.data[:, 1], c=target)
        # 画图
        pyplot.show()
 
    def ou_distance(self, x, y):
        # 定义欧式距离的计算
        return np.sqrt(sum(np.square(x - y)))
 
    def run_k_center(self, func_of_dis):
        """
        选定好距离公式开始进行训练
        :param func_of_dis:
        :return:
        """
        print('初始化', self.k_num_center, '个中心点')
        indexs = list(range(len(self.data)))
        random.shuffle(indexs)  # 随机选择质心
        init_centroids_index = indexs[:self.k_num_center]
        centroids = self.data[init_centroids_index, :]   # 初始中心点
        # 确定种类编号
        levels = list(range(self.k_num_center))
        print('开始迭代')
        sample_target = []
        if_stop = False
        while(not if_stop):
            if_stop = True
            classify_points = [[centroid] for centroid in centroids]
            sample_target = []
            # 遍历数据
            for sample in self.data:
                # 计算距离，由距离该数据最近的核心，确定该点所属类别
                distances = [func_of_dis(sample, centroid) for centroid in centroids]
                cur_level = np.argmin(distances)
                sample_target.append(cur_level)
                # 统计，方便迭代完成后重新计算中间点
                classify_points[cur_level].append(sample)
            # 重新划分质心
            for i in range(self.k_num_center):  # 几类中分别寻找一个最优点
                distances = [func_of_dis(point_1, centroids[i]) for point_1 in classify_points[i]]
                now_distances = sum(distances)   # 首先计算出现在中心点和其他所有点的距离总和
                for point in classify_points[i]:
                    distances = [func_of_dis(point_1, point) for point_1 in classify_points[i]]
                    new_distance = sum(distances)
                    # 计算出该聚簇中各个点与其他所有点的总和，若是有小于当前中心点的距离总和的，中心点去掉
                    if new_distance < now_distances:
                        now_distances = new_distance
                        centroids[i] = point    # 换成该点
                        if_stop = False
        print('结束')
        return sample_target
 
    def run(self):
        """
        先获得数据，由传入参数得到杂乱的n个点，然后由这n个点，分为m个类
        :return:
        """
        self.get_test_data()
        predict = self.run_k_center(self.ou_distance)
        pyplot.scatter(self.data[:, 0], self.data[:, 1], c=predict)
        pyplot.show()
 
 
test_one = KMediod(n_points=1000, k_num_center=3)
test_one.run()