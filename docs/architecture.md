# HumanTrace Architecture

## Overview

HumanTrace is an explainable authorship intelligence platform designed to analyze whether a piece of writing is human-written, AI-generated, or AI-assisted.

The system does not rely on a single AI classifier or external detection API. Instead, it combines linguistic analysis, statistical measurements, language model signals, and machine learning to generate explainable predictions.

---

# High-Level Pipeline

                User Input

                    |

                    v

          Text Processing Layer

                    |

                    v

            EssayDocument

                    |

                    v

      Feature Extraction Pipeline

                    |

                    v

            Feature Vector

                    |

                    v

         Machine Learning Model

                    |

                    v

          Prediction Engine

                    |

                    v

        Explainability Engine

                    |

                    v

          Analysis Report



---

# System Components

## 1. Input Layer

Responsible for receiving:

- Plain text
- Documents
- Essays
- Future API inputs


The input layer converts all sources into raw text.

---

# 2. Preprocessing Engine

The preprocessing engine converts raw text into structured linguistic information.

Responsibilities:

- Text cleaning
- Paragraph extraction
- Sentence segmentation
- Tokenization
- Lemmatization
- Part-of-speech tagging
- Dependency parsing


Output:
EssayDocument


---

# 3. Feature Extraction Engine

The feature engine extracts measurable writing characteristics.

Feature categories:

- Lexical diversity
- Sentence structure
- Syntax patterns
- Readability
- Stylometry
- Repetition
- Semantic similarity
- Language model statistics
- Discourse patterns


Output:
FeatureVector


---

# 4. Machine Learning Layer

The ML layer receives numerical features and predicts authorship characteristics.

Possible models:

- LightGBM
- XGBoost
- Random Forest
- Logistic Regression baseline


The model does not directly read text.

It only receives engineered features.

---

# 5. Explainability Engine

The explainability layer converts model decisions into understandable evidence.

Examples:

- Low vocabulary diversity
- Highly uniform sentence rhythm
- Low perplexity
- Repeated sentence structures


Techniques:

- Feature importance
- SHAP values
- Sentence-level scoring


---

# 6. Reporting Layer

The reporting system generates structured results.

Outputs:

- JSON reports
- PDF reports
- Frontend API responses


---

# Design Principles

## Modular Architecture

Each component performs one responsibility.

Example:

Feature extraction should not perform preprocessing.

---

## Explainability First

Every prediction should have supporting evidence.

---

## Extensible Design

New features or models should be added without rewriting the system.

---

## Reproducibility

Dataset versions, model versions, and feature versions are tracked.

