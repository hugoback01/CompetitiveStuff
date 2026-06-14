import typing

# =============================================================================
# QUICK EXAMPLE: Range Add and Range Max Query
# =============================================================================
#
# # 1. op: How do we combine two elements? (We want the max)
# def op(x, y):
#     return max(x, y)
# 
# # 2. e: The identity for 'max'
# e = float('-inf')
# 
# # 3. mapping: How does an 'add' tag affect an element? (It adds to it)
# def mapping(tag, element):
#     return tag + element
# 
# # 4. composition: How do we combine two 'add' tags? (We sum them)
# def composition(new_tag, old_tag):
#     return new_tag + old_tag
# 
# # 5. id_: The identity for an 'add' tag (Adding 0 does nothing)
# id_ = 0
# 
# # Initialize an array of size 5 with zeros
# initial_array = [0, 0, 0, 0, 0]
# tree = LazySegTree(op, e, mapping, composition, id_, initial_array)
# 
# # Add 5 to range [1, 4) -> array becomes [0, 5, 5, 5, 0]
# tree.apply(1, 4, 5)
# 
# # Query max in range [0, 3) -> max(0, 5, 5) = 5
# print("Max in range [0, 3):", tree.prod(0, 3)) 
# 
# # Add 10 to range [2, 5) -> array becomes [0, 5, 15, 15, 10]
# tree.apply(2, 5, 10)
# 
# # Query max in range [0, 5) -> max(0, 5, 15, 15, 10) = 15
# print("Max in range [0, 5):", tree.prod(0, 5)) 
# =============================================================================


