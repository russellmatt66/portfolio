import numpy as np
import matplotlib.pyplot as plt

N_max = int(20)

N_list = np.linspace(2, N_max, dtype=int, num=N_max-1)
print(N_list)

rt_list = []
rt_list.append(3) # base case

for iN in range(1, len(N_list)):
    rt_list.append(N_list[iN] * (rt_list[iN-1] + 2) - 1)

print(rt_list)

plt.semilogy(N_list, rt_list, linestyle='-', label='O(N) = F(N)')
plt.semilogy(N_list, 2**N_list, linestyle='--', color='orange', label='$O(N) = 2^{N}$')
plt.semilogy(N_list, 4**N_list, linestyle='--', color='red', label='$O(N) = 4^{N}$')
plt.semilogy(N_list, 8**N_list, linestyle='--', color='green', label='$O(N) = 8^{N}$')

plt.semilogy(N_list, [1e9] * len(N_list), linestyle='-.', color='blue', label='1 GFLOP')
plt.semilogy(N_list, [1e12] * len(N_list), linestyle='-.', color='orange', label='1 TFLOP')
plt.semilogy(N_list, [1e15] * len(N_list), linestyle='-.', color='red', label='1 PFLOP')
plt.semilogy(N_list, [1e18] * len(N_list), linestyle='-.', color='green', label='1 EFLOP')

plt.xticks(N_list)
plt.xlim(N_list.min(), N_list.max())
plt.ylim(min(rt_list), max(rt_list))
plt.ylabel('FPOs')
plt.xlabel('N')
plt.title('Computational work required to compute a determinant by sub-matrix expansion')

plt.legend()
plt.show()
