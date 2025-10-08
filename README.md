# 🏥 Kidney Stone Classification System

## 📖 Project Overview
A comprehensive web-based machine learning application for classifying kidney stones from medical images using multiple deep learning and traditional ML models. This system provides medical professionals with an intuitive interface for uploading kidney images and receiving instant AI-powered analysis with detailed diagnostic reports.

## ✨ Key Features
- **🖼️ Image Upload & Preview** - Drag-and-drop interface for uploading kidney images with real-time preview
- **🤖 Multiple AI Models** - Choose between 6 different trained models (CNN, Random Forest, XGBoost, etc.)
- **⚡ Real-time Prediction** - Instant kidney stone analysis with confidence scores
- **📊 Medical Reports** - Detailed diagnosis with risk assessment and professional recommendations
- **📈 History Tracking** - Automatic saving and review of previous analyses
- **🔐 Secure Authentication** - Custom user system with email-based login for medical professionals
- **📱 Responsive Design** - Works seamlessly on desktop and mobile devices

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Django 4.2+** - Web framework
- **SQLite** - Development database
- **TensorFlow/Keras** - Deep learning models
- **scikit-learn** - Traditional ML models

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript (ES6+)** - Interactive functionality
- **Bootstrap 5** - Responsive design framework
- **Font Awesome** - Icons

### Machine Learning
- **CNN** - Convolutional Neural Network for image classification
- **Random Forest** - Ensemble learning method
- **XGBoost** - Gradient boosting framework
- **K-Nearest Neighbors** - Instance-based learning
- **Decision Trees** - Rule-based classification

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Installation Steps