class LazySegTree:
    """
    A self-contained Lazy Segment Tree for efficient range queries and range updates.
    Time Complexity: O(log n) for updates and queries.
    """
    def __init__(
            self,
            op: typing.Callable[[typing.Any, typing.Any], typing.Any],
            e: typing.Any,
            mapping: typing.Callable[[typing.Any, typing.Any], typing.Any],
            composition: typing.Callable[[typing.Any, typing.Any], typing.Any],
            id_: typing.Any,
            v: typing.Union[int, typing.List[typing.Any]]) -> None:
        """
        Parameters:
        - op: Binary operation used to combine two elements (e.g., max, min, operator.add).
        - e: The identity element for `op` (e.g., float('-inf') for max, 0 for sum).
        - mapping: Function applying a lazy tag `f` to an element `x`. Signature: mapping(f, x) -> x'
        - composition: Function combining a new tag `f_new` with an existing tag `f_old`. Signature: composition(f_new, f_old) -> f'
        - id_: The identity element for lazy tags (represents "no operation" / no-op).
        - v: Either an integer (creates an array of that size initialized with `e`), or a list of initial values.
        """
        self._op = op
        self._e = e
        self._mapping = mapping
        self._composition = composition
        self._id = id_

        # If an integer is passed, initialize an array of that size with the identity element
        if isinstance(v, int):
            v = [e] * v

        self._n = len(v)
        
        # Calculate _log and _size (replacing the atcoder._bit._ceil_pow2 dependency)
        self._log = 0
        while (1 << self._log) < self._n:
            self._log += 1
            
        self._size = 1 << self._log
        self._d = [e] * (2 * self._size)         # The segment tree array
        self._lz = [self._id] * self._size       # The lazy tags array

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
        # Push any pending lazy operations down to the leaves
        for i in range(self._log, 0, -1):
            self._push(p >> i)
            
        self._d[p] = x
        
        # Update the path back up to the root
        for i in range(1, self._log + 1):
            self._update(p >> i)

    def get(self, p: int) -> typing.Any:
        """Returns the current value of the element at index `p`."""
        assert 0 <= p < self._n

        p += self._size
        # Push pending lazy operations down to this leaf
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        return self._d[p]

    def prod(self, left: int, right: int) -> typing.Any:
        """Returns the result of `op` applied to the range [left, right)."""
        assert 0 <= left <= right <= self._n

        if left == right:
            return self._e

        left += self._size
        right += self._size

        # Push down lazy tags for the boundaries of our query
        for i in range(self._log, 0, -1):
            if ((left >> i) << i) != left:
                self._push(left >> i)
            if ((right >> i) << i) != right:
                self._push(right >> i)

        sml = self._e
        smr = self._e
        
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

    def apply(self, left: int, right: typing.Optional[int] = None,
              f: typing.Optional[typing.Any] = None) -> None:
        """
        Applies the lazy tag `f` to the range [left, right).
        If `right` is None, applies `f` only to index `left`.
        """
        assert f is not None

        # Single element update
        if right is None:
            p = left
            assert 0 <= left < self._n
            p += self._size
            for i in range(self._log, 0, -1):
                self._push(p >> i)
            self._d[p] = self._mapping(f, self._d[p])
            for i in range(1, self._log + 1):
                self._update(p >> i)
                
        # Range update
        else:
            assert 0 <= left <= right <= self._n
            if left == right:
                return

            left += self._size
            right += self._size

            # Push boundaries down
            for i in range(self._log, 0, -1):
                if ((left >> i) << i) != left:
                    self._push(left >> i)
                if ((right >> i) << i) != right:
                    self._push((right - 1) >> i)

            l2 = left
            r2 = right
            
            # Apply tag to covering nodes
            while left < right:
                if left & 1:
                    self._all_apply(left, f)
                    left += 1
                if right & 1:
                    right -= 1
                    self._all_apply(right, f)
                left >>= 1
                right >>= 1
                
            left = l2
            right = r2

            # Rebuild boundaries upwards
            for i in range(1, self._log + 1):
                if ((left >> i) << i) != left:
                    self._update(left >> i)
                if ((right >> i) << i) != right:
                    self._update((right - 1) >> i)

    def max_right(
            self, left: int, g: typing.Callable[[typing.Any], bool]) -> int:
        """
        Binary search on the tree.
        Returns the largest index `r` such that `g(op(a[left], ..., a[r-1]))` is True.
        """
        assert 0 <= left <= self._n
        assert g(self._e)

        if left == self._n:
            return self._n

        left += self._size
        for i in range(self._log, 0, -1):
            self._push(left >> i)

        sm = self._e
        first = True
        while first or (left & -left) != left:
            first = False
            while left % 2 == 0:
                left >>= 1
            if not g(self._op(sm, self._d[left])):
                while left < self._size:
                    self._push(left)
                    left *= 2
                    if g(self._op(sm, self._d[left])):
                        sm = self._op(sm, self._d[left])
                        left += 1
                return left - self._size
            sm = self._op(sm, self._d[left])
            left += 1

        return self._n

    def min_left(self, right: int, g: typing.Any) -> int:
        """
        Binary search on the tree.
        Returns the smallest index `l` such that `g(op(a[l], ..., a[right-1]))` is True.
        """
        assert 0 <= right <= self._n
        assert g(self._e)

        if right == 0:
            return 0

        right += self._size
        for i in range(self._log, 0, -1):
            self._push((right - 1) >> i)

        sm = self._e
        first = True
        while first or (right & -right) != right:
            first = False
            right -= 1
            while right > 1 and right % 2:
                right >>= 1
            if not g(self._op(self._d[right], sm)):
                while right < self._size:
                    self._push(right)
                    right = 2 * right + 1
                    if g(self._op(self._d[right], sm)):
                        sm = self._op(self._d[right], sm)
                        right -= 1
                return right + 1 - self._size
            sm = self._op(self._d[right], sm)

        return 0

    def _update(self, k: int) -> None:
        """Internal: Recalculates the value of a node based on its children."""
        self._d[k] = self._op(self._d[2 * k], self._d[2 * k + 1])

    def _all_apply(self, k: int, f: typing.Any) -> None:
        """Internal: Applies a tag `f` to a node and accumulates the tag."""
        self._d[k] = self._mapping(f, self._d[k])
        if k < self._size:
            self._lz[k] = self._composition(f, self._lz[k])

    def _push(self, k: int) -> None:
        """Internal: Pushes accumulated tags to children and clears the current tag."""
        self._all_apply(2 * k, self._lz[k])
        self._all_apply(2 * k + 1, self._lz[k])
        self._lz[k] = self._id
