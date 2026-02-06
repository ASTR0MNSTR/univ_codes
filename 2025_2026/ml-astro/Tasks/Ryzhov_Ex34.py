import numpy as np
from scipy.special import gamma, gammaln

def compute_pN(D):
    """
    Computes p(D) for a D-dimensional distribution.
    p(D) = (pi^(D/2) / Gamma(D/2 + 1)) / (2^D)
    """
    # Use log-space calculation to prevent overflow/underflow for large D
    # log(pN) = (D/2)*log(pi) - D*log(2) - log_gamma(D/2 + 1)
    log_pN = (D / 2.0) * np.log(np.pi) - D * np.log(2.0) - gammaln(D / 2.0 + 1)
    
    # Convert back to regular space
    # For very large D, this will return 0.0 as it underflows float64
    return np.exp(log_pN)

# Set of dimensions requested
dimensions = [10, 100, 1000, 10000]

print(f"{'D':>6} | {'p(D)':>12}")
print("-" * 22)

for D in dimensions:
    pN = compute_pN(D)
    # Using scientific notation to handle extremely small probabilities
    print(f"{D:6d} | {pN:.4e}")

# Detailed check for D=10 using the gamma function directly as requested
# p(10) = (pi^5 / gamma(6)) / 2^10
pN_10_direct = (np.pi**5 / gamma(6)) / (2**10)
print(f"\nVerification for D=10 using direct gamma: {pN_10_direct:.4e}")
