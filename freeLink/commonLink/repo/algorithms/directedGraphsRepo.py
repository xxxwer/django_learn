# 有向图 相关算法

from var_dump import var_dump

# 有向图基本类
class Digraph(object):
    # digraphLines 结构
    def setDigraphLines(self, digraphLines):
        for line in digraphLines:
            self.addEdge(line[0], line[1])

    # 参数 V 为顶点数
    def __init__(self, V):
        if V < 0:
            raise Exception('顶点数必须大于0 或 边数必须大于0')
        self.v = V
        self.e = 0
        self.indegree = [0 for i in range(self.v)]
        self.adj = [[] for i in range(self.v)]

    def validateVertex(self, v):
        if v < 0 or v >= self.v:
            raise Exception("vertex " + v + " is not between 0 and " + (self.v-1))

    def addEdge(self, v, w):
        self.validateVertex(v)
        self.validateVertex(w)
        self.adj[v].append(w)
        self.indegree[v] += 1
        self.e += 1

    def copy(self, DigraphObj):
        dg = Digraph(DigraphObj.v)
        dg.e = DigraphObj.e
        i = 0
        for num in

    def __str__(self):
        s = str(self.v) + " vertices, " + str(self.e) + " edges\n"
        i = 0
        for x in self.adj:
            s += str(i) + ': '
            for y in x:
                s += str(y) + ' '
            s += '\n'
            i += 1
        return s

# class  KosarajuSharirSCC(object):

#     # 传入有向图 G
#     def __init__(self, G):
#         self. = arg


if __name__ == '__main__':
    dg = Digraph(13)
    dg.setDigraphLines([
        (4,2),
        (2,3),
        (3,2),
        (6,0),
        (0,1),
        (2,0),
        (11,12),
        (12,9),
        (9,10),
        (9,11),
        (7,9),
        (10,12),
        (11,4),
        (4,3),
        (3,5),
        (6,8),
        (8,6),
        (5,4),
        (0,5),
        (6,4),
        (6,9),
        (7,6)
        ])
    # var_dump(dg)
    print(dg)

# digraphLines 结构: 二元素元组如(4,2) 表示 顶点4 连接到 顶点2
# 有向图中，只有(4,2)而没有(2,4)出现的情况下，4可以连接到2，但2无法直接达到4
'''
[
(4,2),
(2,3),
(3,2),
(6,0),
(0,1),
(2,0),
(11,12),
(12,9),
(9,10),
(9,11),
(7,9),
(10,12),
(11,4),
(4,3),
(3,5),
(6,8),
(8,6),
(5,4),
(0,5),
(6,4),
(6,9),
(7,6)
]
'''
