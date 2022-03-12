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
                if end_Node.nodeChess[i][j] == 0:
                    continue
                for m in range(4):
                    for n in range(4):
                        if self.nodeChess[m][n] == 0:
                            continue
                        if end_Node.nodeChess[i][j] == self.nodeChess[m][n]:
                            self.h += (abs(i - m) + abs(j - n))

    def set_g(self, G):
        self.g = G

    def setFather(self, Father_Node):
        self.father = Father_Node


class priority_queue:

    def __init__(self):
        self.queue = []

    def swap(self, index1, index2):
        temp = self.queue[index1]
        self.queue[index1] = self.queue[index2]
        self.queue[index2] = temp

    def put(self, val):
        self.queue.append(val)
        cur = len(self.queue) - 1
        while cur > 0:
            parent = (cur - 1) // 2
            if self.queue[parent].g + self.queue[parent].h > self.queue[
                    cur].g + self.queue[cur].h:
                self.swap(parent, cur)
            else:
                break
            cur = parent

    def top(self):
        if len(self.queue) == 0:
            print("the queue is empty.")
        else:
            return self.queue[0]

    def find_speci(self, val):
        for auto in self.queue:
            if auto.nodeChess == val.nodeChess:
                return auto
        return None

    def queue_empty(self):
        return len(self.queue) == 0

    def get(self):
        first = self.top()
        last = self.queue.pop()
        if not self.queue_empty():
            self.queue[0] = last
            cur = 0
            while cur < len(self.queue):
                left_child = 2 * cur + 1
                right_child = 2 * cur + 2
                if right_child >= len(self.queue) or left_child >= len(
                        self.queue):
                    break
                if self.queue[cur].g + self.queue[cur].h <= min(
                        self.queue[left_child].h + self.queue[left_child].g,
                        self.queue[right_child].h + self.queue[right_child].g):
                    break
                if self.queue[left_child].h + self.queue[
                        left_child].g < self.queue[right_child].g + self.queue[
                            right_child].h:
                    self.swap(left_child, cur)
                    cur = left_child
                else:
                    self.swap(right_child, cur)
                    cur = right_child
        return first


class A:

    def __init__(self, start_Node, End_Node):
        self.start = start_Node
        self.end = End_Node
        self.depth = 0
        self.start.set_h(self.end)
        self.curNode = start_Node
        self.closelist = []
        self.openlist = priority_queue()
        self.result_path = []

    def if_Nodeinclose(self, node_find):
        for node in self.closelist:
            if node.nodeChess == node_find.nodeChess:
                return True
        return False

    def get_Nodeinopen(self, speci_node):
        return self.openlist.find_speci(speci_node)

    def get_Nodeinclose(self, speci_node):
        for auto in self.closelist:
            if auto.nodeChess == speci_node.nodeChess:
                return auto
        return None

    def is_endinOpen(self):
        if self.openlist.find_speci(self.end):
            return True
        return False

    def searchNode(self, node):
        node_G = self.depth
        node.g = node_G
        node.father = self.curNode
        if node.h == 0:
            node.set_h(self.end)
        in_open = self.get_Nodeinopen(node)
        in_close = self.get_Nodeinclose(node)
        if in_open is None and in_close is None:
            self.openlist.put(node)
        else:
            if in_close:
                tempnode = in_close
                if tempnode.g > node.g:
                    self.closelist.remove(tempnode)
                    self.openlist.put(node)
            if in_open:
                holdnode = in_open
                if holdnode.g > node.g:
                    self.openlist.put(node)
        return

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
        cnt = 0
        self.openlist.put(self.start)
        while True and not self.openlist.queue_empty():
            if self.depth > cnt:
                cnt = self.depth
                print(cnt)
            self.curNode = self.openlist.get()
            self.closelist.append(self.curNode)
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
    a = A(Node([[1, 7, 8, 10], [6, 9, 15, 14], [13, 3, 0, 4], [11, 5, 12, 2]]),
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
