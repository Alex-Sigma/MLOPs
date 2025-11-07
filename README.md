# MLOps Homework 1 – Dependency Control

This repository contains the solution for **Lesson 1: Controlling Dependencies** from the MLOps course.

## 📁 Project Overview

The goal of this task was to demonstrate proper **dependency management** using the modern package manager **[`uv`](https://github.com/astral-sh/uv)**.

Following the assignment instructions, all dependencies were added, structured, and exported according to best practices.

---

## 🧩 Steps Performed

1. **Initialized the project**

   ```bash
   python3 -m uv init

   ```

2. **Installed main dependencies**
   python3 -m uv add numpy pandas scikit-learn

3. **Installed development dependencies**
   python3 -m uv add --dev pre-commit

4. **Exported all dependencies**
   python3 -m uv export -o requirements.txt

5. **Committed and pushed to GitHub**
   git add pyproject.toml requirements.txt
   git commit -m "Add deps via uv and export requirements"
   git push
