# TeraQSAR — Backend API

FastAPI backend for an AI-based QSAR research prototype that predicts grouped historical pregnancy-risk categories using molecular descriptors and a trained Random Forest classifier.

## Features

- Molecular descriptor-based prediction
- Random Forest classification pipeline
- Three-class risk category output
- Class probability reporting
- Input validation using Pydantic
- REST API built with FastAPI

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Pandas
- Scikit-learn
- Joblib

## Input Features

The API requires five molecular descriptors:

| Feature | Description |
|---|---|
| `a_acc` | Number of hydrogen-bond acceptors |
| `a_don` | Number of hydrogen-bond donors |
| `b_rotN` | Number of rotatable bonds |
| `SlogP` | Molecular lipophilicity descriptor |
| `Weight` | Molecular weight in g/mol |

## Project Structure

```text
backend/
├── models/
│   ├── teratogenicity_descriptor_rf.joblib
│   └── descriptor_columns.joblib
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone <YOUR_BACKEND_REPOSITORY_URL>
cd TeraQSAR-Backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the API server

```bash
uvicorn main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check whether the API is running |
| GET | `/health` | Check model loading and input features |
| POST | `/predict` | Generate a model prediction |

## API Documentation

Once the server is running, visit:

`http://127.0.0.1:8000/docs`

Use the interactive Swagger UI to test the endpoints.

## Prediction Categories

- **Clinically Acceptable Risk**
- **Moderate Risk**
- **Clinically Unacceptable Risk**

These are grouped historical pregnancy-risk categories used by this research prototype.

## Important Disclaimer

This project is an educational and research prototype. Its predictions are based on historical pregnancy-risk categories and are not a clinically validated assessment of teratogenicity, fetal harm, or drug safety.

The reported class probabilities are model outputs, not the probability that a drug will harm a fetus. Do not use this application to make medical decisions.
