from django.urls import path
from . import views

app_name = 'classification'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('predict/', views.PredictView.as_view(), name='predict'),
    path('models/', views.GetModelsView.as_view(), name='get_models'),
    path('refresh-history/', views.RefreshHistoryView.as_view(), name='refresh_history'),
]