import typing

# =============================================================================
# QUICK EXAMPLE: Polynomial Multiplication / Convolution
# =============================================================================
#
# # Example 1: Standard Integer Convolution (No overflow, works for any size)
# poly_a = [1, 2, 3]  # represents 1 + 2x + 3x^2
# poly_b = [1, 1, 1]  # represents 1 + x + x^2
# 
# result = convolution_int(poly_a, poly_b)
# # Expected output: [1, 3, 6, 5, 3]
# # (1*1) + (1*1 + 2*1)x + (1*1 + 2*1 + 3*1)x^2 + (2*1 + 3*1)x^3 + (3*1)x^4
# print("Integer Convolution Result:", result)
#
# # Example 2: Convolution modulo 998244353
# MOD = 998244353
# result_mod = convolution(MOD, poly_a, poly_b)
# print("Modular Convolution Result:", result_mod)
# =============================================================================


# -----------------------------------------------------------------------------
# Internal Helper Functions (Replacing atcoder internal modules)
# -----------------------------------------------------------------------------

def _ceil_pow2(n: int) -> int:
    """Returns the smallest exponent `x` such that 2^x >= n."""
    x = 0
    while (1 << x) < n:
        x += 1
    return x


def _bsf(x: int) -> int:
    """Bit Scan Forward: Returns the number of trailing zeros in the binary of x."""
    return (x & -x).bit_length() - 1


def _inv_gcd(a: int, b: int) -> typing.Tuple[int, int]:
    """Extended Euclidean Algorithm to find modular inverse."""
    a = a % b
    if a == 0:
        return b, 0
    s = b
    t = a
    m0, m1 = 0, 1
    while t:
        u = s // t
        s -= u * t
        m0 -= u * m1
        s, t = t, s
        m0, m1 = m1, m0
    if m0 < 0:
        m0 += b // s
    return s, m0


