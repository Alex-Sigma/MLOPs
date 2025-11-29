# MLOPs

# DVC Homework — MLOps Course (Lecture 5)

This project demonstrates how to integrate **Data Version Control (DVC)** with
**AWS S3 remote storage** and track datasets in a reproducible way.  
The workflow follows the homework requirements from Lecture 5.

---

## 📌 Homework Tasks (Completed)

1. Configure AWS CLI locally
2. Create S3 bucket for DVC remote storage
3. Download dataset archive from lecturer
4. Create project structure
5. Install DVC
6. Initialize DVC inside the project
7. Configure DVC remote storage (S3)
8. Add dataset into DVC tracking
9. Push dataset to S3
10. Push DVC metafiles to GitHub

---

The dataset itself is **not stored in GitHub** — only the `.dvc` file is stored.
Actual data lives in **DVC cache** (locally) and **remote S3 storage**.

## ⚙️ Installation & Setup

### 1. Install DVC with S3 support

```bash
python3 -m pip install "dvc[s3]"

```

### 2. Initialize DVC

```bash
python3 -m dvc init

```

### 3. Configure DVC remote (AWS S3)

A bucket was created:
dvc-store-voh3osoe

Remote configuration:

```bash
python3 -m dvc remote add -d s3remote s3://dvc-store-voh3osoe/pool_data
git add .dvc/config
git commit -m "Configure DVC remote on S3"

```

### 4. Add dataset to DVC

```bash
python3 -m dvc add Data/pool_data
git add Data/pool_data.dvc Data/.gitignore
git commit -m "Track pool_data dataset with DVC"

```

### 5. Push data to AWS S3

```bash
python3 -m dvc push
```

The dataset is now stored in S3 under:

```bash
s3://dvc-store-voh3osoe/pool_data/files/

```

### 🔄 Reproducibility

Anyone who clones this repository can restore the full dataset by running:

```bash
python3 -m pip install "dvc[s3]"
python3 -m dvc pull

```

DVC will automatically download the data from the configured S3 bucket.
