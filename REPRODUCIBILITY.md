# Reproducibility Guide: 5G Network Benchmarking Study

This document provides step-by-step instructions to reproduce four result tables from the paper "msData: A Millisecond-Resolution Network Dataset for Advancing Time Series Foundation Models".

The reproducibility package covers:
1. Main univariate and multivariate benchmark results on `youtube_static.csv`
2. Additional benchmark results on `webbrowsing_train.csv`
3. Temporal-resolution ablation results on `youtube_pedestrian.csv`
4. A second ablation study results on `youtube_static.csv` for fine-tuning TTM

---

## Quick Start

Follow the steps below to generate the filtered datasets, run the supported experiments, and collect the final metrics.

### 1. Create the required conda environments

```bash
conda env create -f environment.yml
conda activate tf-env

conda env create -f arf_environment.yml
conda activate river-env
```

### 2. Prepare the Filtered Datasets
Place the original dataset in: data/raw/, then run:
```bash
python scripts/filter_data.py
```
This generates the experiment-ready datasets in: data/filtered/
The supported experiments use:

> - `data/filtered/youtube_static.csv` for the main benchmarks (Table 4) and TTM fine-tuning (Table 5)
> - `data/filtered/webbrowsing_train.csv` for the additional filtered data subset experiments (Table 7)
> - `data/filtered/youtube_pedestrian.csv` for the temporal-resolution ablation study (Table 6)

### 3. To reproduce the main benchmark results (Table 4):

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

### 4. To reproduce the additional filtered data subset results (Table 7):

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

### 5. Reproduce the ablation studies (TTM fine-tuning strategies) results (Table 5).
```bash
conda activate tf-env
scripts\fine-tuning_TTM\reproduce_fine-tuning.bat
```

### 6. Reproduce the ablation studies (Temporal resolution) results (Table 6).
```bash
conda activate tf-env
scripts\temporal_resolution\reproduce_tempresolution.bat
```

```bash
conda activate river-env
scripts\temporal_resolution\arf_tempresolution.bat
```

### 7. Output Location
The saved metrics are written to: notebooks/results/metrics/

---

## Repository Structure

The repository is organized as follows:

- `README.md`: short project overview and quick entry point
- `REPRODUCIBILITY.md`: detailed step-by-step reproduction guide
- `environment.yml`: conda environment for TensorFlow/foundation-model experiments
- `arf_environment.yml`: conda environment for River-based streaming models
- `data/raw/`: original raw dataset (empty for now)
- `data/filtered/`: filtered datasets generated before model execution
- `notebooks/`: experiment notebooks for all models
- `scripts/`: helper scripts, Python runners, and Windows batch files
- `notebooks/results/metrics/`: saved model metrics
- `executed_notebooks/`: saved executed notebooks run from scripts

```
tmlr-reproducibility/
├── README.md
├── REPRODUCIBILITY.md
├── environment.yml
├── arf_environment.yml
├── test_imports.py
├── data/
│   ├── raw/
│   │   └── 5G_millisecond.csv
│   └── filtered/
│       ├── youtube_static.csv
│       ├── webbrowsing_train.csv
│       └── youtube_pedestrian.csv
├── notebooks/
│   ├── Fine-Tuning_strategies_for_TTM/
│   ├── results/
│   ├── Temporal_Resolution/
│   ├── webbrowsing_train/
│   ├── youtube_static/
├── scripts/
│   ├── filter_data.py
│   ├── youtube_static/
│   ├── webbrowsing_train/
│   └── temporal_resolution/
│   └── fine-tuning_TTM/
├── executed_notebooks/
    
```

---

## Environment Map
Different models require different software environments.
### `tf-env`
Use this environment for:
- Random Forest
- XGBoost
- Naive
- TTM
- Chronos
- Lag-Llama
- iTransformer
- PatchTST

### `river-env`
Use this environment for:
- Adaptive Random Forest (ARF)
- Online Linear Regression (OLR)

## Complete Environment Setup

# TensorFlow environment (most models)
```bash
conda env create -f environment.yml
conda activate tf-env
```

# ARF/OLR (streaming/online learning)
For Adaptive Random Forest, first ensure Python 3 is installed. Then, install the River library and create the conda environment using arf_environment.yml

```bash
conda env create -f arf_environment.yml
conda activate river-env
```

## Model-Specific One-Time Setup:

The following TSFMs require additional one-time setup before the experiment notebooks can be executed:
- Chronos
- TTM
- Lag-Llama


# Chronos
To set up Chronos, follow these instructions from the official GitHub repository:

```sh
conda activate tf-env
!pip install autogluon
If keras3 is installed, then install the backwards-compatible tf-keras package with `!pip install tf-keras`.
```

# TTM

To set up TTM, follow these instructions from the official GitHub repository:

```sh
conda activate tf-env
# Clone the ibm/tsfm
! git clone https://github.com/ibm-granite/granite-tsfm.git
! ls

# Change directory. Move inside the tsfm repo.
%cd granite-tsfm
! ls

# Relax requirement for python version < 3.12
! sed -i.orig 's/3\.12/3.13/g' pyproject.toml

# Install the tsfm library
#! pip install ".[notebooks]"
#! python3 -m pip install ".[notebooks]"
! pip3 install ".[notebooks]"
```

