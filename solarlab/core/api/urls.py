from django.urls import path
from core.api.views import get_data

app_name = 'core'

urlpatterns = [
    path('<str:country>/',get_data),
]