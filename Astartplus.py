import copy
from timeit import default_timer as timer

thefinal_path = []


def move_position(chess2d, startx, starty, endx, endy):
    hold = chess2d[startx][starty]
    chess2d[startx][starty] = chess2d[endx][endy]
    chess2d[endx][endy] = hold
    return chess2d


class Node:

    def __init__(self, chessboard, g=0, h=0):
        self.nodeChess = chessboard
        self.father = None
        self.g = g
        self.h = h

    def set_h(self, end_Node):
        self.h = 0
        for i in range(4):
            for j in range(4):
                if self.nodeChess[i][j] == 0: continue
                for m in range(4):
                    for n in range(4):
                        if end_Node.nodeChess[m][n] == 0: continue
                        if end_Node.nodeChess[m][n] == self.nodeChess[i][j]:
                            self.h += (abs(m - i) + abs(n - j))

    def set_g(self, G):
        self.g = G

    def setFather(self, Father_Node):
        self.father = Father_Node


class A:

    def __init__(self, start_Node, End_Node):
        self.start = start_Node
        self.end = End_Node
        self.depth = 0
        self.curNode = start_Node
        self.closelist = []
        self.openlist = []
        self.result_path = []

    def getMinnode(self):
        hold_Node = self.openlist[0]
        for node in self.openlist:
            if node.g + node.h < hold_Node.h + hold_Node.g:
                hold_Node = node
        return hold_Node

    def if_Nodeinopen(self, node_find):
        for node in self.openlist:
            if node.nodeChess == node_find.nodeChess:
                return True
        return False

    def if_Nodeinclose(self, node_find):
        for node in self.closelist:
            if node.nodeChess == node_find.nodeChess:
                return True
        return False

    def get_Nodeinopen(self, node_get):
        for nodetemp in self.openlist:
            if nodetemp.nodeChess == node_get.nodeChess:
                return nodetemp
        return None

    def get_Nodeinclose(self, node_get):
        for nodetemp in self.closelist:
            if nodetemp.nodeChess == node_get.nodeChess:
                return nodetemp
        return None

    def searchNode(self, node):
        node_G = self.depth
        in_open = self.if_Nodeinopen(node)
        in_close = self.if_Nodeinclose(node)
        node.set_g(node_G)
        node.father = self.curNode
        if node.h == 0:
            node.set_h(self.end)
        if not in_open and not in_close:
            self.openlist.append(node)
        else:
            if in_close:
                tempnode = self.get_Nodeinclose(node)
                if node.g + node.h < tempnode.g + tempnode.h:
                    self.closelist.remove(tempnode)
                    self.openlist.append(node)
            if in_open:
                holdnode = self.get_Nodeinopen(node)
                if node.g + node.h < holdnode.g + holdnode.h:
                    holdnode.father = self.curNode
                    holdnode.g = node.g
                    holdnode.h = node.h
        return

    def is_endinOpen(self):
        for nodetemp in self.openlist:
            if nodetemp.nodeChess == self.end.nodeChess:
                return nodetemp
        return None

    def is_endinClose(self):
        for nodetemp in self.closelist:
            if nodetemp.nodeChess == self.end.nodeChess:
                return nodetemp
        return None

    def search_zero(self, chess):
        for x in range(4):
            for y in range(4):
                if int(chess[x][y]) == 0:
                    return x, y
        return None

    def searchNear(self):
        self.depth += 1
        x, y = self.search_zero(self.curNode.nodeChess)
        if x - 1 >= 0:
            chesstemp = move_position(copy.deepcopy(self.curNode.nodeChess), x,
                                      y, x - 1, y)
            self.searchNode(Node(chesstemp))
        if x + 1 <= 3:
            chesstemp = move_position(copy.deepcopy(self.curNode.nodeChess), x,
                                      y, x + 1, y)
            self.searchNode(Node(chesstemp))
        if y + 1 <= 3:
            chesstemp = move_position(copy.deepcopy(self.curNode.nodeChess), x,
                                      y, x, y + 1)
            self.searchNode(Node(chesstemp))
        if y - 1 >= 0:
            chesstemp = move_position(copy.deepcopy(self.curNode.nodeChess), x,
                                      y, x, y - 1)
            self.searchNode(Node(chesstemp))
        return

    def Astar_p(self):
        self.start.set_h(self.end)
        self.start.set_g(self.depth)
        self.openlist.append(self.start)
        cnt = 0
        while True and self.openlist:
            if self.depth > cnt:
                cnt = self.depth
                print(cnt)
            self.curNode = self.getMinnode()
            self.closelist.append(self.curNode)
            self.openlist.remove(self.curNode)
            self.depth = self.curNode.g
            self.searchNear()
            nodetemp = self.get_Nodeinopen(self.end)
            if nodetemp is not None:
                while True:
                    self.result_path.append(nodetemp)
                    if nodetemp.father is not None:
                        nodetemp = nodetemp.father
                    else:
                        return True
        return True


if __name__ == "__main__":
    tic = timer()
    a = A(Node([[1, 15, 7, 10], [9, 14, 4, 11], [8, 5, 0, 6], [13, 3, 2, 12]]),
          Node([
              [1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]
          ]))  # [1, 7, 8, 10], [6, 9, 15, 14], [13, 3, 0, 4], [11, 5, 12, 2]
    a.Astar_p()
    toc = timer()
    if a.result_path:
        print(toc - tic)
        for auto in a.result_path:
            thefinal_path.append(auto.nodeChess)
        thefinal_path.reverse()
        print(len(thefinal_path) - 1)
        for i in thefinal_path:
            print(i)
    else:
        print("没有元素。")
