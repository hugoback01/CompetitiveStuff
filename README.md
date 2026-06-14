# Competitive Programming

This repository contains my solutions, notes, and occasional writeups from competitive programming platforms and contests.

## Profiles

* Codeforces: [Your Codeforces Profile](YOUR_CODEFORCES_LINK)
* AtCoder: [Your AtCoder Profile](YOUR_ATCODER_LINK)

## Platforms

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

# Latest Solve: ARC 222 C

Problem:
https://atcoder.jp/contests/arc222/tasks/arc222_c

### Short Statement

Given an (n \times n) grid, compute for every cell the minimum cost of constructing a valid diagonal path from the top row to the bottom row while avoiding that specific cell.

### Key Observation

For each cell, only its left and right neighbors contribute to the local cost:

```python
cost[i][j] =
    grid[i][j-1] +
    grid[i][j+1]
```

This allows us to transform the original problem into a shortest-path style dynamic programming problem.

### Step 1: DP From Top

Let

```python
up_dp[i][j]
```

be the minimum cost of a valid diagonal path from the first row to cell `(i,j)`.

Transitions:

```python
up_dp[i][j] =
    min(
        up_dp[i-1][j-1],
        up_dp[i-1][j+1]
    )
    + cost[i][j]
```

### Step 2: DP From Bottom

Similarly,

```python
down_dp[i][j]
```

stores the minimum cost from cell `(i,j)` to the last row.

Transitions are identical but processed in reverse order.

### Step 3: Remove One Cell

Suppose we want the answer for cell `(i,j)`.

A valid path cannot pass through this cell, so it must go through either:

```python
(i, j-1)
```

or

```python
(i, j+1)
```

We combine the best path from above and below:

```python
up_dp + down_dp - cost
```

The subtraction avoids counting the middle cell twice.

### Complexity

```text
Time:  O(n²)
Space: O(n²)
```

The solution performs only a few DP passes over the grid.

## Repository Structure

```text
atcoder/
codeforces/
cses/
kattis/
notes/
```

I primarily write solutions in Python and occasionally include short editorials for interesting problems.
