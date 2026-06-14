import sys
import typing

# =============================================================================
# QUICK EXAMPLE: Strongly Connected Components (SCC)
# =============================================================================
#
# # 1. Initialize a directed graph with 6 vertices (indexed 0 to 5)
# graph = SCCGraph(6)
# 
# # 2. Add edges to form a cycle between vertices 1, 2, and 4
# graph.add_edge(1, 4)
# graph.add_edge(4, 2)
# graph.add_edge(2, 1)
# 
# # 3. Add edges to form another cycle between vertices 3 and 5
# graph.add_edge(3, 5)
# graph.add_edge(5, 3)
# 
# # 4. Add a cross-edge connecting the first group to the second group
# graph.add_edge(2, 3)
# 
# # 5. Calculate the Strongly Connected Components
# sccs = graph.scc()
# 
# # Output will be a list of components, sorted in topological order.
# # Vertices in the same cycle are grouped together.
# # Expected output: [[0], [1, 4, 2], [3, 5]]
# print("Strongly Connected Components:", sccs)
# =============================================================================


class CSR:
    """
    Compressed Sparse Row (CSR) format representation for a graph.
    This provides a highly cache-efficient way to store directed edges.
    """
    def __init__(
            self, n: int, edges: typing.List[typing.Tuple[int, int]]) -> None:
        self.start = [0] * (n + 1)
        self.elist = [0] * len(edges)

        # Count the out-degree of each vertex
        for e in edges:
            self.start[e[0] + 1] += 1

        # Prefix sums to find the starting index for each vertex's adjacency list
        for i in range(1, n + 1):
            self.start[i] += self.start[i - 1]

        # Populate the edge list
        counter = self.start.copy()
        for e in edges:
            self.elist[counter[e[0]]] = e[1]
            counter[e[0]] += 1


class SCCGraph:
    """
    Finds Strongly Connected Components (SCC) in a directed graph using 
    Tarjan's Depth-First Search Algorithm.
    Time Complexity: O(V + E) where V is vertices and E is edges.
    """

    def __init__(self, n: int) -> None:
        """
        Initializes the graph with `n` vertices (0-indexed).
        """
        self._n = n
        self._edges: typing.List[typing.Tuple[int, int]] = []

    def num_vertices(self) -> int:
        """Returns the number of vertices in the graph."""
        return self._n

    def add_edge(self, from_vertex: int, to_vertex: int) -> None:
        """Adds a directed edge from `from_vertex` to `to_vertex`."""
        assert 0 <= from_vertex < self._n
        assert 0 <= to_vertex < self._n
        self._edges.append((from_vertex, to_vertex))

    def scc_ids(self) -> typing.Tuple[int, typing.List[int]]:
        """
        Internal mapping logic.
        Returns a tuple: (number_of_components, component_id_for_each_vertex)
        """
        g = CSR(self._n, self._edges)
        now_ord = 0
        group_num = 0
        visited = []
        low = [0] * self._n
        order = [-1] * self._n
        ids = [0] * self._n

        # Dynamically increase recursion limit to handle deep graphs
        sys.setrecursionlimit(max(self._n + 1000, sys.getrecursionlimit()))

        def dfs(v: int) -> None:
            nonlocal now_ord
            nonlocal group_num
            nonlocal visited
            nonlocal low
            nonlocal order
            nonlocal ids

            low[v] = now_ord
            order[v] = now_ord
            now_ord += 1
            visited.append(v)
            
            # Iterate through all outgoing edges from vertex v
            for i in range(g.start[v], g.start[v + 1]):
                to = g.elist[i]
                if order[to] == -1:
                    dfs(to)
                    low[v] = min(low[v], low[to])
                else:
                    low[v] = min(low[v], order[to])

            # If the lowest reachable vertex is itself, we found an SCC root
            if low[v] == order[v]:
                while True:
                    u = visited[-1]
                    visited.pop()
                    order[u] = self._n
                    ids[u] = group_num
                    if u == v:
                        break
                group_num += 1

        # Run DFS for all unvisited vertices
        for i in range(self._n):
            if order[i] == -1:
                dfs(i)

        # Reverse the IDs so the components are topologically sorted
        for i in range(self._n):
            ids[i] = group_num - 1 - ids[i]

        return group_num, ids

    def scc(self) -> typing.List[typing.List[int]]:
        """
        Groups the vertices into Strongly Connected Components.
        Returns a list of components, where each component is a list of vertex IDs.
        The returned list is sorted in topological order (a vertex in earlier components 
        may have an edge pointing to a later component, but never the reverse).
        """
        group_num, ids = self.scc_ids()
        
        counts = [0] * group_num
        for x in ids:
            counts[x] += 1
            
        groups: typing.List[typing.List[int]] = [[] for _ in range(group_num)]
        for i in range(self._n):
            groups[ids[i]].append(i)

        return groups
