import math
import random
import copy
import numpy as np #sss


class point:

    def __init__(self, number, dx, dy):
        self.ID = number
        self.x = dx
        self.y = dy
        self.weight = 0.0


class SA:

    def __init__(self, tem, L, pos_num, endtemp, midtemp, pointlist):
        self.path = []
        self.temperature = tem
        self.path_best = []
        self.loop_times = L
        self.posnum = pos_num
        self.end_temp = endtemp
        self.new_path = []
        self.mid_temp = midtemp
        self.point_list = pointlist
        self.best_pathcost = -1

    def count_distance(self, point_a, point_b):
        dx = math.pow(point_a.x - point_b.x, 2)
        dy = math.pow(point_a.y - point_b.y, 2)
        return math.pow(dx + dy, 0.5)

    def generate_random_pos(self):
        hold_randompos = []
        for auto in self.point_list:
            hold_randompos.append(auto.ID)
        random.shuffle(hold_randompos)
        return hold_randompos

    def generate_next_pos(self):
        if self.temperature > self.mid_temp:
            left_index = 0
            right_index = 0
            while left_index == right_index:
                left_index = random.randint(0, self.posnum - 1)
                right_index = random.randint(0, self.posnum - 1)

            if left_index > right_index:
                hold = left_index
                left_index = right_index
                right_index = hold
            temp_list = self.path[left_index:right_index:1]
            temp_list.reverse()
            self.new_path = copy.deepcopy(self.path)
            for i in range(left_index, right_index):
                self.new_path[i] = temp_list[i - left_index]
        else:
            left_index = 0
            right_index = 0
            while left_index == right_index:
                left_index = random.randint(0, self.posnum - 1)
                right_index = random.randint(0, self.posnum - 1)

            if left_index > right_index:
                left_index, right_index = right_index, left_index
            self.new_path = copy.deepcopy(self.path)
            hold = self.new_path[left_index]
            self.new_path[left_index] = self.new_path[right_index]
            self.new_path[right_index] = hold

    def count_f(self, mylist):
        path_len = 0.0
        for i in range(0, self.posnum - 1):
            a = self.point_list[mylist[i]-1]
            b = self.point_list[mylist[i + 1]-1]
            path_len += self.count_distance(a, b)
        path_len += self.count_distance(
            self.point_list[mylist[0]-1], self.point_list[mylist[self.posnum - 1]-1])
        return path_len

    def SA_solve(self):
        self.path = self.generate_random_pos()
        k = 1
        self.path_best = copy.deepcopy(self.path)
        self.best_pathcost = self.count_f(self.path)
        while self.temperature > self.end_temp:
            for i in range(0, self.loop_times):
                self.generate_next_pos()
                old_cost = self.count_f(self.path)
                new_cost = self.count_f(self.new_path)
                if new_cost < old_cost:
                    self.path = copy.deepcopy(self.new_path)
                    if self.best_pathcost > new_cost :
                        self.path_best = copy.deepcopy(self.path)
                        self.best_pathcost = new_cost
                else:
                    if random.random() < np.exp(-(new_cost - old_cost) / self.temperature):
                        self.path = copy.deepcopy(self.new_path)
            self.temperature = self.temperature / (1 + k)
            k += 1
            print("the " + str(k-1) + " times to decrease the temperature,and the best pathlength is " + str(
                self.best_pathcost))


if __name__ == "__main__":
    data = np.genfromtxt("/home/wuzhen/桌面/search/ch150", dtype=[int, float, float])
    point_num = int(len(data))
    point_list = []
    for i in range(point_num):
        a = point(int(data[i][0]), float(data[i][1]), float(data[i][2]))
        point_list.append(a)
    max_temp = 15000000000.0
    Loop_times = 20000
    end_temp = 0.00000000000001 * max_temp
    midtemp = 0.003 * max_temp
    test_SA = SA(max_temp, Loop_times, point_num, end_temp, midtemp, point_list)
    test_SA.SA_solve()
