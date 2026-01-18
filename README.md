# Keystroke Accelerometer ML (TinyML-Style Dataset)

This repository contains a keystroke-labeled 3-axis accelerometer dataset and an analysis notebook used for machine learning experiments (e.g., keystroke classification from vibration/vibration-like signatures).

An Arduino streams accelerometer readings (X, Y, Z) over serial. A Python logger records those readings alongside keyboard keypress events with timestamps on the same host machine. The dataset can be aligned by time and segmented into labeled windows for supervised learning.

## Goal

Keystrokes produce small, repeatable vibration patterns that can be captured by a 3-axis accelerometer. The goal of this project is to support ML workflows such as:
- keystroke classification (predict which key was pressed)
- window-based feature extraction (time- and frequency-domain)
- baseline model evaluation and comparison across recording segments/sessions

## Repository contents

This repo contains four primary artifacts:

- **`alphabet.ext`**  
  Raw capture file. Most rows contain timestamped accelerometer samples. Key labels (e.g., `a`, `b`) appear as separate timestamped rows with missing X/Y/Z values and are used to mark labeled segments.

- **`RawAccelerometer.ino`**  
  Arduino sketch used during data collection to read a 3-axis accelerometer and stream values over serial as:
  `x,y,z`

- **`serial.py`**  
  Host-side logger that records two synchronized streams:
  - accelerometer samples from Arduino serial
  - keyboard keypress events (labels)  
  Both streams are timestamped on the host machine to enable time alignment for downstream ML.

- **`analysis.ipynb`**  
  Notebook for parsing/cleaning the raw data, aligning labels with accelerometer samples, constructing labeled datasets, and running baseline ML experiments.

## Original data collection setup (high level)

This dataset was originally recorded using the following workflow:

1) **Arduino + accelerometer sensor**  
   The Arduino streamed accelerometer readings over USB serial in CSV format (`x,y,z`).

2) **Host-side logging + keyboard labels**  
   The Python script (`serial.py`) ran on the host computer to:
   - read the serial stream (accelerometer samples)
   - capture keyboard keypress events (key down)
   - timestamp both streams on the same machine for alignment

3) **Analysis / ML preparation**  
   The notebook (`analysis.ipynb`) parses the raw capture (`alphabet.ext`) and/or logger outputs to build labeled windows and run baseline ML experiments.

> Note: I no longer have access to the original hardware setup to re-validate exact wiring/sensor model details. The scripts and files in this repository reflect the workflow and data format used to generate the dataset.

## Raw data format (alphabet.ext)

The raw capture follows a time-series pattern:

- **Sensor sample rows** contain:
  `timestamp, x, y, z`

- **Label rows** contain a timestamp and a key label (e.g., `a`, `b`) with missing x/y/z values.
  These label rows are used to mark the start of a labeled segment and associate nearby accelerometer samples with the corresponding keypress class.

## Data overview

- **Signals:** 3-axis accelerometer (X, Y, Z)
- **Labels:** keyboard keypress classes (characters such as `a`, `b`, etc.)
- **Timestamps:** recorded on the host machine for both sensor samples and key events
- **Intended use:** create fixed-length windows around key events and train supervised ML models

## Baseline ML approach (current)

The notebook contains an initial baseline using KNN to explore learnability and establish a starting point for classification experiments.

Important evaluation note:
- The current notebook includes an initial approach that uses a regressor with encoded class labels and prints `model.score(...)`.
- For regressors, `.score()` returns **R²**, not classification accuracy. R² can be negative and should not be interpreted as an “accuracy” metric for multi-class key classification.

This repository is shared primarily as:
- a dataset + parsing reference for keystroke-labeled accelerometer data, and
- a baseline starting point with documented limitations and clear next steps.

## Results (current baseline)

The current baseline results are not strong and do not generalize well. They are included to document the initial pipeline and identify the major gaps to address for improved performance, including:
- treating the task as **classification** (not regression)
- using windowing around keypress events
- extracting features that emphasize transient keystroke signatures rather than baseline orientation/offset

## Limitations / known issues

- **Timestamp alignment is host-based:** serial transport can introduce small timing jitter.
- **Windowing/feature extraction is minimal in the current baseline:** raw XYZ points may be dominated by baseline components rather than keystroke transients.
- **Split strategy matters:** sensor time series can leak information if near-duplicate samples or adjacent windows from the same segment appear in both train and test.
- **Hardware replication is not currently verified:** the original equipment is no longer available to re-check sensor model and wiring details.

## Recommended next steps

If extending this project, the most impactful improvements are:

- **Reformulate as classification**  
  Use classifiers (e.g., `KNeighborsClassifier`, SVM, RandomForest) and report classification metrics (accuracy/F1/confusion matrix).

- **Add windowing around key events**  
  Construct fixed windows around each keypress timestamp (e.g., 0.2s pre + 0.8s post) and label each window by the corresponding key.

- **Feature engineering**  
  Add time- and frequency-domain features such as RMS, standard deviation, peak-to-peak amplitude, energy, and FFT band power.

- **Evaluation with leakage control**  
  Use session/segment-based splits to test generalization (not random shuffles of adjacent samples).

