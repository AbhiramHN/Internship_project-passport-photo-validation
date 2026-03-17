# Passport Photo Validator

A Streamlit application that validates passport-sized photos of students using computer vision. It checks file format, image quality, face detection, head pose, background, and accessories (cap detection).

---

## Requirements

- Python 3.9+
- Git

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AbhiramHN/Internship_project-passport-photo-validation.git
cd Internship_project-passport-photo-validation
```

### 2. Create and Activate a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```

Once running, open your browser and go to:

```
http://localhost:8501
```

---

## How to Use

- **Select a Dataset Image** — pick from the dropdown and use the `← Prev` / `Next →` arrows to browse
- **Upload an Image** — upload your own `.jpg`, `.jpeg`, or `.png` file
- **Validate Photo** — click the button to run all validation checks and see the result

---

## Validation Checks

| Check | Description |
|-------|-------------|
| File | Format and file size (max 300 KB) |
| Quality | Blur detection |
| Face | Exactly one face must be present |
| Pose | Head must be straight and facing forward |
| Background | Must be plain and non-textured |
| Accessories | No cap/hat allowed |

---
