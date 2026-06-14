import typing

# =============================================================================
# QUICK EXAMPLE: Point Update and Range Sum Query
# =============================================================================
#
# # 1. op: How do we combine two elements? (We want the sum)
# def op(x, y):
#     return x + y
# 
# # 2. e: The identity element for 'sum'
# e = 0
# 
# # Initialize an array of size 5
# initial_array = [1, 2, 3, 4, 5]
# tree = SegTree(op, e, initial_array)
# 
# # Query sum in range [0, 3) -> sum(1, 2, 3) = 6
# print("Sum in range [0, 3):", tree.prod(0, 3)) 
# 
# # Update index 2 to value 10 -> array becomes [1, 2, 10, 4, 5]
# tree.set(2, 10)
# 
# # Query sum in range [0, 3) -> sum(1, 2, 10) = 13
# print("Sum in range [0, 3) after update:", tree.prod(0, 3)) 
# 
# # Query sum of the whole array -> sum(1, 2, 10, 4, 5) = 22
# print("Total sum:", tree.all_prod())
# =============================================================================


class SegTree:
    """
    A self-contained Segment Tree for efficient range queries and point updates.
    Time Complexity: O(log n) for updates and queries.
    """
    def __init__(self,
                 op: typing.Callable[[typing.Any, typing.Any], typing.Any],
                 e: typing.Any,
                 v: typing.Union[int, typing.List[typing.Any]]) -> None:
        """
        Parameters:
        - op: Binary operation used to combine two elements (e.g., operator.add, max, min).
        - e: The identity element for `op` (e.g., 0 for sum, float('-inf') for max).
        - v: Either an integer (creates an array of that size initialized with `e`), or a list of initial values.
        """
        self._op = op
        self._e = e

        # If an integer is passed, initialize an array of that size with the identity element
        if isinstance(v, int):
            v = [e] * v

        self._n = len(v)
        
        # Calculate _log and _size (replacing the atcoder._bit._ceil_pow2 dependency)
        self._log = 0
        while (1 << self._log) < self._n:
            self._log += 1
            
        self._size = 1 << self._log
        self._d = [e] * (2 * self._size)  # The segment tree array

        # Initialize the leaf nodes with the provided array values
        for i in range(self._n):
            self._d[self._size + i] = v[i]
            
        # Build the tree bottom-up
        for i in range(self._size - 1, 0, -1):
            self._update(i)

    def set(self, p: int, x: typing.Any) -> None:
        """Sets the element at index `p` to value `x`."""
        assert 0 <= p < self._n

        p += self._size
        self._d[p] = x
        
        # Update the path back up to the root
        for i in range(1, self._log + 1):
            self._update(p >> i)

    def get(self, p: int) -> typing.Any:
        """Returns the current value of the element at index `p`."""
        assert 0 <= p < self._n
        return self._d[p + self._size]

    def prod(self, left: int, right: int) -> typing.Any:
        """Returns the result of `op` applied to the range [left, right)."""
        assert 0 <= left <= right <= self._n
        sml = self._e
        smr = self._e
        left += self._size
        right += self._size

        # Combine the elements in the range
        while left < right:
            if left & 1:
                sml = self._op(sml, self._d[left])
                left += 1
            if right & 1:
                right -= 1
                smr = self._op(self._d[right], smr)
            left >>= 1
            right >>= 1

        return self._op(sml, smr)

    def all_prod(self) -> typing.Any:
        """Returns the result of `op` applied to the entire array."""
        return self._d[1]

    def max_right(self, left: int,
                  f: typing.Callable[[typing.Any], bool]) -> int:
        """
        Binary search on the tree.
        Returns the largest index `r` such that `f(op(a[left], ..., a[r-1]))` is True.
        """
        assert 0 <= left <= self._n
        assert f(self._e)

        if left == self._n:
            return self._n

        left += self._size
        sm = self._e

        first = True
        while first or (left & -left) != left:
            first = False
            while left % 2 == 0:
                left >>= 1
            if not f(self._op(sm, self._d[left])):
                while left < self._size:
                    left *= 2
                    if f(self._op(sm, self._d[left])):
                        sm = self._op(sm, self._d[left])
                        left += 1
                return left - self._size
            sm = self._op(sm, self._d[left])
            left += 1

        return self._n

    def min_left(self, right: int,
                 f: typing.Callable[[typing.Any], bool]) -> int:
        """
        Binary search on the tree.
        Returns the smallest index `l` such that `f(op(a[l], ..., a[right-1]))` is True.
        """
        assert 0 <= right <= self._n
        assert f(self._e)

        if right == 0:
            return 0

        right += self._size
        sm = self._e

        first = True
        while first or (right & -right) != right:
            first = False
            right -= 1
            while right > 1 and right % 2:
                right >>= 1
            if not f(self._op(self._d[right], sm)):
                while right < self._size:
                    right = 2 * right + 1
                    if f(self._op(self._d[right], sm)):
                        sm = self._op(self._d[right], sm)
                        right -= 1
                return right + 1 - self._size
            sm = self._op(self._d[right], sm)

        return 0

    def _update(self, k: int) -> None:
        """Internal: Recalculates the value of a node based on its children."""
        self._d[k] = self._op(self._d[2 * k], self._d[2 * k + 1])
