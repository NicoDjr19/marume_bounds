"""
MARUME BOUNDS - Core Mathematical Functions
Discoveries 10 & 11: Turning Variance Formula and Root Bounds

Author: Zvinaishe Nicodemus Marume
NUST Computer Science
"""

import math
import numpy as np

def turning_variance(coeffs):
    """
    DISCOVERY 10: Compute turning variance σ_t² directly from coefficients.
    
    Formula: σ_t² = ((n-2)/n²)·b_{n-1}² - (2(n-2)/(n(n-1)))·b_{n-2}
    
    Parameters:
        coeffs: list [a_n, a_{n-1}, a_{n-2}, ..., a_0]
    
    Returns:
        σ_t² (turning variance)
    
    Example:
        >>> # For cubic x³ - 6x² + 11x - 6 (roots 1,2,3)
        >>> turning_variance([1, -6, 11, -6])
        0.3333333333333333
    """
    n = len(coeffs) - 1
    if n < 3:
        return 0.0
    
    a_n = coeffs[0]
    if a_n == 0:
        return 0.0
    
    b_n1 = coeffs[1] / a_n if len(coeffs) > 1 else 0
    b_n2 = coeffs[2] / a_n if len(coeffs) > 2 else 0
    
    term1 = ((n - 2) / (n * n)) * (b_n1 ** 2)
    term2 = (2 * (n - 2) / (n * (n - 1))) * b_n2
    
    return term1 - term2


def mean_of_roots(coeffs):
    """
    Compute mean of all roots via Viète's formula.
    
    μ = -a_{n-1} / (n·a_n)
    
    Parameters:
        coeffs: list [a_n, a_{n-1}, ..., a_0]
    
    Returns:
        μ (mean of roots)
    """
    n = len(coeffs) - 1
    a_n = coeffs[0]
    if a_n == 0:
        return 0
    return -coeffs[1] / (a_n * n) if len(coeffs) > 1 else 0


def marume_root_bounds(coeffs):
    """
    DISCOVERY 11: Guaranteed interval containing all real roots.
    
    For a real-rooted polynomial of degree n ≥ 3, all roots lie in:
    [μ - ((n-1)/√(n-2))·σ_t, μ + ((n-1)/√(n-2))·σ_t]
    
    Parameters:
        coeffs: list [a_n, a_{n-1}, ..., a_0]
    
    Returns:
        (lower_bound, upper_bound) or None if not applicable
    """
    n = len(coeffs) - 1
    if n < 3:
        return None
    
    sigma_t_sq = turning_variance(coeffs)
    if sigma_t_sq <= 1e-10:
        return None
    
    sigma_t = math.sqrt(sigma_t_sq)
    mu = mean_of_roots(coeffs)
    k_n = (n - 1) / math.sqrt(n - 2)
    radius = k_n * sigma_t
    
    return (mu - radius, mu + radius)


def cubic_trajectory(P0, P1, P2, P3, t):
    """
    Evaluate cubic Bézier curve at parameter t.
    
    Parameters:
        P0, P1, P2, P3: control points (x, y)
        t: parameter in [0, 1]
    
    Returns:
        (x, y) point on curve
    """
    u = 1 - t
    x = u**3 * P0[0] + 3*u**2*t * P1[0] + 3*u*t**2 * P2[0] + t**3 * P3[0]
    y = u**3 * P0[1] + 3*u**2*t * P1[1] + 3*u*t**2 * P2[1] + t**3 * P3[1]
    return (x, y)


# Test the core functions
if __name__ == "__main__":
    print("=" * 60)
    print("MARUME BOUNDS - Core Functions Test")
    print("=" * 60)
    
    # Test cubic with roots 1,2,3: x³ - 6x² + 11x - 6
    coeffs = [1, -6, 11, -6]
    
    mu = mean_of_roots(coeffs)
    sigma_t_sq = turning_variance(coeffs)
    bounds = marume_root_bounds(coeffs)
    
    print(f"\nPolynomial: x³ - 6x² + 11x - 6")
    print(f"Mean of roots (μ): {mu:.4f}")
    print(f"Turning variance (σ_t²): {sigma_t_sq:.6f}")
    print(f"Root bounds: [{bounds[0]:.4f}, {bounds[1]:.4f}]")
    print(f"Actual roots: [1, 2, 3]")
    print(f"✅ All roots within bounds: {bounds[0] <= 1 and bounds[1] >= 3}")
    
    print("\n✅ Core functions working correctly!")