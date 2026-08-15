# HumanTrace — Backend

HumanTrace is an AI-text detection system that uses a fine-tuned **DistilBERT sequence-classification model** to classify text as either **human-written** or **AI-generated**.

This repository contains the backend/API responsible for loading the trained model and serving predictions to the HumanTrace frontend.

---

## Features

* Flask REST API
* DistilBERT-based text classification
* Human vs AI prediction
* Confidence score
* AI probability
* Human probability
* Health-check endpoint
* CORS support for frontend communication
* Local model inference
* JSON-based API requests and responses

---

## Architecture

```text
                    HumanTrace Frontend
                           │
                           │ HTTP POST
                           ▼
                 ┌─────────────────────┐
                 │     Flask API       │
                 │       app.py        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ HumanTracePredictor │
                 │     predict.py      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  DistilBERT Model   │
                 │ Human / AI Classes  │
                 └─────────────────────┘
```

---

## Project Structure

```text
humantrace/
│
├── app.py
│
├── models/
│   ├── train.py
│   ├── predict.py
│   └── evaluate.py
│
├── datasets/
│   ├── loaders/
│   ├── metadata/
│   ├── processed/
│   ├── raw/
│   ├── scripts/
│   ├── splits/
│   └── validation/
│
├── preprocessing/
├── feature_engine/
├── explainability/
├── generation/
├── config/
├── core/
├── api/
├── tests/
├── reports/
├── notebooks/
├── topics/
│
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

The primary backend files are:

| File                 | Purpose                                          |
| -------------------- | ------------------------------------------------ |
| `app.py`             | Flask API and HTTP endpoints                     |
| `models/predict.py`  | Loads the trained model and performs predictions |
| `models/train.py`    | Training pipeline for the DistilBERT classifier  |
| `models/evaluate.py` | Model evaluation                                 |
| `requirements.txt`   | Python dependencies                              |

---

# Model

HumanTrace uses:

```text
distilbert-base-uncased
```

The model was fine-tuned as a binary sequence classifier.

### Classes

```text
0 → human
1 → ai
```

The training data contains:

```text
Human: 992
AI:    2400
```

The model was trained using the HumanTrace dataset pipeline with data from sources including:

* HC3
* RAID
* Wikipedia

The trained model is also available on Hugging Face:

**harkirankaur/humantrace-distilbert**

---

# Prediction Pipeline

When text is submitted to the backend:

```text
Input text
    ↓
Validation
    ↓
DistilBERT tokenizer
    ↓
Tokenization
    ↓
Trained DistilBERT classifier
    ↓
Softmax probabilities
    ↓
Human / AI prediction
    ↓
JSON response
```

The backend returns:

```json
{
  "prediction": "human",
  "confidence": 0.9985,
  "ai_probability": 0.0015,
  "human_probability": 0.9985
}
```

---

# Requirements

Recommended environment:

```text
Python 3.11
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

# Running Locally

Clone the repository:

```powershell
git clone https://github.com/Harkirankaur06/humantrace.git
```

Enter the project:

