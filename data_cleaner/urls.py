from django.urls import path
from .views import get_raw_data, get_cleaned_data, submit_cleaned_data

urlpatterns = [
    path('raw/<int:batch>/', get_raw_data),
    path('cleaned/<int:batch>/', get_cleaned_data),
    path('submit/', submit_cleaned_data),
]
