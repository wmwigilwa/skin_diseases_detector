from django.urls import path
from detector import views

urlpatterns = [
    # Other URL patterns
    path('', views.index, name='index'),
    path('process-image/', views.process_image, name='process_image'),
]
