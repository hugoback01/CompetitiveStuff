import sys
input = lambda: sys.stdin.readline().strip()
inp = lambda: list(map(int, input().split()))
from collections import defaultdict, deque,Counter
import heapq
MOD = 10**9 + 7
INF = 10**18

n, = inp()
graph = [[] for _ in range(n)]

for _ in range(n-1):
    u,v = inp()
    u-=1;v-=1
    graph[u].append(v)
    graph[v].append(u)


par = [-1]*n

lst = [0]

for e in lst:
    for nei in graph[e]:
        if nei!=par[e]:
            lst.append(nei)
            par[nei]=e

dp = [0]*n
sz = [1]*n

for e in lst[::-1]:
    for ch in graph[e]:
        if ch==par[e]:continue
        dp[e] += dp[ch]+sz[ch]
        sz[e] += sz[ch]

for e in lst:
    if par[e]==-1:
        continue

    dp[e] += (dp[par[e]]-dp[e]-sz[e]) + (n-sz[e])

print(*dp)
"""
Reroot solution
def combine(nodeDP, neiDP, node, eind):
    curr_d, curr_sz = nodeDP
    chi_d,chi_sz = neiDP
    return (curr_d+chi_d+chi_sz, curr_sz+chi_sz)
 
def finalize(nodeDP, node, eind):
    return nodeDP

"""

""
