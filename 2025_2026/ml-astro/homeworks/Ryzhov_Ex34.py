import numpy as np
from scipy.special import gamma

def calculate_pD(D):
    """
    Calculate pD = (π^(D/2)) / (2^(D-1) * Γ(D/2))
    
    Parameters:
    D (int or float): Dimensionality
    
    Returns:
    float: The calculated pD value
    """
    numerator = np.pi ** (D / 2)
    denominator = (2 ** (D - 1)) * gamma(D / 2)
    pD = numerator / denominator
    return pD

# Example usage
D_values = [10, 100, 1000, 10000]
for D in D_values:
    result = calculate_pD(D)
    print(f"pD for D={D}: {result}")