import typing

# =============================================================================
# QUICK EXAMPLE: Persistent Point Update and Range Sum Query
# =============================================================================
#
# def op(x, y):
#     return x + y
#
# e = 0
#
# # Initialize with a list or an integer: e.g., PersistentSegTree(op, e, [1, 2, 3, 4, 5])
# tree = PersistentSegTree(op, e, 5) # Creates [0, 0, 0, 0, 0]
#
# # Update index 2 to 10 in the latest version -> creates Version 1
# tree.set(2, 10)
#
# # Query version 0 (original) vs version 1 (updated)
# print(tree.prod(0, 5, version=0)) # Output: 0
# print(tree.prod(0, 5, version=1)) # Output: 10
# =============================================================================


class Node:
    __slots__ = ["val", "left", "right"]

    def __init__(
        self,
        val: typing.Any,
        left: typing.Optional["Node"] = None,
        right: typing.Optional["Node"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right


class PersistentSegTree:
    """A generalized, fully iterative Persistent Segment Tree matching the AtCoder Library interface."""

    def __init__(
        self,
        op: typing.Callable[[typing.Any, typing.Any], typing.Any],
        e: typing.Any,
        v: typing.Union[int, typing.List[typing.Any]],
    ) -> None:
        """Parameters:

        - op: Binary operation used to combine two elements.
        - e: The identity element for `op`.
        - v: Either an integer (creates an array of that size initialized with
        `e`), or a list of initial values.
        """
        self._op = op
        self._e = e

        if isinstance(v, int):
            v = [e] * v

        self._n = len(v)

        # Empty tree guard
        if self._n == 0:
            self.history: typing.List[Node] = [Node(e)]
            return

        # Build the initial tree (Version 0) purely iteratively
        self.history = [self._build_iter(v)]

    def _build_iter(self, v: typing.List[typing.Any]) -> Node:
        """Internal: Iteratively constructs the initial segment tree base."""
        stack = [(0, self._n - 1)]
        nodes: typing.Dict[typing.Tuple[int, int], Node] = {}
        order = []

        while stack:
            curr_l, curr_r = stack.pop()
            order.append((curr_l, curr_r))
            if curr_l < curr_r:
                mid = (curr_l + curr_r) // 2
                stack.append((curr_l, mid))
                stack.append((mid + 1, curr_r))

        while order:
            curr_l, curr_r = order.pop()
            if curr_l == curr_r:
                nodes[(curr_l, curr_r)] = Node(v[curr_l])
            else:
                mid = (curr_l + curr_r) // 2
                left = nodes[(curr_l, mid)]
                right = nodes[(mid + 1, curr_r)]
                nodes[(curr_l, curr_r)] = Node(
                    self._op(left.val, right.val), left, right
                )

        return nodes[(0, self._n - 1)]

    def set(self, p: int, x: typing.Any) -> None:
        """Creates a new tree version by setting the element at index `p` to

        value `x`.
        """
        assert 0 <= p < self._n

        root = self.history[-1]
        l, r = 0, self._n - 1
        path = []
        curr = root

        # Navigate down to leaf while recording path
        while l < r:
            path.append((curr, l, r))
            mid = (l + r) // 2
            if p <= mid:
                curr = curr.left  # type: ignore
                r = mid
            else:
                curr = curr.right  # type: ignore
                l = mid + 1

        # Reconstruct path upwards creating new cloned nodes
        new_node = Node(x)
        while path:
            parent, pl, pr = path.pop()
            mid = (pl + pr) // 2
            if p <= mid:
                new_node = Node(
                    self._op(new_node.val, parent.right.val),
                    new_node,
                    parent.right,
                )
            else:
                new_node = Node(
                    self._op(parent.left.val, new_node.val),
                    parent.left,
                    new_node,
                )

        self.history.append(new_node)

    def get(self, p: int, version: int = -1) -> typing.Any:
        """Returns the value of the element at index `p` for a specific version

        (defaults to latest).
        """
        assert 0 <= p < self._n

        curr = self.history[version]
        l, r = 0, self._n - 1
        while l < r:
            mid = (l + r) // 2
            if p <= mid:
                curr = curr.left  # type: ignore
                r = mid
            else:
                curr = curr.right  # type: ignore
                l = mid + 1
        return curr.val

    def prod(self, left: int, right: int, version: int = -1) -> typing.Any:
        """Returns the result of `op` applied to the half-open range [left,

        right) for a specific version.
        """
        assert 0 <= left <= right <= self._n
        if left == right:
            return self._e

        ql, qr = left, right - 1
        node = self.history[version]

        stack = [(node, 0, self._n - 1)]
        segments = []

        # Iteratively collect all disjoint segments covering [ql, qr] from left to right
        while stack:
            curr, l, r = stack.pop()
            if ql <= l and r <= qr:
                segments.append(curr.val)
                continue

            mid = (l + r) // 2
            # Push right child first, so left child gets popped and evaluated first
            if qr > mid:
                stack.append((curr.right, mid + 1, r))  # type: ignore
            if ql <= mid:
                stack.append((curr.left, l, mid))  # type: ignore

        # Combine segments linearly to preserve non-commutative operations (like Matrix Multiply)
        res = self._e
        for val in segments:
            res = self._op(res, val)
        return res

    def all_prod(self, version: int = -1) -> typing.Any:
        """Returns the total combined result of the entire array for a specific

        version.
        """
        return self.history[version].val

    def undo(self) -> None:
        """Rolls back the latest version modification."""
        if len(self.history) > 1:
            self.history.pop()
