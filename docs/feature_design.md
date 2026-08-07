# HumanTrace Feature Design

## Objective

HumanTrace identifies measurable differences between human-written and machine-generated text.

The system uses multiple independent feature groups rather than relying on a single metric.

---

# Feature Categories

## 1. Sentence Structure Features

Purpose:

Measure writing rhythm and structural consistency.


Examples:

- Average sentence length
- Sentence length variance
- Long sentence ratio
- Short sentence ratio
- Clause frequency


Why useful:

AI-generated text often produces more uniform sentence structures compared to human writing.

---

# 2. Lexical Diversity Features

Purpose:

Analyze vocabulary usage.


Examples:

- Type Token Ratio
- Moving Average TTR
- Unique word percentage
- Word length distribution


Why useful:

Machine-generated text often has predictable vocabulary patterns.

---

# 3. Readability Features

Purpose:

Measure complexity of writing.


Metrics:

- Flesch Reading Ease
- Flesch-Kincaid Grade Level
- Gunning Fog Index
- SMOG Score


---

# 4. Language Model Features

Purpose:

Measure statistical probability of text.


Features:

- Perplexity
- Token probability
- Probability variance


Reason:

AI text often has lower unpredictability compared to human writing.

---

# 5. Burstiness Features

Purpose:

Measure variation in writing style.


Features:

- Sentence rhythm variation
- Sentence length distribution
- Word frequency variation


---

# 6. Repetition Features

Purpose:

Identify repeated patterns.


Features:

- Bigram repetition
- Trigram repetition
- Phrase repetition
- Sentence similarity


---

# 7. Syntax Features

Purpose:

Analyze grammatical structure.


Features:

- Passive voice ratio
- Dependency depth
- Parse complexity
- Clause structure


---

# 8. Semantic Features

Purpose:

Measure meaning-level patterns.


Features:

- Sentence embeddings
- Semantic similarity
- Topic diversity
- Semantic redundancy


---

# 9. Stylometry Features

Purpose:

Capture individual writing style.


Features:

- Punctuation usage
- Capitalization patterns
- Symbol frequency
- Formatting style


---

# 10. AI Pattern Features

Purpose:

Capture common machine-writing tendencies.


Examples:

- Generic introduction detection
- Template phrase detection
- Excessive transitions
- Balanced argument patterns


---

# Feature Development Strategy

Initial implementation:

~40 high-value features


Final system:

90+ features


Feature importance analysis will determine which features contribute most to prediction.