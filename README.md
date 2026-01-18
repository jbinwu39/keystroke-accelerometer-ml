# Keystroke Accelerometer ML

This project contains a keystroke-labeled 3-axis accelerometer dataset and an accompanying analysis notebook used for machine learning experiments (e.g., keystroke classification from vibration signatures).

An Arduino streams accelerometer readings (X, Y, Z) over serial. A Python logger records those readings alongside keyboard keypress events with timestamps. The dataset can then be aligned by time and segmented into labeled windows for supervised learning.

## What this project is about

Keystrokes produce small, repeatable vibration patterns that can be captured by a 3-axis accelerometer. The goal of this project is to support ML workflows such as:
- **Keystroke classification** (predicting which key was pressed)
- **Window-based feature extraction** (time- and frequency-domain features)
- **Baseline model evaluation** and comparison across recording segments/sessions

## Repository contents

- **`alphabet.ext`**  
  Raw capture file. Primarily contains timestamped accelerometer samples, with key labels (e.g., `a`, `b`) embedded as separate timestamped rows that mark the start of labeled segments.

- **`RawAccelerometer.ino`**  
  Arduino sketch used during data collection to read a 3-axis accelerometer and stream values over serial in the format:
  `x,y,z`

- **`serial.py`**  
  Host-side Python logger that:
  - reads accelerometer samples from the Arduino over serial
  - records keyboard keypress events (labels)
  - timestamps both streams on the same machine for alignment  
  (The script writes CSV outputs on exit.)

- **`analysis.ipynb`**  
  Notebook used to parse/clean the raw data, align labels with accelerometer samples, construct labeled windows, and run ML experiments.

## Data overview

- **Signals:** 3-axis accelerometer (X, Y, Z)
- **Labels:** keyboard keypress classes (characters such as `a`, `b`, etc.)
- **Timestamps:** recorded on the host machine for both sensor samples and key events
- **Intended use:** create fixed-length windows around key events and train supervised ML models

## Original data collection setup (high level)

This dataset was originally recorded using the following workflow:

1) **Arduino + accelerometer**  
   An Arduino was connected to a 3-axis accelerometer sensor and programmed to stream readings over USB serial as `x,y,z`.

2) **Host-side logging + keyboard labels**  
   The Python script (`serial.py`) ran on the host computer to:
   - read the serial stream (accelerometer samples)
   - capture keyboard keypress events (labels)
   - timestamp both streams on the same machine for time alignment

3) **Analysis / ML preparation**  
   The notebook (`analysis.ipynb`) parses the raw capture (`alphabet.ext`) and/or the logger outputs to create labeled windows for supervised ML experiments.

> Note: I no longer have access to the original hardware setup to re-validate exact wiring/sensor model details. The files in this repository reflect the workflow and data format used to generate the dataset.

## Raw data format notes

The raw capture (`alphabet.ext`) follows a time-series pattern:
- Most rows contain:
  `timestamp, x, y, z`
- Label events appear as separate rows containing a timestamp and a key label (e.g., `a`, `b`) with missing x/y/z values.

These label rows indicate where labeled segments begin and can be used to associate nearby accelerometer samples with the corresponding keypress class.

## ML framing (high level)

A typical ML workflow (implemented in `analysis.ipynb`) includes:
1) parse the raw capture into continuous samples + label events  
2) align labels to sensor samples using timestamps  
3) window around each keypress event (fixed number of samples or fixed time span)  
4) extract features and/or train window-based models  
5) evaluate with an appropriate split strategy (e.g., by session/run to reduce leakage)

## Limitations

- Host-based timestamps and serial transport can introduce small timing jitter.
- Without the original equipment, this repo focuses on the dataset, parsing, and ML analysis rather than hardware replication.

