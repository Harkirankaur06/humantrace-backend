# Model Development Notes

## Objective

Build a classifier capable of identifying AI-generated writing using explainable features.

---

# Model Approach

HumanTrace follows a feature-based machine learning approach.

The language model is not responsible for making the final decision.

It is only used to extract statistical signals.

---

# Pipeline

Essay
↓
Feature Extraction
↓
Feature Vector
↓
Classifier
↓
Prediction
↓
Explanation



---

# Candidate Models


## Baseline

Logistic Regression

Purpose:

Establish initial performance.


---

## Random Forest

Advantages:

- Handles nonlinear patterns
- Provides feature importance


---

## XGBoost / LightGBM

Advantages:

- Strong performance on structured data
- Handles feature interactions
- Works well with engineered features


---

# Explainability

The system will use:

## SHAP

To identify:

- Which features influenced predictions
- Positive and negative contributors


Example:


Prediction:

AI likelihood = 82%


Reasons:
Low burstiness +15%

High repetition +12%

Low lexical diversity +10%



---

# Evaluation Metrics

The model will be evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC


---

# Future Improvements

Possible future directions:

- Transformer fine-tuning
- Multilingual detection
- Continuous learning
- Larger writing-style datasets
- Human-AI collaboration detection

