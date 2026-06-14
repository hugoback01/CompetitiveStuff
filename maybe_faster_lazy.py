class LazySegTree:

    def __init__(self, op, e_node, mapping, composition, e_lazy, a):
        self.n = len(a)
        self.size = 1
        self.height = 0
        self.e_node = e_node
        self.e_lazy = e_lazy
        self.op = op
        self.mapping = mapping
        self.composition = composition
        while self.size < self.n:
            self.size <<= 1
            self.height += 1
        self.node = [self.e_node] * (self.size * 2)
        self.lazy = [self.e_lazy] * (self.size * 2)
        for idx, val in enumerate(a, self.size):
            self.node[idx] = val
        for idx in range(self.size - 1, 0, -1):
            self.node[idx] = self.op(self.node[idx << 1], self.node[idx << 1 | 1])

    def apply_f(self, f, idx):
        self.node[idx] = self.mapping(f, self.node[idx])
        if idx < self.size:
            self.lazy[idx] = self.composition(f, self.lazy[idx])

    def propagate(self, idx):
        for d in range(self.height, 0, -1):
            p = idx >> d
            if self.lazy[p] == self.e_lazy:
                continue
            self.apply_f(self.lazy[p], p << 1)
            self.apply_f(self.lazy[p], p << 1 | 1)
            self.lazy[p] = self.e_lazy

    def back_propagate(self, idx):
        idx >>= 1
        while idx > 0:
            self.node[idx] = self.mapping(
                self.lazy[idx], self.op(self.node[idx << 1], self.node[idx << 1 | 1])
            )
            idx >>= 1

    def apply(self, l, r, f):
        l += self.size
        r += self.size
        l0, r0 = l, r - 1
        self.propagate(l)
        self.propagate(r - 1)
        while l < r:
            if l & 1:
                l_val = self.apply_f(f, l)
                l += 1
            if r & 1:
                r_val = self.apply_f(f, r - 1)
            l >>= 1
            r >>= 1
        self.back_propagate(l0)
        self.back_propagate(r0)

    def query(self, l, r):
        l += self.size
        r += self.size
        self.propagate(l)
        self.propagate(r - 1)
        l_val = r_val = self.e_node
        while l < r:
            if l & 1:
                l_val = self.op(l_val, self.node[l])
                l += 1
            if r & 1:
                r_val = self.op(self.node[r - 1], r_val)
            l >>= 1
            r >>= 1
        return self.op(l_val, r_val)
