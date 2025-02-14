# ats_model Project

This repository houses an end-to-end workflow for collecting, cleaning, analyzing, and modeling Against-the-Spread (ATS) data for **NBA** and **CBB** (college basketball) games. The primary goal is to predict cover probabilities and implement robust backtesting procedures for eventual bet sizing strategies such as the Kelly criterion.

## Table of Contents
- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Features](#features)
<!-- - [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
  - [Data Ingestion](#data-ingestion)
  - [Data Cleaning & Feature Engineering](#data-cleaning--feature-engineering)
  - [Model Training & Backtesting](#model-training--backtesting)
- [Roadmap](#roadmap)
- [License & Disclaimer](#license--disclaimer)
- [Contact](#contact) -->

---

## Project Overview
1. **Data Pipeline**: Automated scripts scrape or import raw ATS data (cover percentages, ATS records, and more) for NBA and CBB.
2. **Preprocessing & Feature Engineering**: Scripts to clean and unify raw data, then generate key features (e.g., home/away splits, ATS +/-).
3. **Model Training**: Baseline logistic regression (and potentially advanced models like XGBoost or neural nets in the future) to predict cover probability.
4. **Backtesting**: Walk-forward or time-based splits to validate performance on historical data chronologically.
5. **Kelly Criterion (Future)**: Plan to integrate a bet-sizing strategy once predictive probabilities are well-calibrated.

---

## Directory Structure

- **`data/`**: Raw data never changes, while processed data may be overwritten by cleaning scripts.
- **`scripts/`**: Contains “entry point” scripts (e.g., run your model training with one command).
- **`src/`**: Reusable modules (feature engineering functions, model classes, etc.).
- **`notebooks/`**: Exploratory or educational notebooks that show step-by-step analysis or prototypes.
- **`legacy_code/`**: An archive of older code for reference.

---

## Features
- **Automated Data Scraping**: Pull the latest ATS data from your chosen sources with minimal manual intervention.
- **Flexible Feature Engineering**: Focus on home/away cover% but easily expandable for additional splits like rest days, underdog/favorite, etc.
- **Time-Based Model Evaluation**: Built-in methodology for walk-forward testing to avoid data leakage.
- **Logging & Version Control**: Keep a clear record of which version of the model, data, or script produced each result.

---
