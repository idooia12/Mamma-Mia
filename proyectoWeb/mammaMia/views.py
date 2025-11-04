from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from .models import Masa, Ingrediente, Pizza
# Create your views here.

from django.shortcuts import render
from .models import Pizza

def index(request):
    pizzas = Pizza.objects.all()  # Consulta todas las pizzas
    return render(request, 'mammaMia/index.html', {'pizzas': pizzas})