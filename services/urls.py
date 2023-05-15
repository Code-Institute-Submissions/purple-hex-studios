from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_services, name='services'),
    path('<product_id>', views.services_detail, name='service_detail'),
]