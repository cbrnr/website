# (c) Clemens Brunner, licensed under the BSD 3-Clause license

import numpy as np
from scipy.io import loadmat
import mne


mat = loadmat("A01T.mat", simplify_cells=True)

eeg1 = mat["data"][2]["X"] * 1e-6  # run 3 (calibration)
eeg2 = mat["data"][3]["X"] * 1e-6  # run 4 (experiment)

info = mne.create_info(25, 250, ch_types=["eeg"] * 22 + ["eog"] * 3)
raw1 = mne.io.RawArray(eeg1.T, info)
raw2 = mne.io.RawArray(eeg2.T, info)

bip = np.array([[1, -1, 0], [0, -1, 1]])
raw1_eog = bip @ raw1[22:, :][0]
raw2_eog = bip @ raw2[22:, :][0]
raw1_eeg = raw1[:22, :][0]
raw2_eeg = raw2[:22, :][0]

b = np.linalg.solve(raw1_eog @ raw1_eog.T, raw1_eog @ raw1_eeg.T)

eeg_corrected = (raw2_eeg.T - raw2_eog.T @ b).T
raw3 = raw2.copy()
raw3._data[:22, :] = eeg_corrected

raw2.plot(n_channels=25, start=53, duration=5, block=True, title="Before")
raw3.plot(n_channels=25, start=53, duration=5, block=True, title="After")
