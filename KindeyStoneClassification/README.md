# Kidney Stone Classification System 🏥

**Version:** 1.0.0  
**Author:** Faraz Khan  
**Repository:** [https://github.com/FarazKhanAI/ML_project_4th_sem.git](https://github.com/FarazKhanAI/ML_project_4th_sem.git)

---

## 🧭 Project Summary

A Django web application that uses machine learning to classify kidney stones from medical images. Provides an intuitive interface for medical professionals to upload images, run AI analysis with multiple models, and view detailed diagnostic reports with risk assessment.

---

## ⚙️ Technologies

* **Backend:** Django 4.2+, Python 3.8+
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
* **Machine Learning:** TensorFlow, Keras, scikit-learn
* **Database:** SQLite
* **Authentication:** Django Custom User Model

---

## ✨ Key Features

* Interactive web interface for image upload and preview
* Multiple ML models (CNN, Random Forest, XGBoost, KNN, Decision Tree)
* Real-time kidney stone classification with confidence scores
* Medical reports with risk assessment and recommendations
* User authentication and analysis history tracking
* Responsive design for desktop and mobile

---

## 🗂️ Project Structure

- **`manage.py`** - Django project management script
- **`requirements.txt`** - Python dependencies and packages
- **`README.md`** - Project documentation
- **`.env`** - Environment variables (security-sensitive)
- **`.gitignore`** - Git ignore rules for sensitive files

### ⚙️ Project Configuration
- **`KindeyStoneClassification/`** - Main project settings
  - `settings.py` - Django configuration and settings
  - `urls.py` - Main URL routing
  - `wsgi.py` - Web Server Gateway Interface

### 🏥 Classification App (Main Functionality)
- **`classification/`** - Kidney stone classification core logic
  - `models.py` - Database models for classification history
  - `views.py` - Business logic and view handlers
  - `urls.py` - App URL routes
  - `admin.py` - Django admin configuration
  - **`ml_utils/`** - Machine learning utilities
    - `model_loader.py` - ML model loading and prediction functions

### 👤 User Authentication
- **`user/`** - Custom user management
  - `models.py` - CustomUser model with email authentication
  - `views.py` - Registration and login views
  - `urls.py` - Authentication routes
  - `forms.py` - User forms

### 🎨 Frontend & Templates
- **`templates/`** - HTML templates
  - `base.html` - Main template structure
  - **`classification/`**
    - `dashboard.html` - Main classification interface
  - **`user/`**
    - `login.html` - User login page
    - `register.html` - User registration page

- **`static/`** - Frontend assets
  - **`css/`** - Stylesheets
    - `style.css` - Main styling
    - `dashboard.css` - Dashboard-specific styles
  - **`js/`** - JavaScript
    - `dashboard.js` - Main application logic

### 🤖 Machine Learning Models
- **`models_consolidated/`** - Trained ML models
  - `cnn_model_chunk_final_consolidated.h5` - CNN model weights
  - `random_forest_chunk_final_consolidated.pkl` - Random Forest model
  - `xgboost_chunk_final_consolidated.pkl` - XGBoost model
  - `decision_tree_chunk_final_consolidated.pkl` - Decision Tree model
  - `knn_chunk_final_consolidated.pkl` - K-Nearest Neighbors model
  - `scaler_chunk_final_consolidated.pkl` - Data scaler
  - `training_history_chunk_final_consolidated.json` - Training history

### 📁 Data Storage
- **`media/uploads/`** - User-uploaded kidney stone images (auto-generated)
- **`classification/migrations/`** - Database migration files
- **`user/migrations/`** - User migration files

---

## 💻 Installation

**Prerequisites:** Python 3.8+, pip, Git

```bash
git clone https://github.com/FarazKhanAI/ML_project_4th_sem.git
cd KindeyStoneClassification
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
Visit: http://127.0.0.1:8000
```
---
## ▶️ Usage (brief)

* **Register/Login** with medical credentials
* **Upload** kidney stone image (PNG, JPG, JPEG)
* **Select** AI model from available options
* **Analyze** to get instant prediction
* **Review** detailed medical report with confidence scores
* **Access** analysis history from sidebar

## 🧠 ML Models Overview

* **CNN:** Convolutional Neural Network for image classification
* **Random Forest:** Ensemble learning method
* **XGBoost:** Gradient boosting framework
* **K-Nearest Neighbors:** Instance-based learning
* **Decision Trees:** Rule-based classification

**Classification:**
* 🟢 **Normal (no stone)** - Low risk, routine monitoring
* 🔴 **Stone detected** - Medium-High risk, medical consultation

## 📊 Features & Metrics

* Binary classification (Normal vs Stone)
* Confidence percentage for predictions
* Risk level assessment
* Medical recommendations
* Analysis history tracking
* Secure user authentication

## 📦 Dependencies

Core requirements in `requirements.txt`:
* Django 4.2+
* TensorFlow
* scikit-learn
* Pillow
* Other ML and web libraries

## 📝 Notes for Developers

* ML models stored in `models_consolidated/` directory
* Custom user model uses email authentication
* Image processing handled by `classification/ml_utils/`
* Frontend logic in `static/js/dashboard.js`
* All sensitive config in `.env` file

---

**⚠️ Medical Disclaimer:** This application is for educational and research purposes only. Always consult qualified healthcare professionals for medical diagnoses.