---
name: explainable-ai-xai
description: Explainable AI (XAI) and model interpretability using SHAP, LIME, Integrated Gradients, feature attribution, model fairness auditing, and bias detection for tabular and deep learning models.
---

# Explainable AI (XAI) & Model Interpretability

## 1. Intended Role & Domain
- **Primary Domain**: Artificial Intelligence & Data Science
- **Target Roles**: Explainable AI Specialist, Data Scientist, ML Governance Analyst
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "explainable ai", "xai", "shap values", "lime interpretability", "feature attribution", "model fairness", "bias detection", "model audit".
- **Contextual Inferences**: High-stakes ML models (finance, healthcare, credit scoring, hiring), regulatory compliance audits (EU AI Act).
- **Chained Predecessors**: `reproducible-data-science`, `task-decomposition`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Performing raw hyperparameter optimization without any interpretability requirement.
  - Generative creative writing prompts where deterministic attribution is meaningless.

## 4. Required Inputs & Context
- Trained model artifact (scikit-learn, XGBoost, LightGBM, PyTorch, TensorFlow).
- Validation dataset with feature names and target labels.
- Baseline background dataset for reference distribution.

## 5. Expected Outputs & Artifacts
- SHAP summary plot and feature importance ranking.
- Local instance explanations (Waterfall / Force plots).
- Demographic parity and disparate impact fairness report.
- Executive interpretability report documenting key decision boundaries.

## 6. Step-by-Step Operating Procedure
1. **Model & Data Alignment**:
   - Verify feature encodings, missing value imputations, and background dataset representative sampling.
2. **Global Attribution (TreeSHAP / KernelSHAP)**:
   - Compute Shapley values across the test partition to establish global feature importance order.
3. **Local Decision Decomposition (LIME / SHAP Waterfall)**:
   - Explain individual outlier predictions by decomposing output log-odds into additive feature contributions.
4. **Fairness & Bias Auditing**:
   - Compute Disparate Impact Ratio across protected demographic attributes: `DIR = P(Y=1|Protected) / P(Y=1|Privileged)`.
   - Flag disparate impact if DIR < 0.80 (the 80% rule).
5. **Interactive Report Generation**:
   - Compile explanations into reproducible HTML/markdown reports for stakeholders.

## 7. Repository Inspection & Planning Requirements
- Non-destructive dependency check:
  ```bash
  python -c "import shap, lime; print('SHAP version:', shap.__version__)" 2>/dev/null || echo "SHAP not installed"
  ```
- Preservation rule: Never calculate exact KernelSHAP on datasets > 500 instances without background clustering (`shap.kmeans`), as it scales exponentially.

## 8. Tool & Dependency Requirements
- Python 3.10+, `shap`, `lime`, `scikit-learn`, `matplotlib`, `pandas`.

## 9. Implementation Guidelines & Best Practices
- For tree-based models (XGBoost, LightGBM, Random Forest), always use `shap.TreeExplainer` for exact, fast polynomial-time computation.
- For deep learning / black-box APIs, use `shap.KernelExplainer` with k-means background summaries (`shap.sample(X_train, 100)`).

```python
import shap
import xgboost as xgb
import pandas as pd

def compute_model_explanations(model: xgb.XGBClassifier, X_val: pd.DataFrame):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_val)
    
    # Global feature importance
    importance_df = pd.DataFrame({
        'feature': X_val.columns,
        'mean_abs_shap': np.abs(shap_values.values).mean(axis=0)
    }).sort_values('mean_abs_shap', ascending=False)
    
    return explainer, shap_values, importance_df
```

## 10. Error Handling & Recovery Procedures
- Memory exhaustion during SHAP calculation: Subsample background dataset to 100 centroids via `shap.kmeans(X_train, 100)`.
- Categorical encoding errors: Ensure categorical features are consistently ordinal-encoded before passing to the explainer.

## 11. Security & Privacy Constraints
- Data privacy: Ensure sensitive features (e.g. Social Security Numbers, exact medical IDs) are excluded from public explanation visualizations.

## 12. Verification & Testing Requirements
- Verify that additive feature contributions sum to the model output minus base value:
  ```python
  assert np.allclose(shap_values.values.sum(axis=1) + explainer.expected_value, model.predict_proba(X_val)[:, 1], atol=1e-3)
  ```
- Automated test:
  ```bash
  pytest tests/test_model_explainability.py -v
  ```

## 13. Completion Criteria
- Global and local attribution computed without errors.
- Fairness metrics calculated and reported.
- Additivity property mathematically verified.

## 14. Relevant Official References
- "A Unified Approach to Interpreting Model Predictions" (Lundberg & Lee, NeurIPS 2017).
- SHAP Documentation (shap.readthedocs.io).
- EU Artificial Intelligence Act (Transparency & Explainability Requirements).

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Compatible with SHAP 0.45+, XGBoost 2.0+, and Scikit-learn 1.5+.
