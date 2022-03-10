import copy
from queue import PriorityQueue

nextstep = [[1, 0], [-1, 0], [0, 1], [0, -1]]


def move_position(chessboard, startx, starty, endx, endy):
    hold = chessboard[startx][starty]
    chessboard[startx][starty] = chessboard[endx][endy]
    chessboard[endx][endy] = hold
    return chessboard


class Node:

    def __init__(self, chessboard, g=0, h=0):
        self.chess = chessboard
        self.father = None
        self.g = g
        self.h = h

    def set_h(self, end_Node):
        for i in range(4):
            for j in range(4):
                if int(end_Node.chess[i][j]) != int(self.chess[i][j]):
                    self.h += 1

    def set_G(self, G):
        self.g = G

    def setFather(self, Father_Node):
        self.father = Father_Node


class cmp(object):

    def __init__(self, priority, node):
        self.my_priority = priority
        self.my_node = node

    def __lt__(self, other):
        return self.my_priority < other.my_priority

    def return_node(self):
        return self.my_node


class IDAstar:

    def __init__(self, start_node, end_node):
        self.start = start_node
        self.end = end_node
        self.vis = []
        self.result_path = []
        self.Max_deep = 1
        self.stack = PriorityQueue()
        self.cnt = 0

    def is_end(self, check_node):
        return check_node.chess == self.end.chess

    def get_startposition(self, array):
        for x in range(4):
            for y in range(4):
                if int(array.chess[x][y]) == 0:
                    return x, y

    def check_inborder(self, pos_x, pos_y):
        return 0 <= pos_x <= 3 and 0 <= pos_y <= 3

    def Find_vis(self, node):
        for auto1 in self.vis:
            if auto1.chess == node:
                return True
        return False

    def IDA(self, curNode):
        curNode.set_h(self.end)  # 这个为设置h(x)大小的函数，传入目标节点即是终点，根据现在棋盘和目标有多少个不一样确定
        curNode.set_G(0)  # 设置g(x)，此处为深度
        self.stack.put_nowait(cmp(curNode.g + curNode.h, curNode))  # 优先队列内弹入开始节点
        key = False
        while not self.stack.empty():  # 优先队列不为空时进行
            hold = self.stack.get()  # 从栈中弹出一个节点
            my_Node = hold.return_node()
            self.vis.append(my_Node)  # 弹出的标记已经访问
            self.cnt += 1
            if self.cnt % 1000 == 0:
                print(self.cnt)
            if self.is_end(my_Node):  # 判断当前弹出节点是否满足最后目标
                key = True
                while my_Node is not None:
                    self.result_path.append(my_Node)  # 沿着路径回溯
                    my_Node = my_Node.father
                break
            for i in range(4):
                cur_x, cur_y = self.get_startposition(my_Node)
                next_x = cur_x + nextstep[i][0]  # 下一步的坐标
                next_y = cur_y + nextstep[i][1]
                if not self.check_inborder(next_x, next_y):
                    continue
                next_chess = move_position(copy.deepcopy(my_Node.chess), cur_x,
                                           cur_y, next_x, next_y)
                if self.Find_vis(next_chess):
                    continue
                next_Node = Node(next_chess)
                next_Node.set_h(self.end)
                next_Node.set_G(my_Node.g + 1)
                next_Node.setFather(my_Node)
                if next_Node.g + next_Node.h <= self.Max_deep:
                    self.stack.put(cmp(next_Node.g + next_Node.h, next_Node))
        return key

    def Main_func(self):
        while self.IDA(self.start) is False:
            print("加深")
            self.vis.clear()
            self.Max_deep += 1
        return


if __name__ == "__main__":
    idA = IDAstar(
        Node([[1, 15, 7, 10], [9, 14, 4, 11], [8, 5, 0, 6], [13, 3, 2, 12]]),
        Node([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]))
    idA.Main_func()
    if idA.result_path:
        print("Yes")
        idA.result_path.reverse()
        for auto in idA.result_path:
            print(auto.chess)
    else:
        print("No")
