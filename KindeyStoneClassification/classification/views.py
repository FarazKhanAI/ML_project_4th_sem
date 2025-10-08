import threading
import os
import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.utils import timezone
from .models import ClassificationHistory
from .ml_utils.model_loader import model_manager


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        # Get available models for dropdown
        available_models = model_manager.get_available_models()
        
        # Get user's recent history for sidebar
        user_history = ClassificationHistory.objects.filter(
            user=request.user
        ).order_by('-timestamp')[:10]
        
        return render(request, 'classification/dashboard.html', {
            'available_models': available_models,
            'history': user_history
        })

class PredictView(LoginRequiredMixin, View):
    def post(self, request):
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image uploaded'}, status=400)
        
        # Get selected model from form
        model_choice = request.POST.get('model_choice', 'cnn_model')
        
        # Validate model choice
        available_models = [model['id'] for model in model_manager.get_available_models()]
        if model_choice not in available_models:
            return JsonResponse({'error': 'Invalid model selected'}, status=400)
        
        # Process prediction immediately (for demo) or use threading for large files
        try:
            return self._process_prediction_immediate(request.FILES['image'], request.user, model_choice)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def _process_prediction_immediate(self, image_file, user, model_choice):
        """Process prediction immediately and return results"""
        try:
            # Create upload directory if it doesn't exist
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(image_file.name)[1]
            unique_filename = f"{timestamp}_{user.id}{file_extension}"
            image_path = os.path.join(upload_dir, unique_filename)
            
            # Save uploaded image
            with open(image_path, 'wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
            # Make prediction with lazy loading
            predicted_class, confidence = model_manager.predict_with_model(
                model_choice, 
                image_path
            )
            
            # SIMPLIFIED: Only two classes now
            class_details = {
                0: {
                    'name': 'Normal (no stone)',
                    'description': 'No kidney stones detected. The kidney appears healthy and normal.',
                    'risk_level': 'Low',
                    'recommendation': 'Maintain regular checkups and healthy hydration. Continue with routine kidney health monitoring.'
                },
                1: {
                    'name': 'Stone',
                    'description': 'Kidney stone detected. Further medical evaluation recommended.',
                    'risk_level': 'Medium-High',
                    'recommendation': 'Consult with a urologist for proper diagnosis and treatment plan. Increase fluid intake and follow medical advice.'
                }
            }
            
            prediction_details = class_details.get(predicted_class, {
                'name': f'Class {predicted_class}',
                'description': 'Kidney analysis completed.',
                'risk_level': 'Unknown',
                'recommendation': 'Consult healthcare professional for proper diagnosis.'
            })
            
            # Get model display name
            model_display_name = next(
                (model['name'] for model in model_manager.get_available_models() 
                 if model['id'] == model_choice),
                model_choice
            )
            
            # Save to history
            history_entry = ClassificationHistory.objects.create(
                user=user,
                uploaded_image=f'uploads/{unique_filename}',
                predicted_class=prediction_details['name'],
                model_used=model_display_name,
                prediction_confidence=confidence
            )
            
            # Prepare response data
            result_data = {
                'status': 'success',
                'prediction': {
                    'class_name': prediction_details['name'],
                    'confidence': round(confidence * 100, 2),
                    'description': prediction_details['description'],
                    'risk_level': prediction_details['risk_level'],
                    'recommendation': prediction_details['recommendation'],
                    'model_used': model_display_name,
                    'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                'image': {
                    'url': f'/media/uploads/{unique_filename}',
                    'name': image_file.name,
                    'size': image_file.size
                },
                # Add history entry ID for frontend tracking
                'history_id': history_entry.id
            }
            
            print(f"✓ Prediction completed: {prediction_details['name']} with {confidence:.2f} confidence")
            
            return JsonResponse(result_data)
            
        except Exception as e:
            print(f"✗ Prediction error: {str(e)}")
            return JsonResponse({'error': f'Prediction failed: {str(e)}'}, status=500)

# REMOVED: HistoryView class (no longer needed)

class GetModelsView(LoginRequiredMixin, View):
    """API endpoint to get available models"""
    def get(self, request):
        available_models = model_manager.get_available_models()
        return JsonResponse({'models': available_models})

from django.utils.timesince import timesince  # Add this import at the top

class RefreshHistoryView(LoginRequiredMixin, View):
    """API endpoint to refresh history data for sidebar"""
    def get(self, request):
        user_history = ClassificationHistory.objects.filter(
            user=request.user
        ).order_by('-timestamp')[:10]
        
        # Return HTML snippet for history items in sidebar
        history_html = ""
        for item in user_history:
            # Use the timesince function properly
            time_ago = timesince(item.timestamp)
            
            history_html += f"""
            <div class="history-item" data-history-id="{item.id}">
                <div class="history-main">
                    <div class="history-class">{item.predicted_class}</div>
                    <div class="history-meta">
                        <span class="history-model">{item.model_used}</span>
                        <span class="history-confidence">{item.prediction_confidence:.1f}%</span>
                    </div>
                </div>
                <div class="history-time">{time_ago} ago</div>
            </div>
            """
        
        return JsonResponse({'history_html': history_html})
    


class SaveHistoryView(LoginRequiredMixin, View):
    """API endpoint to save current analysis to history"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Create new history entry
            history_entry = ClassificationHistory.objects.create(
                user=request.user,
                uploaded_image=data.get('image_url', ''),
                predicted_class=data.get('predicted_class', 'Unknown'),
                model_used=data.get('model_used', 'Unknown Model'),
                prediction_confidence=data.get('confidence', 0)
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Analysis saved to history',
                'history_id': history_entry.id
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

class RefreshHistoryView(LoginRequiredMixin, View):
    """API endpoint to refresh history data for sidebar"""
    def get(self, request):
        user_history = ClassificationHistory.objects.filter(
            user=request.user
        ).order_by('-timestamp')[:10]
        
        # Return HTML snippet for history items in sidebar
        history_html = ""
        for item in user_history:
            time_ago = timezone.timesince(item.timestamp)
            
            history_html += f"""
            <div class="history-item" data-history-id="{item.id}">
                <div class="history-main">
                    <div class="history-class">{item.predicted_class}</div>
                    <div class="history-meta">
                        <span class="history-model">{item.model_used}</span>
                        <span class="history-confidence">{item.prediction_confidence:.1f}%</span>
                    </div>
                </div>
                <div class="history-time">{time_ago} ago</div>
            </div>
            """
        
        return JsonResponse({'history_html': history_html})