# Lag-Llama
To set up Lag-Llama, follow these instructions from the official GitHub repository:

```sh
!git clone -b update-gluonts https://github.com/time-series-foundation-models/lag-llama/
cd lag-llama
!pip install -r requirements.txt  
!pip install -U torch torchvision
!huggingface-cli download time-series-foundation-models/Lag-Llama lag-llama.ckpt --local-dir lag-llama
cd lag-llama
```

**Expected versions** (minimum):
- Python: 3.9+
- pandas: 2.1+
- scikit-learn: 1.5+
- tensorflow: 2.17+
- numpy: 1.24+
- torch: 2.10.0+
- scipy: 1.10+
- xgboost: 3.0 +
- transformers: 4.50+
- autogluon: 1.1+
- tf-keras:2.15+
- granite-tsfm:0.1+
- matplotlib:3.8+
- river:0.20+


### Verify Installation

Run:
```bash
python test_imports.py
```
---

## Dataset Preparation

### 1. Filter Dataset
Before running any model, generate the filtered datasets. This creates three CSV files:
- `youtube_static.csv`
- `webbrowsing_train.csv`
- `youtube_pedestrian.csv`

```bash
python scripts/filter_data.py
```

The filtered subsets used in the experiments are:

| Dataset | Traffic Class | Mobility Pattern | Timestamp Interval | Usage |
|---|---|---|---:|---|
| `youtube_static.csv` | Video streaming (YouTube) | Static | 1 ms | Main univariate and multivariate benchmarks and TTM Fine-tuning |
| `webbrowsing_train.csv` | Web browsing | Train | 1 ms | Additional dataset experiments |
| `youtube_pedestrian.csv` | Video streaming (YouTube) | Pedestrian | 100 ms | Temporal-resolution ablation study |


## Temporal-Resolution Ablation Setup
The temporal-resolution ablation uses youtube_pedestrian.csv. The resampled datasets are generated during execution and are not saved as separate CSV files. Only the final metrics are saved. The data is resampled in memory to the following temporal resolutions:

| Resolution | Prediction Horizon |
|---|---:|
| 100 ms | 96 |
| 200 ms | 48 |
| 500 ms | 20 |
| 1000 ms | 10 |
| 2000 ms | 5 |
| 3000 ms | 4 |


---

## Reproducing Experiments

## Windows Note

This repository provides Windows batch files (`.bat`) for notebook execution.  
Run them from Anaconda Prompt or Command Prompt after activating the correct conda environment.

### Table 4: Main Performance Results

To reproduce the main experiments, use the commands below.

### Dataset:
data/filtered/youtube_static.csv

### Notebook-based experiments (tf-env)
Run the multivariate notebook group using the appropriate batch file:
```bash
conda activate tf-env
scripts\youtube_static\reproduce_multivariate.bat
```

Run the univariate notebook group using the appropriate batch file:
```bash
conda activate tf-env
scripts\youtube_static\reproduce_univariate.bat
```

The ARF and OLR experiments are run separately in the River/streaming-model environment. 
Run ARF:

```bash
conda activate river-env
python scripts/youtube_static/ARF_Univariate.py --seeds 42
python scripts/youtube_static/ARF_Multivariate.py --seeds 42
```
Run OLR:

```bash
conda activate river-env
python scripts/youtube_static/OLR_Univariate.py 
python scripts/youtube_static/OLR_Multivariate.py 
```

### Lag-Llama
Lag-Llama requires a one-time external setup before the zero-shot or fine-tuning notebook can be executed, as mentioned above (Installation). After completing the one-time setup, run the Lag-Llama notebook.

### Table 7: Additional Filtered Data Subset Results

To reproduce the additional filtered data subset experiments, use the commands below.

### Dataset:
data/filtered/webbrowsing_train.csv

### Notebook-based experiments (tf-env)
Run the multivariate notebook group using the appropriate batch file:
```bash
conda activate tf-env
scripts\webbrowsing_train\reproduce_multivariate.bat
```

Run the univariate notebook group using the appropriate batch file:
```bash
conda activate tf-env
scripts\webbrowsing_train\reproduce_univariate.bat
```

The ARF and OLR experiments are run separately in the River/streaming-model environment. 
Run ARF:

```bash
conda activate river-env
python scripts/webbrowsing_train/ARF_Univariate.py --seeds 42
python scripts/webbrowsing_train/ARF_Multivariate.py --seeds 42
```
Run OLR:

```bash
conda activate river-env
python scripts/webbrowsing_train/OLR_Univariate.py 
python scripts/webbrowsing_train/OLR_Multivariate.py 
```

### Table 5: TTM fine-tuning strategies Results

To reproduce the TTM fine-tuning strategies experiments, use the commands below.

### Dataset:
data/filtered/youtube_static.csv

### Notebook-based experiments (tf-env)
```bash
conda activate tf-env
scripts\fine-tuning_TTM\reproduce_fine-tuning.bat
```

### Table 6: Temporal Resolution Results

To reproduce the temporal resolution experiments, use the commands below.

### Dataset:
data/filtered/youtube_pedestrian.csv

```bash
conda activate tf-env
scripts\temporal_resolution\reproduce_tempresolution.bat
```

```bash
conda activate river-env
scripts\temporal_resolution\arf_tempresolution.bat
```

### Outputs
All Model Outputs are saved in: notebooks/results/metrics/

