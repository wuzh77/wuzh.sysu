import copy
from timeit import default_timer as timer

nextstep = [[1, 0], [-1, 0], [0, 1], [0, -1]]
Manhaton = {}


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
        self.h = 0
        hold_h = Manhaton.get(str(self.chess))
        if hold_h:
            self.h = int(hold_h)
        else:
            for i in range(4):
                for j in range(4):
                    if self.chess[i][j] != 0 and self.chess[i][j] != (i * 4 +
                                                                      j + 1):
                        ii = (self.chess[i][j] - 1) // 4
                        jj = (self.chess[i][j] - 1) % 4
                        self.h += (abs(ii - i) + abs(jj - j))
            Manhaton[str(self.chess)] = int(self.h)

    def set_G(self, G):
        self.g = G

    def setFather(self, Father_Node):
        self.father = Father_Node


class IDAstar:

    def __init__(self, start_node, end_node):
        self.start = start_node
        self.end = end_node
        self.start.set_h(self.end)
        self.vis = []
        self.result_path = []
        self.Max_deep = self.start.h

    def getMinnode(self):
        hold_Node = self.stack[0]
        for node in self.stack:
            if node.g + node.h < hold_Node.g + hold_Node.h:
                hold_Node = node
        return hold_Node

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
            if auto1.chess == node.chess and node.h == auto1.h and node.g == auto1.g:
                return auto1
        return None

    def IDA(self, curNode):  # 这个为设置h(x)大小的函数，传入目标节点即是终点，根据现在棋盘和目标有多少个不一样确定
        key = False
        if self.is_end(curNode):  #判断当前节点是否为终点节点
            key = True
            while curNode is not None:  #如果是则回溯，将路径输入最后存放答案的list中
                self.result_path.append(curNode)
                curNode = curNode.father
            return key
        self.vis.append(curNode)
        for i in range(4):
            cur_x, cur_y = self.get_startposition(curNode)  #当前状态（0，0）的坐标
            next_x = cur_x + nextstep[i][0]  # 下一步的坐标
            next_y = cur_y + nextstep[i][1]
            if not self.check_inborder(next_x, next_y):  #判断（0，0）是否在状态内
                continue
            next_chess = move_position(copy.deepcopy(curNode.chess), cur_x,
                                       cur_y, next_x,
                                       next_y)  #若在状态内，就移动，生成下一个节点
            next_Node = Node(next_chess)  #此处设置扩展结点节点的信息
            next_Node.set_h(self.end)
            next_Node.set_G(curNode.g + 1)
            next_Node.setFather(curNode)
            vis_Node = self.Find_vis(next_Node)  #在vis表中查找该节点是否搜索过，若搜索过则跳过
            if vis_Node:
                continue
            if next_Node.g + next_Node.h <= self.Max_deep:  #当该节点未搜索过，且h + g < maxdepth时候就继续递归该节点
                if self.IDA(next_Node):
                    return True
        return key

    def Main_func(self):
        self.start.g = 0
        while self.IDA(self.start) is False:
            print(self.Max_deep)
            self.vis.clear()
            self.Max_deep += 2
        return


if __name__ == "__main__":
    tic = timer()
    idA = IDAstar(
        Node([[11, 3, 1, 7], [4, 6, 8, 2], [15, 9, 10, 13], [14, 12, 5, 0]]),
        Node([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]))
    idA.Main_func()
    toc = timer()
    if idA.result_path:
        print("Yes")
        delta_time = toc - tic
        print(delta_time)
        idA.result_path.reverse()
        print(len(idA.result_path) - 1)
        filename = "data_out.txt"
        with open(filename, "w") as fileout:
            for auto in idA.result_path:
                fileout.write(str(auto.chess))
                fileout.write("\n")
            fileout.write(str(delta_time))
    else:
        print("No")
