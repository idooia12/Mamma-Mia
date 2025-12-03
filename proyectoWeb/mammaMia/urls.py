#urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    
    path('pizzas/', views.ListaPizzas.as_view(), name='todas_pizzas'),
    path('masas/', views.ListaMasas.as_view(), name='todas_masas'),
    path('ingredientes/', views.ListaIngredientes.as_view(), name='todos_ingredientes'),
    
    path('masa/<int:pk>/', views.DetalleMasa.as_view(), name='detalleMasa'),
    path('ingrediente/<int:pk>/', views.DetalleIngrediente.as_view(), name='detalleIngrediente'),
    path('pizza/<int:pk>/', views.DetallePizza.as_view(), name='detallePizza'),
]
