#!/usr/bin/env python3

import sys, os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns

# Add src directory to system path
project_path = os.getcwd().split('/src')[0]
sys.path.append(project_path)

print(project_path)

plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16

try:
    from src.models.run import Run
    from src.utils.functions import gaussian
    from src.utils.functions import decay
    from src.utils.functions import hist_to_scatter
    from src.utils.functions import remove_nans
except Exception as e:
    print("Failed to import local modules:")
    print(e)

# Define important paths
lcd_path  = os.path.join(project_path, 'lcd')
out_path  = os.path.join(project_path, 'out')
plt_path  = os.path.join(project_path, 'plt')

a1 = np.load(os.path.join(out_path, "a1.npy"))
a2 = np.load(os.path.join(out_path, "a2.npy"))
a3 = np.load(os.path.join(out_path, "a3.npy"))

# Boundaries
SN1 = 631

WE1 = 725
WE2 = WE1 + 743
WE3 = WE2 + 690

off = 6
mod = 48

sn1 = ((a2[:SN1] / 3600) + 16.63 - off) 
sn2 = ((a2[SN1:] / 3600) + 15.1 - off ) 

we1 = ((a3[:WE1] / 3600) + 7.7 - off)
we2 = ((a3[WE1:WE2] / 3600) + 7.3 - off)
we3 = ((a3[WE2:WE3] / 3600) + 6.9 - off)
we4 = ((a3[WE3:] / 3600) + 7.3 - off)

plt.rcParams['ytick.labelsize'] = 0
plt.rcParams['xtick.labelsize'] = 22

bins = np.arange(0, 38, 2)
fig, axs = plt.subplots(nrows=6, ncols=1, figsize=(8,16), sharex=True, sharey=False)
plt.subplots_adjust(hspace=0, wspace=0)

# remove ticks from plots
for i in range(0,5):
    axs[i].set_xticks([])
    
    axs[i].axhline(60, linestyle = '--', color = 'grey', lw = 2.5, zorder=3, alpha = 0.7)  

axs[5].axhline(60, linestyle = '--', color = 'grey', lw = 2.5, zorder=3, alpha = 0.7)

axs[5].set_xticks([0,12,24,36], labels = ["06:00", "18:00", "06:00", "18:00"])

sn1_hist, edges = np.histogram(sn1, bins=bins)
bin_centres = np.array(edges[:-1] + (np.diff(edges)/2), dtype=int)
sns.barplot(x=bin_centres, y = sn1_hist, ax=axs[0])
#sns.histplot(data = sn1, bins=bins, ax = axs[0], zorder=2)
axs[0].set_ylabel("11/08/2024", fontsize = 16) #16:38
axs[0].axvspan(0,18, color='brown', alpha = 0.1)
axs[0].axvspan(18,36, color='magenta', alpha = 0.1)

axs[0].text(1.1, 63, r'2 events min$^{-1}$', style='italic', fontsize = 16)

sn2_hist, edges = np.histogram(sn2, bins=bins)
bin_centres = np.array(edges[:-1] + (np.diff(edges)/2), dtype=int)
sns.barplot(x=bin_centres, y = sn2_hist, ax=axs[1])
#sns.histplot(data = sn2, bins=bins, ax = axs[1], zorder=2)
axs[1].set_ylabel("12/08/2024", fontsize = 16) #15:06
axs[1].axvspan(0,18, color='brown', alpha = 0.1)
axs[1].axvspan(18,36, color='magenta', alpha = 0.1)

we1_hist, edges = np.histogram(we1, bins=bins)
bin_centres = np.array(edges[:-1] + (np.diff(edges)/2), dtype=int)
sns.barplot(x=bin_centres, y = we1_hist, ax=axs[2])
#sns.histplot(data = we1, bins=bins, ax = axs[2], zorder=2)
axs[2].set_ylabel("18/08/2024", fontsize = 16) #07:43
axs[2].axvspan(0,18, color='brown', alpha = 0.1)
axs[2].axvspan(18,36, color='magenta', alpha = 0.1)

we2_hist, edges = np.histogram(we2, bins=bins)
bin_centres = np.array(edges[:-1] + (np.diff(edges)/2), dtype=int)
sns.barplot(x=bin_centres, y = we2_hist, ax=axs[3])
#sns.histplot(data = we2, bins=bins, ax = axs[3], zorder=2)
axs[3].set_ylabel("19/08/2024", fontsize = 16) #07:16
axs[3].axvspan(0,18, color='brown', alpha = 0.1)
axs[3].axvspan(18,36, color='magenta', alpha = 0.1)

we3_hist, edges = np.histogram(we3, bins=bins)
bin_centres = np.array(edges[:-1] + (np.diff(edges)/2), dtype=int)
sns.barplot(x=bin_centres, y = we3_hist, ax=axs[4])
#sns.histplot(data = we3, bins=bins, ax = axs[4], zorder=2)
axs[4].set_ylabel("20/08/2024", fontsize = 16) #06:53
axs[4].axvspan(0,18, color='brown', alpha = 0.1)
axs[4].axvspan(18,36, color='magenta', alpha = 0.1)

we4_hist, edges = np.histogram(we4, bins=bins)
bin_centres = np.array(edges[:-1] + (np.diff(edges)/2), dtype=int)
sns.barplot(x=bin_centres, y = we4_hist, ax=axs[5])
#sns.histplot(data = we4, bins=bins, ax = axs[5], zorder=2)
axs[5].set_ylabel("21/08/2024", fontsize = 16) #07:16
axs[5].axvspan(0,18, color='brown', alpha = 0.1)
axs[5].axvspan(18,36, color='magenta', alpha = 0.1)


plt.show()
plt.close()

"""
print("Bins: ", bins)
print()
print("Hist: ", we4_hist)
print()
print("Edges:", edges)
print()
print("Centres: ", bin_centres)
"""

# ===

sn1_24 = ((a2[:SN1] / 3600) + 16.63 - off) % 24
sn2_24 = ((a2[SN1:] / 3600) + 15.1 - off ) % 24

we1_24 = ((a3[:WE1] / 3600) + 7.7 - off) % 24
we2_24 = ((a3[WE1:WE2] / 3600) + 7.3 - off) % 24
we3_24 = ((a3[WE2:WE3] / 3600) + 6.9 - off) % 24
we4_24 = ((a3[WE3:] / 3600) + 7.3 - off) % 24

# ===

print(sn1)




























