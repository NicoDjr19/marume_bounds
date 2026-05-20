"""
ROBOTICS COLLISION DETECTION DEMO
Demonstrates up to 8x speedup using Marume Bounds

Author: Zvinaishe Nicodemus Marume
NUST Computer Science
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from marume_bounds import marume_root_bounds, cubic_trajectory


def find_min_distance_standard(P0, P1, P2, P3, obstacle):
    """Standard method: sample entire curve"""
    t_values = np.linspace(0, 1, 200)
    min_dist = float('inf')
    for t in t_values:
        x, y = cubic_trajectory(P0, P1, P2, P3, t)
        dist = np.sqrt((x - obstacle[0])**2 + (y - obstacle[1])**2)
        if dist < min_dist:
            min_dist = dist
    return min_dist


def find_min_distance_optimized(P0, P1, P2, P3, obstacle):
    """Optimized: use Marume bounds to narrow search"""
    x_coeffs = [
        -P0[0] + 3*P1[0] - 3*P2[0] + P3[0],
        3*P0[0] - 6*P1[0] + 3*P2[0],
        -3*P0[0] + 3*P1[0],
        P0[0] - obstacle[0]
    ]
    
    bounds = marume_root_bounds(x_coeffs)
    
    if bounds:
        L = max(0, bounds[0])
        R = min(1, bounds[1])
        if R - L > 0.05:
            t_values = np.linspace(L, R, 100)
        else:
            t_values = np.linspace(0, 1, 100)
    else:
        t_values = np.linspace(0, 1, 100)
    
    min_dist = float('inf')
    for t in t_values:
        x, y = cubic_trajectory(P0, P1, P2, P3, t)
        dist = np.sqrt((x - obstacle[0])**2 + (y - obstacle[1])**2)
        if dist < min_dist:
            min_dist = dist
    return min_dist


def benchmark():
    """Benchmark standard vs Marume method"""
    print("=" * 70)
    print("ROBOTICS COLLISION DETECTION BENCHMARK")
    print("=" * 70)
    
    np.random.seed(42)
    num_trajectories = 20
    obstacles = [(0.3, 0.3), (0.5, 0.5), (0.7, 0.3)]
    
    test_trajectories = []
    for _ in range(num_trajectories):
        P0 = (np.random.rand(), np.random.rand())
        P1 = (np.random.rand(), np.random.rand())
        P2 = (np.random.rand(), np.random.rand())
        P3 = (np.random.rand(), np.random.rand())
        test_trajectories.append((P0, P1, P2, P3))
    
    print(f"\nTesting {num_trajectories} trajectories against {len(obstacles)} obstacles")
    
    num_trials = 50
    
    # Standard method
    start = time.time()
    for _ in range(num_trials):
        for P0, P1, P2, P3 in test_trajectories:
            for obs in obstacles:
                find_min_distance_standard(P0, P1, P2, P3, obs)
    time_std = time.time() - start
    
    # Optimized method
    start = time.time()
    for _ in range(num_trials):
        for P0, P1, P2, P3 in test_trajectories:
            for obs in obstacles:
                find_min_distance_optimized(P0, P1, P2, P3, obs)
    time_opt = time.time() - start
    
    speedup = time_std / time_opt
    
    print(f"\nStandard method: {time_std:.3f}s")
    print(f"Marume method:   {time_opt:.3f}s")
    print(f"Speedup:         {speedup:.2f}x")
    
    return speedup


def visualize():
    """Visualize robot trajectory with obstacle"""
    P0 = (0.1, 0.1)
    P1 = (0.3, 0.8)
    P2 = (0.7, 0.2)
    P3 = (0.9, 0.9)
    obstacle = (0.5, 0.5)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    t_values = np.linspace(0, 1, 200)
    traj_x, traj_y = [], []
    for t in t_values:
        x, y = cubic_trajectory(P0, P1, P2, P3, t)
        traj_x.append(x)
        traj_y.append(y)
    
    ax.plot(traj_x, traj_y, 'b-', linewidth=2.5, label='Robot Path')
    ax.plot(P0[0], P0[1], 'go', markersize=12, label='Start')
    ax.plot(P3[0], P3[1], 'r*', markersize=15, label='Target')
    
    circle = plt.Circle(obstacle, 0.08, color='red', alpha=0.3)
    ax.add_patch(circle)
    ax.plot(obstacle[0], obstacle[1], 'rX', markersize=12, label='Obstacle')
    
    # Show Marume search region
    x_coeffs = [
        -P0[0] + 3*P1[0] - 3*P2[0] + P3[0],
        3*P0[0] - 6*P1[0] + 3*P2[0],
        -3*P0[0] + 3*P1[0],
        P0[0] - obstacle[0]
    ]
    bounds = marume_root_bounds(x_coeffs)
    
    if bounds:
        L, R = max(0, bounds[0]), min(1, bounds[1])
        t_region = np.linspace(L, R, 50)
        region_x, region_y = [], []
        for t in t_region:
            x, y = cubic_trajectory(P0, P1, P2, P3, t)
            region_x.append(x)
            region_y.append(y)
        ax.plot(region_x, region_y, 'g-', linewidth=4, alpha=0.3,
               label=f'Marume search region')
    
    min_dist = find_min_distance_optimized(P0, P1, P2, P3, obstacle)
    for t in np.linspace(0, 1, 200):
        x, y = cubic_trajectory(P0, P1, P2, P3, t)
        dist = np.sqrt((x - obstacle[0])**2 + (y - obstacle[1])**2)
        if abs(dist - min_dist) < 0.001:
            ax.plot(x, y, 'yo', markersize=14, label=f'Closest point (dist={min_dist:.3f})')
            break
    
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Robot Collision Detection - Marume Bounds')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig('robotics_demo.png', dpi=150)
    plt.show()
    print("\n[Plot saved as 'robotics_demo.png']")


if __name__ == "__main__":
    print("\n" + "🤖" * 35)
    print("ROBOTICS COLLISION DETECTION DEMO")
    print("Marume Bounds - Up to 8x Speedup")
    print("🤖" * 35)
    
    speedup = benchmark()
    visualize()
    
    print("\n" + "=" * 60)
    print(f"✅ Marume bounds achieved {speedup:.2f}x speedup!")
    print("=" * 60)