1. **Clone the Repository**
   \`\`\`bash
   git clone <your-repository-url>
   cd KindeyStoneClassification
   \`\`\`

2. **Create Virtual Environment**
   \`\`\`bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   \`\`\`

3. **Install Dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Environment Setup**
   \`\`\`bash
   # Copy environment template
   cp .env.example .env
   # Edit .env with your configuration
   \`\`\`

5. **Database Setup**
   \`\`\`bash
   python manage.py migrate
   python manage.py createsuperuser
   \`\`\`

6. **Run Development Server**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

7. **Access Application**
   Open your browser and navigate to: \`http://127.0.0.1:8000\`

## 📁 Project Structure

### 🎯 Core Application Files
- **\`manage.py\`** - Django project management script
- **\`requirements.txt\`** - Python dependencies and packages
- **\`README.md\`** - Project documentation (this file)
- **\`.env\`** - Environment variables (security-sensitive, excluded from Git)
- **\`.gitignore\`** - Git ignore rules for sensitive files

### ⚙️ Project Configuration
- **\`KindeyStoneClassification/\`** - Main project settings
  - \`settings.py\` - Django configuration and settings
  - \`urls.py\` - Main URL routing
  - \`wsgi.py\` - Web Server Gateway Interface

### 🏥 Classification App (Main Functionality)
- **\`classification/\`** - Kidney stone classification core logic
  - \`models.py\` - Database models for classification history
  - \`views.py\` - Business logic and view handlers
  - \`urls.py\` - App URL routes
  - \`admin.py\` - Django admin configuration
  - **\`ml_utils/\`** - Machine learning utilities
    - \`model_loader.py\` - ML model loading and prediction functions

### 👤 User Authentication
- **\`user/\`** - Custom user management
  - \`models.py\` - CustomUser model with email authentication
  - \`views.py\` - Registration and login views
  - \`urls.py\` - Authentication routes
  - \`forms.py\` - User forms

### 🎨 Frontend & Templates
- **\`templates/\`** - HTML templates
  - \`base.html\` - Main template structure
  - **\`classification/\`**
    - \`dashboard.html\` - Main classification interface
  - **\`user/\`**
    - \`login.html\` - User login page
    - \`register.html\` - User registration page

- **\`static/\`** - Frontend assets
  - **\`css/\`** - Stylesheets
    - \`style.css\` - Main styling
    - \`dashboard.css\` - Dashboard-specific styles
  - **\`js/\`** - JavaScript
    - \`dashboard.js\` - Main application logic

### 🤖 Machine Learning Models
- **\`models_consolidated/\`** - Trained ML models
  - \`cnn_model_chunk_final_consolidated.h5\` - CNN model weights
  - \`random_forest_chunk_final_consolidated.pkl\` - Random Forest model
  - \`xgboost_chunk_final_consolidated.pkl\` - XGBoost model
  - \`decision_tree_chunk_final_consolidated.pkl\` - Decision Tree model
  - \`knn_chunk_final_consolidated.pkl\` - K-Nearest Neighbors model
  - \`scaler_chunk_final_consolidated.pkl\` - Data scaler
  - \`training_history_chunk_final_consolidated.json\` - Training history

## 🎯 Usage Guide

### For Medical Professionals

1. **Registration & Login**
   - Create an account with professional credentials
   - Login using email and password

2. **Upload Kidney Image**
   - Click "Upload Image" or drag-and-drop kidney stone image
   - Supported formats: PNG, JPG, JPEG
   - Maximum file size: 10MB

3. **Select AI Model**
   - Choose from 6 available models:
     - CNN (Recommended for images)
     - Random Forest
     - XGBoost
     - Decision Tree
     - K-Nearest Neighbors

4. **Analyze & Get Results**
   - Click "Analyze Image" for instant prediction
   - View confidence scores and risk assessment
   - Receive medical recommendations

5. **Review History**
   - Access previous analyses in the sidebar
   - Click on any history item to reload results

### Medical Classification

**Prediction Classes:**
- **🟢 Normal (no stone)** - No kidney stones detected
  - *Risk Level*: Low
  - *Recommendation*: Maintain regular checkups and healthy hydration

- **🔴 Stone** - Kidney stone detected
  - *Risk Level*: Medium-High  
  - *Recommendation*: Consult with a urologist for proper diagnosis

## 🔌 API Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| \`/\` | GET | Main dashboard | Required |
| \`/classification/predict/\` | POST | Image analysis | Required |
| \`/classification/refresh-history/\` | GET | Update history sidebar | Required |
| \`/classification/save-history/\` | POST | Save analysis to history | Required |
| \`/user/login/\` | GET/POST | User login | Optional |
| \`/user/register/\` | GET/POST | User registration | Optional |

## 🔒 Security Features

- **Custom User Authentication** - Email-based login system
- **CSRF Protection** - Built-in Django security
- **File Upload Validation** - Size and type restrictions
- **SQL Injection Prevention** - Django ORM protection
- **Environment Variables** - Sensitive data isolation

## 🧪 Machine Learning Models

### Model Performance
- **CNN Model**: Primary model for image classification with high accuracy
- **Ensemble Methods**: Random Forest and XGBoost for robust predictions
- **Traditional ML**: KNN and Decision Trees for comparative analysis

### Training Data
- Dataset: Kidney stone CT scan images
- Classes: Normal (no stone) vs Stone
- Preprocessing: Image normalization and augmentation

## 🤝 Contributing

We welcome contributions from the community! Please follow these steps:

1. Fork the repository
2. Create a feature branch (\`git checkout -b feature/AmazingFeature\`)
3. Commit your changes (\`git commit -m 'Add some AmazingFeature'\`)
4. Push to the branch (\`git push origin feature/AmazingFeature\`)
5. Open a Pull Request

### Development Setup
\`\`\`bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python manage.py test

# Check code style
flake8 .
\`\`\`

## 📄 License

This project is developed as part of **Domain Core 1 (Machine Learning)** for the Fourth Semester academic program. The code is available for educational and research purposes.

## ⚠️ Medical Disclaimer

**Important**: This application is designed for educational and research purposes only. It is not intended for actual medical diagnosis or treatment. 

- Always consult qualified healthcare professionals for medical diagnoses
- The AI predictions should be verified by medical experts
- The developers are not liable for any medical decisions made based on this software
- Use this tool as a supplementary aid, not a replacement for professional medical advice


---

**Developed with ❤️ for Medical Education and Research**
