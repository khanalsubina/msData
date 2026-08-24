# 5G Millisecond-Resolution Network Benchmarking Dataset & Time Series Foundation Models

**Paper**: "msData: A Millisecond-Resolution Network Dataset for Advancing Time Series Foundation Models"

This repository contains code and data for benchmarking shallow models, transformer-based deep learning models, and Time Series Foundation Models (TSFMs) on high-frequency 5G network traffic forecasting tasks using millisecond-resolution measurements from an operational 5G Radio Access Network (RAN).

## Overview

This work addresses a critical gap in TSFM evaluation: the lack of diverse, high-frequency datasets. While existing benchmarks focus on low-frequency time series (seconds to years), production wireless networks generate data at millisecond granularity with complex temporal dynamics. This repository provides:

1. **5G_millisecond.csv**: A novel dataset capturing millisecond-resolution RAN metrics
2. **Comprehensive benchmarks**: 12 models evaluated in both univariate and multivariate settings
3. **Supplementary notebooks**: Full experimental reproductions of main experiments

---

## Quick Start

> **Experiment datasets:** The supported experiments use:
     > - `data/filtered/youtube_static.csv` for the main benchmarks (Table 4) and TTM fine-tuning (Table 5)
     > - `data/filtered/webbrowsing_train.csv` for the additional filtered data subset experiments (Table 7)
     > - `data/filtered/youtube_pedestrian.csv` for the temporal-resolution ablation study (Table 6)

1. Create the required conda environments:
```bash
   conda env create -f environment.yml
   conda env create -f arf_environment.yml
```

Use:
- tf-env for Random Forest, XGBoost, TTM, Chronos, Lag-Llama, iTransformer, and PatchTST
- river-env for ARF and OLR

2. Generate the filtered datasets: Place the raw dataset in data/raw/, then run:
```bash
  python scripts/filter_data.py
```

3. To reproduce the main benchmark results (Table 4):

#### 3a. Run the notebook-based experiments:
```bash
conda activate tf-env
scripts\youtube_static\reproduce_univariate.bat
scripts\youtube_static\reproduce_multivariate.bat
```

#### 3b. Run ARF and OLR separately:
```bash
conda activate river-env
python scripts/youtube_static/ARF_Univariate.py --seeds 42
python scripts/youtube_static/ARF_Multivariate.py --seeds 42
python scripts/youtube_static/OLR_Univariate.py
python scripts/youtube_static/OLR_Multivariate.py
```

4. To reproduce the additional filtered data subset results (Table 7):

#### 4a. Run the notebook-based experiments:
```bash
conda activate tf-env
scripts\webbrowsing_train\reproduce_univariate.bat
scripts\webbrowsing_train\reproduce_multivariate.bat
```

#### 4b. Run ARF and OLR separately:
```bash
conda activate river-env
python scripts/webbrowsing_train/ARF_Univariate.py --seeds 42
python scripts/webbrowsing_train/ARF_Multivariate.py --seeds 42
python scripts/webbrowsing_train/OLR_Univariate.py
python scripts/webbrowsing_train/OLR_Multivariate.py
```

5. Reproduce the ablation studies (TTM fine-tuning strategies) results (Table 5).
```bash
conda activate tf-env
scripts\fine-tuning_TTM\reproduce_fine-tuning.bat
```

6. Reproduce the ablation studies (Temporal resolution) results (Table 6).
```bash
conda activate tf-env
scripts\temporal_resolution\reproduce_tempresolution.bat
```

```bash
conda activate river-env
scripts\temporal_resolution\arf_tempresolution.bat
```

### Environment Map

- `tf-env`: Random Forest, XGBoost, Naive, TTM, Chronos, Lag-Llama, iTransformer, PatchTST
- `river-env`: Adaptive Random Forest (ARF), Online Linear Regression (OLR)

### Windows Note

This repository uses Windows batch files (`.bat`) for notebook execution.  
Run them from Anaconda Prompt or Command Prompt after activating the correct conda environment.

For detailed setup instructions, model-specific installation steps, and full experiment commands, see `REPRODUCIBILITY.md`.
---

## Dataset
**Raw Data**: `5G_millisecond.csv`

**Experiment dataset**: The experiment-ready datasets are generated using:

```bash
python scripts/filter_data.py
```


### Data Source & Collection
All filtered datasets originate from the same OpenRanlab 5G O-RAN testbed deployment.

- **Source**: OpenRanlab 5G O-RAN testbed deployment
- **Collection Duration**: ~33 seconds of continuous measurements (January 1, 2022, 00:00:00 to 00:00:32.814)
- **Collection Method**: Software-Defined Radios (Ettus USRPs) configured as base station, collecting from multiple User Equipments (UEs)

The filtered subsets used in the experiments are:

| Dataset | Traffic Class | Mobility Pattern | Timestamp Interval | Usage |
|---|---|---|---:|---|
| `youtube_static.csv` | Video streaming (YouTube) | Static | 1 ms | Main univariate and multivariate benchmarks and TTM Fine-tuning |
| `webbrowsing_train.csv` | Web browsing | Train | 1 ms | Additional dataset experiments |
| `youtube_pedestrian.csv` | Video streaming (YouTube) | Pedestrian | 100 ms | Temporal-resolution ablation study |


## Forecasting Setup

### Main Benchmark

- **Task**: Short-term bitrate forecasting (1-96 steps ahead)
- **Horizon**: 96 steps = 96 milliseconds into future
- **Input Sequence Length**: 5 steps (50 milliseconds of history for shallow models)
- **Prediction Target**: `mac_dl_brate` (downlink bitrate)

