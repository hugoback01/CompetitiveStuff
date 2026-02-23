
class FenwickTree:
   def __init__(self, n):
       self.n = n
       self.bit = [0] * (n + 1)
  
   def add(self, idx, val):
       idx += 1  # BIT is 1-indexed
       while idx <= self.n:
           self.bit[idx] += val
           idx += idx & -idx
  
   def prefix_sum(self, idx):
       idx += 1  # BIT is 1-indexed
       res = 0
       while idx > 0:
           res += self.bit[idx]
           idx -= idx & -idx
       return res


def euler_tour(tree, root=0):
   n = len(tree)
   in_time = [0] * n
   out_time = [0] * n
   par = [-1] * n
   timer = 0
   stack = [(root, -1, False)]
  
   while stack:
       u, parent, visited_children = stack.pop()
      
       if not visited_children:
           in_time[u] = timer
           timer += 1
           stack.append((u, parent, True))
           for v in reversed(tree[u]):
               if v != parent:
                   par[v] = u
                   stack.append((v, u, False))
       else:
           out_time[u] = timer - 1


   return in_time, out_time, par


# Example usage:
n = 7
edges = [
   (0, 1), (0, 2),
   (1, 3), (1, 4),
   (2, 5), (2, 6)
]


# Build adjacency list
tree = [[] for _ in range(n)]
for u, v in edges:
   tree[u].append(v)
   tree[v].append(u)


in_time, out_time = euler_tour(tree, root=0)
ft = FenwickTree(n)


# Add +1 to subtree rooted at node 1
u = 1
ft.add(in_time[u], 1)
ft.add(out_time[u] + 1, -1)


# Query value at node 3 (should reflect the update from node 1)
print(ft.prefix_sum(in_time[3]))  # Output: 1


# Subtract 1 from subtree rooted at node 1
ft.add(in_time[u], -1)
ft.add(out_time[u] + 1, 1)


print(ft.prefix_sum(in_time[3]))  # Output: 0
