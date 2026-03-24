import sys
input = lambda: sys.stdin.readline().strip()
inp = lambda: list(map(int, input().split()))
from collections import defaultdict, deque,Counter
import heapq
MOD = 10**9 + 7
INF = 10**18

n = int(input())
graph = [[] for _ in range(n)]

for _ in range(n-1):
    u,v = map(int,input().split())
    u-=1;v-=1
    graph[u].append(v)
    graph[v].append(u)

root = 0
lst = [root]

par = [-1]*n

#bfs

for node in lst:
    for nei in graph[node]:
        if nei!=par[node]:
            par[nei]=node
            lst.append(nei)

#the two maximum in subtree of each node with root in 0
#thus answer only for sure at root=0
max1 = [0]*n
max2 = [0]*n

for node in lst[::-1]:
    for nei in graph[node]:
        if nei!=par[node]:
            new_v = 1+max1[nei]
            if new_v>max1[node]:
                max2[node] = max1[node]
                max1[node] = new_v
            elif new_v>max2[node]:
                max2[node] = new_v

#above solves question only for the root, now we go down in tree
# to solve for the rest of the nodes. that is
#reroot

for node in lst:
    #skip root
    if par[node]==-1:continue
    pa = par[node]
    if max1[pa]==(max1[node]+1):
        new_v = max2[pa]+1
    else:
        new_v = max1[pa]+1

    if new_v>max1[node]:
        max2[node] = max1[node]
        max1[node] = new_v
    elif new_v>max2[node]:
        max2[node] = new_v

print(*max1)



