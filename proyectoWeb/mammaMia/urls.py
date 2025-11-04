from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pizza/<int:pk>/', views.DetallePizza.as_view(), name='detallePizza'),
    path('pizzas/', views.todasLasPizzas, name='todasLasPizzas'),
]