### Temporal-Resolution Ablation
The temporal-resolution study adjusts the prediction horizon according to the resampling interval:

| Resolution | Prediction Horizon |
|---|---:|
| 100 ms | 96 |
| 200 ms | 48 |
| 500 ms | 20 |
| 1000 ms | 10 |
| 2000 ms | 5 |
| 3000 ms | 4 |

The resampled datasets are generated in memory during execution. Only the final metrics are saved.

### Univariate vs. Multivariate

| Setting      | Features Used                     |
|--------------|-----------------------------------|
| Univariate   | Lagged values of `mac_dl_brate` only |
| Multivariate | 4 features (CQI, MCS, pkt ok, pkt nok)                 |

---

## Models Benchmarked

### Shallow Machine Learning Models

1. **Random Forest (RF)** - Scikit-learn, optimized for multi-step forecasting
2. **XGBoost (XGB)** - Gradient boosting ensemble
3. **Adaptive Random Forest (ARF)** - River library; handles streaming/online learning
4. **Online Linear Regression (OLR)** - Incremental learning baseline


5. **Naive Baseline** - Previous value repeated

### Transformer-based Deep Learning Models
6. **PatchTST** - Patch-based transformer
7. **iTransformer** - Attention over features 

### Time Series Foundation Models (TSFMs)
8. **TTM (Tiny Time Mixers)** - Light-weight pre-trained model
9. **Chronos** - Probabilistic TSFM; supports zero-shot and fine-tuned variants
10. **Lag-Llama** - Decoder-only transformer; zero-shot and fine-tuned variants (supports univariate setting only)


### Main Benchmark Results (Table 4)
The table below summarizes the main benchmark results on youtube_static.csv. Additional results and ablation-study tables are reproduced through the scripts listed in REPRODUCIBILITY.md.

**Table: Performance Metrics (Scaled RMSE / MAE)**

| Model | Univariate | Multivariate | 
|-------|-----------|--------------|
| RF | 0.0344 / 0.0227 | 0.0342 / 0.0226 | 
| XGB | 0.0354 / 0.0232 | 0.0354 / 0.0231 | 
| ARF | **0.0270 / 0.0189** | **0.0175 / 0.0130** |
| Naive | 0.0418 / 0.0240 | 0.0418 / 0.0240 | 
| OLR | 0.0551 / 0.0308 | 0.0555 / 0.0310 | 
| PatchTST | 0.0327 / 0.0212 | 0.0321 / 0.0207 | 
| iTransformer | 0.0325 / 0.0208 | 0.0324 / 0.0208 | 
| TTM Zero-shot | 0.0359 / 0.0230 | 0.0359 / 0.0230 | 
| TTM Fine-tuning | 0.0371 / 0.0237 | 0.0393 / 0.0250 | 
| Chronos Zero-shot | 0.0313 / 0.0185 | 0.0273 / 0.0181 | 
| Chronos Fine-tuning | 0.0281 / 0.0178 | 0.0253 / 0.0176 | 
| Lag-Llama Zero-shot | 0.0617 / 0.0384 | - | 
| Lag-Llama Fine-tuning | 0.0474 / 0.0268 | - | 

---

## Installation

### 1. Environment Setup
Create the required conda environments:
```bash
conda env create -f environment.yml
conda env create -f arf_environment.yml
```

TSFMs require additional one-time setup:
- Chronos
- TTM
- Lag-Llama

See REPRODUCIBILITY.md for detailed installation instructions.


### 2. Load Dataset

```python
import pandas as pd

df = pd.read_csv('data/filtered/youtube_static.csv')
print(df.head())
```

### 3. Run a Simple Experiment

**Univariate Random Forest:**
```bash
jupyter notebook notebooks/youtube_static/RF_Univariate.ipynb
```

**Multivariate Adaptive Random Forest (Best Performance):**
```bash
jupyter notebook notebooks/AdaptiveRF_Multivariate.ipynb
```

### 4. Run All Benchmarks

See `REPRODUCIBILITY.md` for automated scripts and commands to reproduce the main results reported in Table 4.

---

## Main Benchmark: Key Findings (Table 4)

1. **ARF Excels at High-Frequency Data**: ARF achieved the best multivariate performance (RMSE 0.0175, MAE 0.0130).

2. **TSFMs Show Promise**: Chronos fine-tuning achieved strong TSFM performance (RMSE 0.0253, MAE 0.0176).

3. **Fine-tuning Matters**: Fine-tuning improved Lag-Llama and Chronos over zero-shot baselines.

---

## Limitations & Future Work

1. **Limited Temporal Span**: 33 seconds is short; multi-hour or multi-day traces would enable seasonality analysis.
2. **Single Traffic Class**: Video streaming only; generalization to mixed traffic unknown.
3. **Single Testbed**: Results specific to O-RAN architecture; applicability to traditional RAN/cellular unclear.

**Future Work:**
- Longer traces (hours/days) with realistic traffic mix
- Real-world deployment scenarios
- Anomaly detection and classification sub-tasks

---

## Reproducibility

See `REPRODUCIBILITY.md` for the complete mapping between the four supported result tables, input datasets, environments, notebooks, scripts, expected outputs, and execution commands.


---


## Changelog
- **v1.1** (2026-08-21): Expanded the reproducibility package to support four published result tables, including additional experiments on `webbrowsing_train.csv` and two ablation studies.
- **v1.0** (2026-06-16): Initial release with 12 models, 32.8K samples, millisecond-resolution 5G RAN data
