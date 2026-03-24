

"""
def treeDP(root, graph, default, combine, finalize = lambda nodeDP,node,eind: nodeDP):
    DP = [0] * len(graph)
    def dfs(node, parent=-1):
        nodeDP = default[node]
        for eind, nei in enumerate(graph[node]):
            if nei != parent:
                neiDP = dfs(nei, node)
                nodeDP = combine(nodeDP, neiDP, node, eind)
        parent_eind = -1 if parent == -1 else graph[node].index(parent)
        DP[node] = finalize(nodeDP, node, parent_eind)
        return DP[node]
    
    dfs(root)
    return DP
"""
def exclusive(A, zero, combine, node):
    n = len(A)
    exclusiveA = [zero] * n
    for bit in range(n.bit_length())[::-1]:
        for i in range(n)[::-1]:
            exclusiveA[i] = exclusiveA[i // 2]
        for i in range(n & ~+(bit == 0)):
            ind = (i >> bit) ^ 1
            exclusiveA[ind] = combine(exclusiveA[ind], A[i], node, i)
    return exclusiveA

def rerooter(graph, default, combine, finalize=lambda nodeDP,node,eind: nodeDP):
    n = len(graph)
    rootDP = [0] * n
    forwardDP = [None] * n
    reverseDP = [None] * n

    DP = [0] * n
    bfs = [0]
    P = [-1] * n

    for node in bfs:
        for nei in graph[node]:
            if nei == P[node]: continue
            P[nei] = node
            bfs.append(nei)

    for node in reversed(bfs):
        nodeDP = default[node]
        for eind, nei in enumerate(graph[node]):
            if nei == P[node]: continue
            nodeDP = combine(nodeDP, DP[nei], node, eind)
        parent_index = graph[node].index(P[node]) if P[node] != -1 else -1
        DP[node] = finalize(nodeDP, node, parent_index)

    for node in bfs:
        if P[node] != -1:
            DP[P[node]] = DP[node]

        forwardDP[node] = [DP[nei] for nei in graph[node]]
        rerootDP = exclusive(forwardDP[node], default[node], combine, node)

        reverseDP[node] = [
            finalize(nodeDP, node, eind)
            for eind, nodeDP in enumerate(rerootDP)
        ]

        rootDP[node] = finalize(
            combine(rerootDP[0], forwardDP[node][0], node, 0)
            if len(graph[node]) else default[node],
            node, -1
        )

        for nei, dp in zip(graph[node], reverseDP[node]):
            DP[nei] = dp

    return rootDP, forwardDP, reverseDP


# ========== SOLUTION STARTS HERE ==========

    
def combine(nodeDP, neiDP, node, eind):
    return nodeDP


def finalize(nodeDP, node, eind):
    return nodeDP

n = int(input())
graph = [[] for _ in range(n)]

for _ in range(n-1):
    u,v = map(int,input().split())
    u-=1;v-=1
    graph[u].append(v)
    graph[v].append(u)

#default = [0]*n

#rootDP, forwardDP, reverseDP = rerooter(graph, default, combine, finalize)

#print(*rootDP)