def _primitive_root(m: int) -> int:
    """Finds a primitive root modulo m (optimized for standard NTT moduli)."""
    if m == 2:
        return 1
    if m in (167772161, 469762049, 754974721, 998244353):
        return 3
    
    # Fallback primitive root finder
    divs = []
    x = m - 1
    i = 2
    while i * i <= x:
        if x % i == 0:
            divs.append(i)
            while x % i == 0:
                x //= i
        i += 1
    if x > 1:
        divs.append(x)
    g = 2
    while True:
        ok = True
        for d in divs:
            if pow(g, (m - 1) // d, m) == 1:
                ok = False
                break
        if ok:
            return g
        g += 1


# -----------------------------------------------------------------------------
# Modular Arithmetic Context and Object Wrapper
# -----------------------------------------------------------------------------

class ModContext:
    """Manages the current active modulus context."""
    _current_mod = 998244353

    def __init__(self, mod: int) -> None:
        self.mod = mod
        self.prev_mod = 998244353

    def __enter__(self) -> "ModContext":
        self.prev_mod = ModContext._current_mod
        ModContext._current_mod = self.mod
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        ModContext._current_mod = self.prev_mod


class Modint:
    """Lightweight representation of an integer modulo the active ModContext."""
    def __init__(self, v: int = 0) -> None:
        self._mod = ModContext._current_mod
        self._v = int(v) % self._mod

    def mod(self) -> int:
        return self._mod

    def val(self) -> int:
        return self._v

    def inv(self) -> "Modint":
        g, x = _inv_gcd(self._v, self._mod)
        return Modint(x)

    def __add__(self, other: typing.Any) -> "Modint":
        o = other.val() if isinstance(other, Modint) else int(other)
        return Modint(self._v + o)

    def __sub__(self, other: typing.Any) -> "Modint":
        o = other.val() if isinstance(other, Modint) else int(other)
        return Modint(self._v - o)

    def __mul__(self, other: typing.Any) -> "Modint":
        o = other.val() if isinstance(other, Modint) else int(other)
        return Modint(self._v * o)

    def __pow__(self, n: int) -> "Modint":
        return Modint(pow(self._v, int(n), self._mod))

    def __imul__(self, other: typing.Any) -> "Modint":
        o = other.val() if isinstance(other, Modint) else int(other)
        self._v = (self._v * o) % self._mod
        return self


# -----------------------------------------------------------------------------
# Butterfly / NTT Algorithm Core
# -----------------------------------------------------------------------------

_sum_e: typing.Dict[int, typing.List[Modint]] = {}
_sum_ie: typing.Dict[int, typing.List[Modint]] = {}


def _butterfly(a: typing.List[Modint]) -> None:
    """In-place Number Theoretic Transform (Forward Butterfly)."""
    g = _primitive_root(a[0].mod())
    n = len(a)
    h = _ceil_pow2(n)

    if a[0].mod() not in _sum_e:
        es = [Modint(0)] * 30
        ies = [Modint(0)] * 30
        cnt2 = _bsf(a[0].mod() - 1)
        e = Modint(g) ** ((a[0].mod() - 1) >> cnt2)
        ie = e.inv()
        for i in range(cnt2, 1, -1):
            es[i - 2] = e
            ies[i - 2] = ie
            e = e * e
            ie = ie * ie
        sum_e = [Modint(0)] * 30
        now = Modint(1)
        for i in range(cnt2 - 2):
            sum_e[i] = es[i] * now
            now *= ies[i]
        _sum_e[a[0].mod()] = sum_e
    else:
        sum_e = _sum_e[a[0].mod()]

    for ph in range(1, h + 1):
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        now = Modint(1)
        for s in range(w):
            offset = s << (h - ph + 1)
            for i in range(p):
                left = a[i + offset]
                right = a[i + offset + p] * now
                a[i + offset] = left + right
                a[i + offset + p] = left - right
            now *= sum_e[_bsf(~s)]


def _butterfly_inv(a: typing.List[Modint]) -> None:
    """In-place Inverse Number Theoretic Transform (Inverse Butterfly)."""
    g = _primitive_root(a[0].mod())
    n = len(a)
    h = _ceil_pow2(n)

    if a[0].mod() not in _sum_ie:
        es = [Modint(0)] * 30
        ies = [Modint(0)] * 30
        cnt2 = _bsf(a[0].mod() - 1)
        e = Modint(g) ** ((a[0].mod() - 1) >> cnt2)
        ie = e.inv()
        for i in range(cnt2, 1, -1):
            es[i - 2] = e
            ies[i - 2] = ie
            e = e * e
            ie = ie * ie
        sum_ie = [Modint(0)] * 30
        now = Modint(1)
        for i in range(cnt2 - 2):
            sum_ie[i] = ies[i] * now
            now *= es[i]
        _sum_ie[a[0].mod()] = sum_ie
    else:
        sum_ie = _sum_ie[a[0].mod()]

    for ph in range(h, 0, -1):
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        inow = Modint(1)
        for s in range(w):
            offset = s << (h - ph + 1)
            for i in range(p):
                left = a[i + offset]
                right = a[i + offset + p]
                a[i + offset] = left + right
                a[i + offset + p] = Modint(
                    (a[0].mod() + left.val() - right.val()) * inow.val())
            inow *= sum_ie[_bsf(~s)]


# -----------------------------------------------------------------------------
# Primary Exposed Convolution Interfaces
# -----------------------------------------------------------------------------

def convolution_mod(a: typing.List[Modint],
                    b: typing.List[Modint]) -> typing.List[Modint]:
    """Computes convolution under a predefined active ModContext environment."""
    n = len(a)
    m = len(b)

    if n == 0 or m == 0:
        return []

    # O(N*M) Native fallback for tiny inputs to bypass transform overheads
    if min(n, m) <= 60:
        if n < m:
            n, m = m, n
            a, b = b, a
        ans = [Modint(0) for _ in range(n + m - 1)]
        for i in range(n):
            for j in range(m):
                ans[i + j] += a[i] * b[j]
        return ans

    z = 1 << _ceil_pow2(n + m - 1)

    while len(a) < z:
        a.append(Modint(0))
    _butterfly(a)

    while len(b) < z:
        b.append(Modint(0))
    _butterfly(b)

    for i in range(z):
        a[i] *= b[i]
    _butterfly_inv(a)
    a = a[:n + m - 1]

    iz = Modint(z).inv()
    for i in range(n + m - 1):
        a[i] *= iz

    return a


def convolution(mod: int, a: typing.List[typing.Any],
                b: typing.List[typing.Any]) -> typing.List[typing.Any]:
    """Computes the multiplication of two polynomials modulo `mod`."""
    n = len(a)
    m = len(b)

    if n == 0 or m == 0:
        return []

    with ModContext(mod):
        a2 = list(map(Modint, a))
        b2 = list(map(Modint, b))

        return list(map(lambda c: c.val(), convolution_mod(a2, b2)))


def convolution_int(
        a: typing.List[int], b: typing.List[int]) -> typing.List[int]:
    """
    Computes standard integer polynomial multiplication without overflow constraints.
    Employs the Chinese Remainder Theorem (CRT) across three large NTT-friendly prime fields.
    """
    n = len(a)
    m = len(b)

    if n == 0 or m == 0:
        return []

    mod1 = 754974721  # 2^24 * 45 + 1
    mod2 = 167772161  # 2^25 * 5 + 1
    mod3 = 469762049  # 2^26 * 7 + 1
    m2m3 = mod2 * mod3
    m1m3 = mod1 * mod3
    m1m2 = mod1 * mod2
    m1m2m3 = mod1 * mod2 * mod3

    i1 = _inv_gcd(mod2 * mod3, mod1)[1]
    i2 = _inv_gcd(mod1 * mod3, mod2)[1]
    i3 = _inv_gcd(mod1 * mod2, mod3)[1]

    c1 = convolution(mod1, a, b)
    c2 = convolution(mod2, a, b)
    c3 = convolution(mod3, a, b)

    c = [0] * (n + m - 1)
    for i in range(n + m - 1):
        c[i] += (c1[i] * i1) % mod1 * m2m3
        c[i] += (c2[i] * i2) % mod2 * m1m3
        c[i] += (c3[i] * i3) % mod3 * m1m2
        c[i] %= m1m2m3

    return c
