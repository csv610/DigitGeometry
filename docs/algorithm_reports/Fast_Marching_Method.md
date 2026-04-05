# Fast Marching Method

## 1. Overview
The Fast Marching Method (FMM) is a numerical technique for solving boundary value problems of the Eikonal equation, which describes the propagation of an interface (a wave) through a medium. It is an efficient algorithm for computing the travel time or the shortest path from a starting point (source) to all other points in a grid. It is an extension of Dijkstra's algorithm that accounts for the continuous nature of wave propagation.

## 2. Definitions
*   **Eikonal Equation:** $|\nabla T(x)| = 1/F(x)$, where $T(x)$ is the time of arrival and $F(x)$ is the speed of propagation at position $x$.
*   **Source:** The initial set of points from which the wave propagates.
*   **Known, Trial, Far:** The three sets of nodes in the algorithm (similar to the Open and Closed lists in Dijkstra).

## 3. Theory
FMM uses an upwind finite difference scheme to solve the Eikonal equation. The core idea is that the arrival time $T$ at a node can be computed from the arrival times of its neighbors.
On a 2D Cartesian grid, the discrete Eikonal equation is:
$\left[\max(D_x^{-T}, -D_x^{+T}, 0)^2 + \max(D_y^{-T}, -D_y^{+T}, 0)^2\right]^{1/2} = \frac{1}{F_{ij}}$
Where $D_x$ and $D_y$ are the backward and forward finite differences. The algorithm processes nodes in increasing order of $T$, ensuring that the "upwind" information is always available when computing a node's arrival time.

## 4. Pseudo Code
```text
function FastMarching(speed_image, sources)
    time := map with default Infinity
    status := map with default Far
    
    for s in sources
        time[s] := 0
        status[s] := Trial
        push(priority_queue, {s, 0})
        
    while priority_queue is not empty
        {current, t} := priority_queue.popMin()
        status[current] := Known
        
        for neighbor of current
            if status[neighbor] != Known
                // Solve the discrete Eikonal equation for neighbor
                new_time := solveEikonal(neighbor, time, speed_image)
                time[neighbor] := new_time
                if status[neighbor] == Far
                    status[neighbor] := Trial
                push_or_update(priority_queue, {neighbor, new_time})
                
    return time
```

## 5. Parameters Selections
*   **Speed Function ($F(x)$):** The speed of propagation must be non-negative. $F(x) = 1$ leads to the Euclidean distance transform.
*   **Grid Resolution:** FMM is a first-order method; increasing the resolution reduces the numerical error.

## 6. Complexity
*   **Time Complexity:** $O(N \log N)$ where $N$ is the number of pixels, due to the use of a priority queue to manage trial nodes.
*   **Space Complexity:** $O(N)$ to store the arrival times and node status.

## 7. Usage
*   Geodesic distance calculation on surfaces and in 3D volumes.
*   Image segmentation (e.g., medical imaging, seismic processing).
*   Pathfinding in robotics with varying costs (e.g., terrain speed).
*   Shape reconstruction from point clouds.

## 9. References
1.  Sethian, J. A. (1996). A Fast Marching Level Set Method for Monotonically Advancing Fronts. Proceedings of the National Academy of Sciences.
2.  Sethian, J. A. (1999). Level Set Methods and Fast Marching Methods. Cambridge University Press.
3.  Tsitsiklis, J. N. (1995). Efficient algorithms for globally optimal trajectories. IEEE Transactions on Automatic Control.
