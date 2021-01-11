# (c) Clemens Brunner, licensed under the BSD 3-Clause license

import mne


raw = mne.io.read_raw_edf("S001R04.edf", preload=True)
raw.rename_channels(lambda s: s.strip("."))

montage = mne.channels.make_standard_montage("standard_1020")
raw.set_montage(montage, match_case=False)

raw.set_eeg_reference("average")
