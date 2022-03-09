import copy

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
                for m in range(4):
                    for n in range(4):
                        if self.chess[i][j] == end_Node.chess[m][n]:
                            self.h += (abs(i - m) + abs(j - n))

    def set_G(self, G):
        self.g = G

    def setFather(self, Father_Node):
        self.father = Father_Node


class IDAstar:

    def __init__(self, start_node, end_node):
        self.start = start_node
        self.end = end_node
        self.vis = []
        self.result_path = []
        self.Max_deep = 30
        self.cnt = 0

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
            if auto1.chess == node:
                return True
        return False

    def IDA(self, curNode):  # 这个为设置h(x)大小的函数，传入目标节点即是终点，根据现在棋盘和目标有多少个不一样确定
        key = False
        if self.is_end(curNode):
            key = True
            while curNode is not None:
                self.result_path.append(curNode)
                curNode = curNode.father
            return key
        self.vis.append(curNode)
        for i in range(4):
            cur_x, cur_y = self.get_startposition(curNode)
            next_x = cur_x + nextstep[i][0]  # 下一步的坐标
            next_y = cur_y + nextstep[i][1]
            if not self.check_inborder(next_x, next_y):
                continue
            next_chess = move_position(copy.deepcopy(curNode.chess), cur_x,
                                       cur_y, next_x, next_y)
            if self.Find_vis(next_chess):
                continue
            next_Node = Node(next_chess)
            next_Node.set_h(self.end)
            next_Node.set_G(curNode.g + 1)
            next_Node.setFather(curNode)
            if next_Node.g + next_Node.h <= self.Max_deep:
                key = self.IDA(next_Node)
                if key:
                    return key
        return key

    def Main_func(self):
        self.start.set_h(self.end)
        while self.IDA(self.start) is False:
            print("加深")
            self.vis.clear()
            self.Max_deep += 2
        return


if __name__ == "__main__":
    idA = IDAstar(
        Node([[5, 1, 2, 4], [9, 6, 3, 8], [13, 15, 10, 11], [14, 0, 7, 12]]),
        Node([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]))
    idA.Main_func()
    if idA.result_path:
        print("Yes")
        idA.result_path.reverse()
        for auto in idA.result_path:
            print(auto.chess)
    else:
        print("No")
