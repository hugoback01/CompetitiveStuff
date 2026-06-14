# Competitive Programming

This repository contains a very little portion of my solutions from competitive programming platforms and contests. I have solved over 1100 problems across many plattforms, thus gained an increadibly problems solving mindset.

## Profiles

* Codeforces: [hugoback01](https://codeforces.com/profile/hugoback01)
* AtCoder: [hugoback01](https://atcoder.jp/)

## Platforms


### Codeforces

Codeforces is my main platform for competitive programming contests. It features regular rated contests (Div.1–Div.4) and a strong problem archive.

What I use Codeforces for:
- Timed contests under pressure
- Learning new algorithms and tricks from editorials
- Practicing implementation speed and accuracy
- Upsolving past contest problems

The difficulty varies a lot, which makes it useful for continuous improvement from beginner level up to advanced algorithmic problems.

---

### CSES

The CSES Problem Set is one of the best collections of algorithmic problems for learning competitive programming. It covers a wide range of topics including:

* Dynamic Programming
* Graph Algorithms
* Trees
* Mathematics
* String Algorithms
* Range Queries

I regularly use CSES to strengthen fundamentals and revisit classic algorithms.

### Kattis

Kattis offers a large archive of contest-style problems used in programming competitions around the world. Many problems focus on implementation and problem-solving speed, making it a great platform for practicing contest performance.

### AtCoder

AtCoder contests are known for their clean problem statements and high-quality tasks. Many problems require discovering elegant observations rather than applying standard templates.

---

# Latest Solve: ARC 222 C — 2 Directions vs 4 Directions

🔗 Problem: https://atcoder.jp/contests/arc222/tasks/arc222_c

---

## Idea Summary

We reduce the problem into a **grid DP with constrained movement directions**.

Instead of simulating the game, we observe that:
- Horizontal movement is the key restriction
- Vertical propagation is handled by DP layers
- The problem becomes combining two directional DP passes

We define a modified cost:
- each cell depends only on its horizontal neighbors

Then compute:
- DP from top → bottom
- DP from bottom → top
- combine results for each cell

---

## Full Solution Code

```python
import sys

input = lambda: sys.stdin.readline().strip()
inp = lambda: list(map(int, input().split()))

INF = 10**18


def solve():
    (n,) = inp()
    A = [inp() for _ in range(n)]

    # compute local horizontal cost contribution
    cost = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if j - 1 >= 0:
                cost[i][j] += A[i][j - 1]
            if j + 1 < n:
                cost[i][j] += A[i][j + 1]

    # DP from top
    up_dp = [[INF] * n for _ in range(n)]
    for j in range(n):
        up_dp[0][j] = cost[0][j]

    for i in range(1, n):
        for j in range(n):
            best = INF
            if j - 1 >= 0:
                best = min(best, up_dp[i - 1][j - 1])
            if j + 1 < n:
                best = min(best, up_dp[i - 1][j + 1])
            up_dp[i][j] = best + cost[i][j]

    # DP from bottom
    down_dp = [[INF] * n for _ in range(n)]
    for j in range(n):
        down_dp[n - 1][j] = cost[n - 1][j]

    for i in range(n - 2, -1, -1):
        for j in range(n):
            best = INF
            if j - 1 >= 0:
                best = min(best, down_dp[i + 1][j - 1])
            if j + 1 < n:
                best = min(best, down_dp[i + 1][j + 1])
            down_dp[i][j] = best + cost[i][j]

    # combine both directions
    ans = [[INF] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if j - 1 >= 0:
                ans[i][j] = min(
                    ans[i][j],
                    up_dp[i][j - 1] + down_dp[i][j - 1] - cost[i][j - 1],
                )
            if j + 1 < n:
                ans[i][j] = min(
                    ans[i][j],
                    up_dp[i][j + 1] + down_dp[i][j + 1] - cost[i][j + 1],
                )

    for row in ans:
        print(*row)


t = int(input())
for _ in range(t):
    solve() ```
