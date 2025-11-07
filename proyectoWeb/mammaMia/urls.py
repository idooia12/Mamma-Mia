from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pizza/<int:pk>/', views.DetallePizza.as_view(), name='detallePizza'),
    path('pizzas/', views.todasLasPizzas, name='todasLasPizzas'),
     path('masas/', views.todasLasMasas, name='todasLasMasas'),
    path('masa/<int:pk>/', views.DetalleMasa.as_view(), name='detalleMasa'),
    path('ingredientes/', views.todosLosIngredientes, name='todosIngredientes'),
    path('ingrediente/<int:pk>/', views.DetalleIngrediente.as_view(), name='detalleIngrediente'),
]
