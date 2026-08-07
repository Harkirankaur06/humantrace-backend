# Dataset Strategy

## Objective

HumanTrace requires a balanced dataset containing both human-written and AI-generated essays.

The dataset should represent realistic academic writing scenarios.

---

# Dataset Classes


## Human Essays

Sources:

- Public essay datasets
- Student writing datasets
- Open educational resources


Examples:

- Argumentative essays
- Opinion essays
- Academic responses


---

## AI Generated Essays

Generated using:

- GPT models
- Open-source LLMs
- Different prompting styles


Prompts should include:

- Academic essays
- Personal narratives
- Explanations
- Research summaries


---

# Dataset Structure

dataset/
├── human/
│ ├── essay_001.txt
│ └── essay_002.txt
├── ai/
│ ├── essay_001.txt
│ └── essay_002.txt



---

# Data Processing

Each essay passes through:

1. Cleaning
2. Preprocessing
3. Feature extraction
4. Label assignment


Labels:
0 = Human

1 = AI Generated


---

# Evaluation Strategy

Dataset split:
Training: 70%

Validation: 15%

Testing: 15%


---

# Error Analysis

The system will document:

- False positives
- False negatives
- Cases involving non-native English writers
- AI-assisted human writing


---

# Limitations

The dataset may not represent:

- Every writing style
- Every language background
- Every AI model


Results will be reported honestly.