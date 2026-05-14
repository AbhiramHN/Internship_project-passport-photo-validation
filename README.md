# Passport Photo Validator

A web application that validates passport-sized photos using computer vision. It checks file format, image quality, face detection, head pose, background, and accessories.

---

## Requirements

* Python 3.9+
* XAMPP (Apache)
* Git

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

### Start Backend (Flask)

```bash
python api.py
```

Once running:

```
http://127.0.0.1:5000
```

---

### Start Frontend (PHP)

1. Copy the `frontend` files (index.php and result.php) to:

```
C:\xampp\htdocs\passport\
```

2. Start Apache in XAMPP

3. Open:

```
http://localhost/passport/
```

---

## How to Use

* Upload an image (`.jpg`, `.jpeg`, `.png`)
* Click **Validate**
* View result (Valid / Invalid with reasons)

---

## Validation Checks

| Check       | Description                      |
| ----------- | -------------------------------- |
| File        | Format and file size             |
| Quality     | Blur detection                   |
| Face        | Exactly one face must be present |
| Pose        | Head must be straight            |
| Background  | Plain background                 |
| Accessories | No cap or sunglasses             |

---
