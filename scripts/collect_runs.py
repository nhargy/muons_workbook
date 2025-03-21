#!python3
from config.settings import LocalDataPath, OutPath

from models.run import Run

import os
import numpy as np
import pickle

#%%capture

TLV     = np.arange(0,11,1)
KYUL_SN = np.arange(11,13,1)
KYUL_WE = np.arange(13,17,1)

run_TLV = Run()
for i in TLV:
    print("# -- #")
    print(f"Processing Run{i}")
    print()
    run_path = os.path.join(LocalDataPath, f"Run{i}")
    run_TLV.add_run(run_path);

save_path = os.path.join(OutPath, "run_TLV.pkl")
with open(save_path, "wb") as f:
    pickle.dump(run_TLV, f)

run_SN = Run()
for i in KYUL_SN:
    print("# -- #")
    print(f"Processing Run{i}")
    print()
    run_path = os.path.join(LocalDataPath, f"Run{i}")
    run_SN.add_run(run_path);

save_path = os.path.join(OutPath, "run_SN.pkl")
with open(save_path, "wb") as f:
    pickle.dump(run_SN, f)

run_WE = Run()
for i in KYUL_WE:
    print("# -- #")
    print(f"Processing Run{i}")
    print()
    run_path = os.path.join(LocalDataPath, f"Run{i}")
    run_WE.add_run(run_path);

save_path = os.path.join(OutPath, "run_WE.pkl")
with open(save_path, "wb") as f:
    pickle.dump(run_WE, f)