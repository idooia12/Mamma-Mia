from django.urls import path
from . import views

urlpatterns = [
    # Inicio
    path('', views.IndexView.as_view(), name='index'),

    # Listados (Coincidiendo con tus templates: todasLasPizzas, todasLasMasas...)
    path('pizzas/', views.ListaPizzas.as_view(), name='todasLasPizzas'),
    path('masas/', views.ListaMasas.as_view(), name='todasLasMasas'),
    path('ingredientes/', views.ListaIngredientes.as_view(), name='todosIngredientes'),

    # Detalles
    path('pizza/<int:pk>/', views.DetallePizza.as_view(), name='detallePizza'),
    path('masa/<int:pk>/', views.DetalleMasa.as_view(), name='detalleMasa'),
    path('ingrediente/<int:pk>/', views.DetalleIngrediente.as_view(), name='detalleIngrediente'),

    # API Ajax
    path('api/oferta/', views.OfertaAjaxView.as_view(), name='oferta_ajax'),
]