import threading
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
import joblib
import numpy as np
from PIL import Image
from django.conf import settings

class ModelManager:
    _instance = None
    _lock = threading.Lock()
    _models = {}
    _model_loaded_flags = {}  # Track which models are loaded
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ModelManager, cls).__new__(cls)
                cls._instance._initialize_model_paths()
        return cls._instance
    
    def _initialize_model_paths(self):
        """Initialize model paths and metadata"""
        models_dir = os.path.join(settings.BASE_DIR, 'models_consolidated')
        
        self.model_paths = {
            'cnn_model': {
                'path': os.path.join(models_dir, 'cnn_model_chunk_final_consolidated.h5'),
                'type': 'keras',
                'name': 'CNN (Convolutional Neural Network)',
                'description': 'Deep learning model for image classification'
            },
            'decision_tree': {
                'path': os.path.join(models_dir, 'decision_tree_chunk_final_consolidated.pkl'),
                'type': 'sklearn',
                'name': 'Decision Tree',
                'description': 'Tree-based model for classification'
            },
            'random_forest': {
                'path': os.path.join(models_dir, 'random_forest_chunk_final_consolidated.pkl'),
                'type': 'sklearn', 
                'name': 'Random Forest',
                'description': 'Ensemble of decision trees'
            },
            'xgboost': {
                'path': os.path.join(models_dir, 'xgboost_chunk_final_consolidated.pkl'),
                'type': 'sklearn',
                'name': 'XGBoost',
                'description': 'Gradient boosting algorithm'
            },
            'knn': {
                'path': os.path.join(models_dir, 'knn_chunk_final_consolidated.pkl'),
                'type': 'sklearn',
                'name': 'K-Nearest Neighbors',
                'description': 'Instance-based learning'
            },
            'scaler': {
                'path': os.path.join(models_dir, 'scaler_chunk_final_consolidated.pkl'),
                'type': 'sklearn',
                'name': 'Feature Scaler',
                'description': 'StandardScaler for feature normalization'
            }
        }
        
        # Initialize all models as not loaded
        for model_name in self.model_paths.keys():
            self._model_loaded_flags[model_name] = False
    
    def get_available_models(self):
        """Return list of available models for user selection"""
        available_models = []
        for model_id, model_info in self.model_paths.items():
            # Don't include scaler in user-facing options
            if model_id != 'scaler':
                available_models.append({
                    'id': model_id,
                    'name': model_info['name'],
                    'description': model_info['description'],
                    'type': model_info['type'],
                    'loaded': self._model_loaded_flags.get(model_id, False)
                })
        return available_models
    
    def load_model(self, model_name):
        """Lazy load a specific model only when needed"""
        with self._lock:
            if model_name not in self.model_paths:
                raise ValueError(f"Model {model_name} not found in available models")
            
            # If model already loaded, return it
            if self._model_loaded_flags.get(model_name, False):
                return self._models[model_name]
            
            model_info = self.model_paths[model_name]
            model_path = model_info['path']
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            try:
                if model_info['type'] == 'keras':
                    self._models[model_name] = load_model(model_path)
                elif model_info['type'] == 'sklearn':
                    self._models[model_name] = joblib.load(model_path)
                
                self._model_loaded_flags[model_name] = True
                print(f"✓ Lazy loaded {model_name} successfully")
                return self._models[model_name]
                
            except Exception as e:
                print(f"✗ Error lazy loading {model_name}: {str(e)}")
                raise
    
    def get_model(self, model_name):
        """Get a model, loading it if necessary"""
        if not self._model_loaded_flags.get(model_name, False):
            return self.load_model(model_name)
        return self._models.get(model_name)
    
    def preprocess_image_for_cnn(self, image_path, target_size=(224, 224)):
        """Preprocess image for CNN models"""
        try:
            img = Image.open(image_path)
            img = img.convert('RGB')
            img = img.resize(target_size)
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            return img_array
        except Exception as e:
            print(f"Error preprocessing image for CNN: {str(e)}")
            raise
    
    def preprocess_image_for_ml(self, image_path, target_size=(224, 224)):
        """Preprocess image for traditional ML models"""
        try:
            img = Image.open(image_path)
            img = img.convert('RGB')
            img = img.resize(target_size)
            img_array = np.array(img) / 255.0
            # Flatten image for ML models
            img_array_flat = img_array.flatten().reshape(1, -1)
            
            # Scale features if scaler is available
            scaler = self.get_model('scaler')
            if scaler:
                img_array_flat = scaler.transform(img_array_flat)
            
            return img_array_flat
        except Exception as e:
            print(f"Error preprocessing image for ML: {str(e)}")
            raise
    
    def predict_with_model(self, model_name, image_path):
        """Make prediction using specified model with lazy loading"""
        try:
            # Get model (will load if not already loaded)
            model = self.get_model(model_name)
            if model is None:
                raise ValueError(f"Model {model_name} could not be loaded")
            
            model_info = self.model_paths[model_name]
            
            if model_info['type'] == 'keras':
                # CNN model prediction
                processed_image = self.preprocess_image_for_cnn(image_path)
                prediction = model.predict(processed_image)
                confidence = float(np.max(prediction))
                predicted_class = int(np.argmax(prediction))
                
            else:
                # Traditional ML model prediction
                processed_image = self.preprocess_image_for_ml(image_path)
                
                if hasattr(model, 'predict_proba'):
                    prediction = model.predict_proba(processed_image)
                    confidence = float(np.max(prediction))
                    predicted_class = int(model.predict(processed_image)[0])
                else:
                    prediction = model.predict(processed_image)
                    confidence = 1.0  # Default confidence
                    predicted_class = int(prediction[0])
            
            return predicted_class, confidence
            
        except Exception as e:
            print(f"Error during prediction with {model_name}: {str(e)}")
            raise

# Global model manager instance
model_manager = ModelManager()