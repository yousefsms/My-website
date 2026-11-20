import math

def compute_uj(npr, gamma=1.4, R=287, T0=295):
    term1 = (2 * gamma * R * T0) / (gamma - 1)
    term2 = 1 - math.pow(npr, -(gamma - 1) / gamma)
    return math.sqrt(term1 * term2)

nprs = [4.3, 5.2, 7, 7.83, 8, 10, 12.5, 15]
for npr in nprs:
    print(f"NPR {npr}: {compute_uj(npr):.2f} m/s")
