"""Example of using the MCNP Meshtal Python Processor (MMPP)"""

# The function-call 'ReadMeshtalfile' reads the meshtal
# file into memory.

# ========================================== Import module
import MMPP

# ========================================== Import plotting utils
import matplotlib.pyplot as plt
from matplotlib import cm,colors
import numpy as np

# ========================================== Read data into memory
data_blocks = MMPP.ReadMeshtalfile("TestMeshTally.msht")

# ========================================== Extract 2D data
a,b,c,d = data_blocks[0].UnpackGivenXE_bins(0,0)

# ========================================== (OPTIONAL) Rescale data
maxc = np.max(c)
minc = np.min(c)
print(maxc,minc)
maxc = 1.0e-4
minc = 1.0e-8
c = np.clip(c,minc,maxc)

# ========================================== (OPTIONAL)
#                                            Compute log-plot levels
lev_exp = np.linspace(np.floor(np.log10(minc)),
                      np.ceil(np.log10(maxc)),124)                     
levels = np.power(10, lev_exp)

# ========================================== Plot
plt.xlabel("X [cm]")
plt.ylabel("Z [cm]")
plt.contourf(a,b,c,levels,cmap='jet',norm=colors.LogNorm())
plt.show()
# plt.savefig("example_output.png")
