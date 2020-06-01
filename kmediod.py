from sklearn.datasets import make_blobs
from matplotlib import pyplot
import numpy as np
import random
 
 
class KMediod():
    """
    ʵ�ּ򵥵�k-medoid�㷨
    """
    def __init__(self, n_points, k_num_center):
        self.n_points = n_points
        self.k_num_center = k_num_center
        self.data = None
 
    def get_test_data(self):
        """
        ������������, n_samples��ʾ���ٸ���, n_features��ʾ��ά, centers
        �õ���data��n�����������
        target��ÿ������ķ������˵�ҹ涨���ĸ����࣬target����Ϊn��ΧΪ0-3����Ҫ�ǻ�ͼ��ɫ����
        :return: none
        """
        self.data, target = make_blobs(n_samples=self.n_points, n_features=2, centers=self.n_points)
        np.put(self.data, [self.n_points, 0], 500, mode='clip')
        np.put(self.data, [self.n_points, 1], 500, mode='clip')
        pyplot.scatter(self.data[:, 0], self.data[:, 1], c=target)
        # ��ͼ
        pyplot.show()
 
    def ou_distance(self, x, y):
        # ����ŷʽ����ļ���
        return np.sqrt(sum(np.square(x - y)))
 
    def run_k_center(self, func_of_dis):
        """
        ѡ���þ��빫ʽ��ʼ����ѵ��
        :param func_of_dis:
        :return:
        """
        print('��ʼ��', self.k_num_center, '�����ĵ�')
        indexs = list(range(len(self.data)))
        random.shuffle(indexs)  # ���ѡ������
        init_centroids_index = indexs[:self.k_num_center]
        centroids = self.data[init_centroids_index, :]   # ��ʼ���ĵ�
        # ȷ��������
        levels = list(range(self.k_num_center))
        print('��ʼ����')
        sample_target = []
        if_stop = False
        while(not if_stop):
            if_stop = True
            classify_points = [[centroid] for centroid in centroids]
            sample_target = []
            # ��������
            for sample in self.data:
                # ������룬�ɾ������������ĺ��ģ�ȷ���õ��������
                distances = [func_of_dis(sample, centroid) for centroid in centroids]
                cur_level = np.argmin(distances)
                sample_target.append(cur_level)
                # ͳ�ƣ����������ɺ����¼����м��
                classify_points[cur_level].append(sample)
            # ���»�������
            for i in range(self.k_num_center):  # �����зֱ�Ѱ��һ�����ŵ�
                distances = [func_of_dis(point_1, centroids[i]) for point_1 in classify_points[i]]
                now_distances = sum(distances)   # ���ȼ�����������ĵ���������е�ľ����ܺ�
                for point in classify_points[i]:
                    distances = [func_of_dis(point_1, point) for point_1 in classify_points[i]]
                    new_distance = sum(distances)
                    # ������þ۴��и��������������е���ܺͣ�������С�ڵ�ǰ���ĵ�ľ����ܺ͵ģ����ĵ�ȥ��
                    if new_distance < now_distances:
                        now_distances = new_distance
                        centroids[i] = point    # ���ɸõ�
                        if_stop = False
        print('����')
        return sample_target
 
    def run(self):
        """
        �Ȼ�����ݣ��ɴ�������õ����ҵ�n���㣬Ȼ������n���㣬��Ϊm����
        :return:
        """
        self.get_test_data()
        predict = self.run_k_center(self.ou_distance)
        pyplot.scatter(self.data[:, 0], self.data[:, 1], c=predict)
        pyplot.show()
 
 
test_one = KMediod(n_points=1000, k_num_center=3)
test_one.run()