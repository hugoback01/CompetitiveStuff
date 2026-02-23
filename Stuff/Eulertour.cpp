#include <bits/stdc++.h>
using namespace std;

class FenwickTree {
    int n;
    vector<long long> bit;

public:
    FenwickTree(int n) : n(n), bit(n + 1, 0) {}

    // Add value to index idx (0-based index)
    void add(int idx, long long val) {
        idx++; // convert to 1-based indexing
        while (idx <= n) {
            bit[idx] += val;
            idx += idx & -idx;
        }
    }

    // Get prefix sum [0..idx] (0-based index)
    long long prefix_sum(int idx) {
        idx++; // convert to 1-based indexing
        long long res = 0;
        while (idx > 0) {
            res += bit[idx];
            idx -= idx & -idx;
        }
        return res;
    }
};

// Iterative Euler Tour
void euler_tour(
    const vector<vector<int>>& tree,
    int root,
    vector<int>& in_time,
    vector<int>& out_time,
    vector<int>& parent
) {
    int n = tree.size();
    in_time.assign(n, 0);
    out_time.assign(n, 0);
    parent.assign(n, -1);

    int timer = 0;
    stack<tuple<int,int,bool>> st;
    st.push({root, -1, false});

    while (!st.empty()) {
        auto [u, par, visited_children] = st.top();
        st.pop();

        if (!visited_children) {
            in_time[u] = timer++;
            st.push({u, par, true});

            for (int i = tree[u].size() - 1; i >= 0; i--) {
                int v = tree[u][i];
                if (v != par) {
                    parent[v] = u;
                    st.push({v, u, false});
                }
            }
        } else {
            out_time[u] = timer - 1;
        }
    }
}

int main() {
    int n = 7;

    vector<pair<int,int>> edges = {
        {0,1}, {0,2},
        {1,3}, {1,4},
        {2,5}, {2,6}
    };

    // Build adjacency list
    vector<vector<int>> tree(n);
    for (auto [u, v] : edges) {
        tree[u].push_back(v);
        tree[v].push_back(u);
    }

    vector<int> in_time, out_time, parent;
    euler_tour(tree, 0, in_time, out_time, parent);

    FenwickTree ft(n);

    // Add +1 to subtree rooted at node 1
    int u = 1;
    ft.add(in_time[u], 1);
    ft.add(out_time[u] + 1, -1);

    // Query value at node 3 (should be 1)
    cout << ft.prefix_sum(in_time[3]) << endl;

    // Subtract 1 from subtree rooted at node 1
    ft.add(in_time[u], -1);
    ft.add(out_time[u] + 1, 1);

    cout << ft.prefix_sum(in_time[3]) << endl;

    return 0;
}
