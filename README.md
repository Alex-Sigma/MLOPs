# DVC Pipeline: Training & Evaluation Workflow

This repository contains a DVC-based machine learning pipeline for image segmentation, implemented as part of Lesson 9 (MLOps).
The pipeline is fully reproducible, parameterized, and integrated with S3 remote storage.

# Project Overview

The pipeline consists of three stages:

- data_split
  Splits raw pool data into train and test sets based on a region rule.

- train
  Trains a segmentation model using fastai and saves the trained model artifacts.

- evaluate
  Evaluates the trained model on test data and saves visualized results and metrics.

All data, models, and results are tracked with DVC, while code and configuration are tracked with Git.

# Requirements

- Python ≥ 3.10
- uv (dependency manager)
- AWS credentials configured (for S3 access)

# Setup & Usage

## Install dependencies

```
uv sync
```

## Pull data from DVC remote (S3)

```
uv run dvc pull

```

This downloads:

- raw pool data
- cached outputs (if available)

## Run the full pipeline

```
uv run dvc repro

```

DVC will:

- reuse cached stages when possible
- re-run only outdated stages
- restore outputs automatically

## Pipeline Stages

- data_split

Splits raw data into train and test datasets.
Controlled by parameters in params.yaml

- train

Trains a segmentation model and saves:
models/model.pkl
models/model.pth

- evaluate
  Evaluates the model and saves visual results under

# Remote Storage

DVC remote: AWS S3
All data, models, and results are versioned and stored remotely
Git contains only lightweight metadata
