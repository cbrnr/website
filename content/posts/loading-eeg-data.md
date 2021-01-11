---
title: Loading EEG data in Python
date: 2017-10-23T00:00:00+00:00
summary: Python is an extremely popular programming language for data analysis in general. In addition, the scientific Python community has created a striving ecosystem of neuroscience tools. A popular EEG/MEG toolbox is MNE, which offers almost anything required in an EEG processing pipeline. In this post, I show how to load EEG data sets and how to view and edit associated meta information.
tags:
  - Python
  - MNE
  - EEG
aliases:
  - 2017-10-23-loading-eeg-data
---

## MNE
[MNE](https://mne.tools) is a popular Python package for EEG/MEG processing. It offers a wide variety of useful tools including reading and writing of various file formats, filtering, independent component analysis (ICA), forward modeling, inverse solutions, time-frequency decompositions, visualization, and more. In fact, if you are familiar with [EEGLAB](https://sccn.ucsd.edu/eeglab/index.php) you might find that you can perform many similar analyses with Python and MNE. In this post I will show how to load EEG data as well as view and edit associated meta information.

## Prerequisites
The first step in almost any EEG processing pipeline is loading the raw data files into memory. There are many different file formats for storing EEG data, mostly because each EEG amplifier manufacturer uses its own data format. For example, [BrainProducts](http://www.brainproducts.com/) amplifiers store data as an EEG/VHDR/VMRK file triplet, [BioSemi](https://www.biosemi.com/) amplifiers create BDF files (an extension of the [European Data Format](https://www.edfplus.info/)), [Neuroscan](https://compumedicsneuroscan.com/) amplifiers use proprietary CNT files, and so on. Luckily, MNE comes with support for many popular EEG file formats.

The [EEG motor movement/imagery data set](https://physionet.org/content/eegmmidb/1.0.0/) we will use in this tutorial was contributed to the public domain by the developers of the [BCI2000](https://www.bci2000.org/mediawiki/index.php/Main_Page) system. In brief, they recorded 64-channel EEG from over 100 participants during motor execution and motor imagery tasks. In this tutorial, we will analyze only one participant and only one motor imagery run. If you want to follow along, go ahead and download [run 4 of subject 1](https://physionet.org/files/eegmmidb/1.0.0/S001/S001R04.edf?download) (note that MNE has a dedicated loader in `mne.datasets.eegbci` for this data set, which makes it even easier to load particular subjects and runs). All subsequent commands assume that the file is located in the current working directory.

Now that we have selected our data, it is time to fire up Python. I recommend [IPython](https://ipython.org/) as an enhanced interactive Python shell (go ahead and read my article on [how to set up Python for EEG analysis]({{< ref "setting-up-python" >}}) if you do not have a working Python environment yet). You can start IPython from a terminal by typing `ipython`.

We want to use the MNE package, so we have to import it.

```python
import mne
```

You can check the version of MNE as follows (make sure you always use the latest version):

```python
mne.__version__
```

```
'0.22.0'
```

## Loading EEG data
Loading EEG data works as follows. First, we need to know the file type of the file we want to load. In our case, the data is stored in an [EDF](https://www.edfplus.info/) file called `S001R04.edf`. Second, Python needs to know exactly where this file is located. We can either specify the full path to the file, or we can make sure that the file is in the current working directory, in which case the file name alone is sufficient. In this case, we can use the following command to load the raw data:

```python
raw = mne.io.read_raw_edf("S001R04.edf", preload=True)
```

The argument `preload=True` means that MNE performs the actual loading process immediately instead of the default lazy behavior. Also note that there are many more reader functions available in the `mne.io` package, including `mne.io.read_raw_bdf`, `mne.io.read_raw_brainvision`, `mne.io.read_raw_cnt`, and `mne.io.read_raw_eeglab`.

I won't reproduce the output that is generated during the loading process here. Usually, it contains some more or less useful logging messages, so if anything goes wrong make sure to carefully study these messages. If you don't want to see these messages, you can suppress them as follows:

```python
mne.set_log_level("WARNING")
```

This will instruct MNE to only print out warnings and errors.

## Viewing and editing meta information
The previous assignment generated a [`Raw`](https://mne.tools/stable/generated/mne.io.Raw.html) object in our workspace. This object holds the actual EEG data and associated meta information. We can get some basic information by inspecting this object in the interactive Python session:

```python
raw
```

```
<RawEDF | S001R04.edf, 64 x 20000 (125.0 s), ~9.8 MB, data loaded>
```

We can see the file name, the number of channels and sample points, the length in seconds, and the approximate size of the data in memory.

### The meta information attribute
We can dig deeper into the meta information by inspecting the `info` attribute associated with `raw`.

```python
raw.info
```

```
<Info | 7 non-empty values
 bads: []
 ch_names: Fc5., Fc3., Fc1., Fcz., Fc2., Fc4., Fc6., C5.., C3.., C1.., ...
 chs: 64 EEG
 custom_ref_applied: False
 highpass: 0.0 Hz
 lowpass: 80.0 Hz
 meas_date: 2009-08-12 16:15:00 UTC
 nchan: 64
 projs: []
 sfreq: 160.0 Hz
>
```

There are seven non-empty values in this attribute. For example, the line `chs: 64 EEG` near the top of the output tells us that there are 64 EEG channels (the first few channel names are listed in the line starting with `ch_names`). Individual elements of `raw.info` can be accessed with dictionary-like indexing. For example, the sampling frequency is stored in:

```python
raw.info["sfreq"]
```

```
160.0
```

Other useful `info` keys are:

- `"bads"`: A list of noisy (bad) channels which should be ignored in further analyses. Initially, this list is empty (as in our example), but we will manually populate it [in a later post]({{< ref visualizing-eeg-data >}}).
- `"ch_names"`: A list of channel names.
- `"chs"`: A detailed list of channel properties, including their types (for example, `EEG`, `EOG` or `MISC`).
- `"highpass"` and `"lowpass"`: Highpass and lowpass edge frequencies that were used during recording.
- `"meas_date"`: The recording date (a `datetime.datetime` object).

### Renaming channels
The output of `raw.info` revealed that some channel names are suffixed with one or more dots. Since these are non-standard names, let's rename the channels by removing all trailing dots:

```python
raw.rename_channels(lambda s: s.strip("."))
```

### Assigning a montage
For good measure (and for later use), we can assign a montage to the data (a montage relates channels names to standardized or actual locations on the scalp surface). First, let's list all montages that ship with MNE.

```python
mne.channels.get_builtin_montages()
```

```
['EGI_256',
 'GSN-HydroCel-128',
 'GSN-HydroCel-129',
 'GSN-HydroCel-256',
 'GSN-HydroCel-257',
 'GSN-HydroCel-32',
 'GSN-HydroCel-64_1.0',
 'GSN-HydroCel-65_1.0',
 'biosemi128',
 'biosemi16',
 'biosemi160',
 'biosemi256',
 'biosemi32',
 'biosemi64',
 'easycap-M1',
 'easycap-M10',
 'mgh60',
 'mgh70',
 'standard_1005',
 'standard_1020',
 'standard_alphabetic',
 'standard_postfixed',
 'standard_prefixed',
 'standard_primed']
```

According to the [data set documentation](https://physionet.org/content/eegmmidb/1.0.0/), the channel locations conform to the international 10&ndash;10 system. MNE does not seem to ship a 10&ndash;10 montage, but `standard_1020` contains template locations from the extended 10&ndash;20 system:

```python
montage = mne.channels.make_standard_montage("standard_1020")
montage.plot()
```

![](/images/montage.png)

It looks like this montage contains all channels used in our example data set. Therefore, we can assign this montage to our `raw` object.

```python
raw.set_montage(montage, match_case=False)
```

### Re-referencing
The data documentation does not mention any reference electrode, but it is safe to assume that all channels are referenced to some standard location such as a mastoid or the nose. Often, we want to re-reference EEG data to the so-called average reference (the average over all recording channels). In MNE, we can compute average referenced signals as follows:

```python
raw.set_eeg_reference("average")
```

Note that in general, methods modify MNE objects in-place.

### Annotations
Finally, many EEG data sets come with discrete events, either in the form of an analog stimulation channel or (text) annotations. Our example data set contains annotations that can be accessed with the `annotations` attribute:

```python
raw.annotations
```

```
<Annotations | 30 segments: T0 (15), T1 (8), T2 (7)>
```

We see that there are 30 annotations in total. There are three kinds of annotations named T0, T1, and T2. According to the [data set description](https://physionet.org/content/eegmmidb/1.0.0/), T0 corresponds to rest, T1 corresponds to motion onset of the left fist, and T2 corresponds to motion onset of the right fist.

If you encounter a file with an analog stimulation channel (this is typically the case for data recorded with BioSemi amplifiers), you need to extract discrete events from this channel as a first step. The `mne.find_events` function converts information contained in an analog stimulation channel to a NumPy array of shape `(N, 3)`, where `N` (the number of rows) is the number of detected events. The first column contains event onsets (in samples), whereas the third column contains (integer) event codes. The second column contains the values of the stimulation channel one sample before the detected events (this column can usually be ignored).

This NumPy array can be converted to an `Annotations` object using `mne.annotations_from_events`, which is often necessary for further analyses (note that you can associate an existing `Annotations` object with a `Raw` object by calling the `raw.set_annotations` method).

In the next post, I will demonstrate how to visualize this data set and how to interactively mark bad channels and bad segments.

## Download the code
The script [loading-eeg-data.py](/code/loading-eeg-data.py) contains all relevant code snippets from this post.