from django.db import models
from django.conf import settings

class ClassificationHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_image = models.ImageField(upload_to='uploads/')
    predicted_class = models.CharField(max_length=100)
    model_used = models.CharField(max_length=100)
    prediction_confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Additional fields for medical context
    clinical_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.predicted_class}"
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Classification Histories'