```powershell
cd humantrace
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

# Starting the API

From the root of the `humantrace` repository:

```powershell
python app.py
```

The API will start on:

```text
http://127.0.0.1:5000
```

You should see:

```text
* Running on http://127.0.0.1:5000
```

---

# API Endpoints

## GET `/`

Returns basic API information.

### Request

```text
GET http://127.0.0.1:5000/
```

### Response

```json
{
  "message": "HumanTrace API is running",
  "status": "ok"
}
```

---

## GET `/health`

Used to verify that the backend is running.

### Request

```text
GET http://127.0.0.1:5000/health
```

### Response

```json
{
  "status": "healthy"
}
```

---

## POST `/predict`

Analyzes submitted text.

### Request

```http
POST /predict
Content-Type: application/json
```

Request body:

```json
{
  "text": "Artificial intelligence is transforming modern software development."
}
```

### Response

```json
{
  "prediction": "ai",
  "confidence": 0.9955,
  "ai_probability": 0.9955,
  "human_probability": 0.0045
}
```

---

# Testing the API

PowerShell can be used to test the endpoint locally.

```powershell
$body = @{
    text = "Artificial intelligence is transforming modern software development and enabling intelligent applications."
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/predict" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

Expected response format:

```text
ai_probability confidence human_probability prediction
-------------- ---------- ----------------- ----------
        0.99       0.99              0.00 ai
```

---

# Error Handling

The API validates incoming requests.

### Empty request

```json
{
  "error": "Request body is required."
}
```

### Invalid text type

```json
{
  "error": "Text must be a string."
}
```

### Empty text

```json
{
  "error": "Text cannot be empty."
}
```

### Prediction errors

Unexpected inference errors are returned as:

```json
{
  "error": "..."
}
```

with an HTTP `500` status.

---

# Model Inference

The `HumanTracePredictor` class in:

```text
models/predict.py
```

is responsible for inference.

It:

1. Loads the tokenizer.
2. Loads the trained DistilBERT model.
3. Detects whether CPU or CUDA is available.
4. Tokenizes incoming text.
5. Runs the model in evaluation mode.
6. Converts logits to probabilities using softmax.
7. Selects the class with the highest probability.
8. Returns the prediction and probability scores.

The model is loaded **once when the Flask application starts**, rather than loading the model for every request.

---

# Training

The training pipeline is located at:

```text
models/train.py
```

The training configuration uses:

```text
Model: distilbert-base-uncased
Maximum sequence length: 512
Learning rate: 2e-5
Batch size: 8
Epochs: 3
Weight decay: 0.01
Seed: 42
```

The model is trained as a two-class classifier:

```text
human
ai
```

After training, the model and tokenizer are saved for inference.

---

# Dataset

HumanTrace uses a dataset pipeline containing human-written and AI-generated text.

The training split currently contains:

```text
AI:     2400
Human:   992
Total:  3392
```

The validation split contains:

```text
AI:      300
Human:   124
Total:   424
```

Training and validation data are stored as JSONL files:

```text
datasets/splits/train.jsonl
datasets/splits/validation.jsonl
```

Each record contains fields such as:

```json
{
  "essay_id": "...",
  "text": "...",
  "label": "human",
  "source": "..."
}
```

---

# Important Note About Detection

HumanTrace is a machine-learning classifier and its predictions should be interpreted as **probabilistic signals**, not definitive proof of authorship.

AI-generated and human-written text can share similar linguistic patterns, and detection performance can vary depending on:

* writing style
* text length
* topic
* editing or paraphrasing
* model/domain differences

The confidence value represents the model's classification confidence, not a guaranteed probability that a particular author wrote the text.

---

# Frontend Integration

The HumanTrace frontend communicates with this backend through the `/predict` endpoint.

The frontend sends:

```json
{
  "text": "Text to analyze..."
}
```

The backend responds with the prediction object.

For local development, the frontend API URL should point to:

```text
http://127.0.0.1:5000
```

---

# CORS

Flask-CORS is enabled so that the frontend and backend can communicate from different local development origins.

```python
CORS(app)
```

---

# Deployment

The backend can be deployed as a Python web service using a WSGI server such as Gunicorn.

For local development:

```powershell
python app.py
```

For a production-style server:

```powershell
gunicorn app:app
```

Deployment environments may require additional memory because Transformer models can consume significant RAM during initialization and inference.

---

# Hugging Face Model

The trained model is hosted separately on Hugging Face:

```text
harkirankaur/humantrace-distilbert
```

The repository contains the model configuration, tokenizer, and model weights required for inference.

---

# Technology Stack

### Backend

* Python
* Flask
* Flask-CORS

### Machine Learning

* PyTorch
* Hugging Face Transformers
* DistilBERT
* NumPy

### Data

* JSONL
* Hugging Face Datasets
* Pandas
* Scikit-learn

### Development

* pytest
* python-dotenv
* Git / GitHub

---

# Current Scope

The backend currently focuses on:

* text classification
* human vs AI prediction
* probability scoring
* REST API communication
* model inference

Document parsing such as PDF and DOCX extraction is handled by the **frontend**, which extracts the document text before sending it to the backend.

---

# License

This project is released under the **MIT License**.

See `LICENSE` for the complete license text.

---

## Author

**Harkiran Kaur**

GitHub:

`https://github.com/Harkirankaur06`

HumanTrace:

`https://github.com/Harkirankaur06/humantrace`
