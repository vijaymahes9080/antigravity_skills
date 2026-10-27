---
name: reproducible-data-science
description: Reproducible data science workflows, converting Jupyter notebooks to tested Python modules, deterministic random seeds, dataset schema validation with Great Expectations/Pydantic, and pipeline automation.
---

# Reproducible Data Science & Statistical Engineering

## 1. Intended Role & Domain
- **Primary Domain**: Data Science & Scientific Computing
- **Target Roles**: Data Scientist, Scientific Computing Specialist, Dataset Quality Analyst
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "reproducible data science", "convert jupyter notebook", "dataset quality", "data validation", "statistical analysis", "pandas polars pipeline".
- **Contextual Inferences**: Repositories containing `.ipynb` files, Pandas/Polars scripts, machine learning training pipelines needing deterministic execution.
- **Chained Predecessors**: `task-decomposition`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Simple web layout CSS or frontend component updates.
  - Quick exploratory one-liner data prints where reproducibility is unnecessary.

## 4. Required Inputs & Context
- Raw dataset (CSV, Parquet, JSON, SQL source).
- Exploratory script or Jupyter Notebook (`.ipynb`).
- Target performance metrics (Accuracy, ROC-AUC, F1-score, RMSE) and statistical tests.

## 5. Expected Outputs & Artifacts
- Modular, testable Python scripts (`src/data/`, `src/features/`, `src/models/`).
- Schema validation suite using Great Expectations or Pandera (`schema.py`).
- Deterministic configuration file (`config.yaml`) with explicit random seeds.
- Automated data quality and regression test suite.

## 6. Step-by-Step Operating Procedure
1. **Notebook Deconstruction & Code Extraction**:
   - Extract messy notebook cells into clean, single-responsibility functions.
   - Eliminate hidden state caused by out-of-order notebook cell executions.
2. **Schema & Integrity Validation**:
   - Define strict column types, null thresholds, and valid value ranges using Pandera or Pydantic.
   - Assert validation rules on raw data ingestion before feature transformations.
3. **Deterministic Seeding & Isolation**:
   - Set fixed seeds across all random generators: `random.seed(42)`, `np.random.seed(42)`, `torch.manual_seed(42)`.
   - Prevent data leakage: fit transformers (scalers, encoders) ONLY on training splits; never on the full dataset.
4. **Pipeline Modularization**:
   - Structure pipeline into distinct, reproducible CLI commands (`python -m src.pipeline --step train`).
5. **Statistical Verification & Artifact Persistence**:
   - Compute descriptive statistics, hypothesis tests (p-values, confidence intervals), and log model metrics.

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of data science packages:
  ```bash
  python -c "import pandas, numpy, sklearn; print('Core DS stack verified')" 2>/dev/null || echo "DS libs missing"
  find . -name "*.ipynb" -o -name "*.parquet" -o -name "*.csv"
  ```
- Preservation rule: Never modify raw input data in-place; always write processed data to separate versioned directories.

## 8. Tool & Dependency Requirements
- Python 3.10+, Pandas or Polars, NumPy, Scikit-learn, Pandera / Great Expectations, PyYAML.

## 9. Implementation Guidelines & Best Practices
- Use Polars or DuckDB for multi-gigabyte datasets to eliminate Python GIL and memory bottlenecks.
- Never use magic numbers; externalize parameters in `config.yaml`.

```python
import pandera as pa
from pandera.typing import Series
import pandas as pd

class CustomerDatasetSchema(pa.DataFrameModel):
    customer_id: Series[int] = pa.Field(unique=True, ge=1)
    age: Series[int] = pa.Field(ge=18, le=120)
    churn_status: Series[int] = pa.Field(isin=[0, 1])
    total_spend: Series[float] = pa.Field(ge=0.0)

    class Config:
        strict = True
        coerce = True

def validate_and_process(raw_df: pd.DataFrame) -> pd.DataFrame:
    # Strict runtime validation
    validated_df = CustomerDatasetSchema.validate(raw_df)
    return validated_df
```

## 10. Error Handling & Recovery Procedures
- Missing values in production data: Implement deterministic imputation strategies (median, KNN, explicit 'MISSING' indicator) and log warnings when missingness exceeds 5%.

## 11. Security & Privacy Constraints
- Data Anonymization: Hash or redact Personally Identifiable Information (PII) before saving processed dataset artifacts.

## 12. Verification & Testing Requirements
- Unit test data transformers:
  ```bash
  pytest tests/test_data_pipeline.py -v
  ```
- Assert that model training produces identical metric values across two consecutive runs with identical seed.

## 13. Completion Criteria
- Pipeline executes end-to-end via CLI script with zero manual cell-clicking.
- Data validation schema catches malformed rows cleanly.
- Results are 100% reproducible across runs.

## 14. Relevant Official References
- "Good Enough Practices in Scientific Computing" (Wilson et al., PLOS Comput Biol).
- Pandera Documentation (pandera.readthedocs.io).
- Scikit-learn Pipeline and Model Evaluation Standards.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with Pandas 2.2+, Polars 1.0+, and Scikit-learn 1.5+.
