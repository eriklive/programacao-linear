\ Model
\ minimize total distance
\ subject to capacity and distance constraints

Minimize
    sum{i in 1..n} sum{j in 1..n} c[i,j] * x[i,j]

Subject To
 \ capacity constraint
 c1: sum{j in 1..n : j != i} d[j] * x[i,j] <= Q
   for i in 2..n

 \ distance constraint
 c2: sum{j in 1..n} x[i,j] = 1
   for i in 1..n
 c3: sum{i in 1..n} x[i,j] = 1
   for j in 1..n
 c4: sum{j in 1..n} x[1,j] = 1
 c5: sum{i in 2..n} x[i,n+1] = 1

Bounds
 0 <= x[i,j] <= 1
   for i in 1..n, j in 1..n

Integers
 x[i,j]
   for i in 1..n, j in 1..n
