from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from .models import Masa, Ingrediente, Pizza
# Create your views here.

from django.shortcuts import render
from .models import Pizza

def index(request):
    masas = Masa.objects.all()
    pizzas_destacadas = []
    for masa in masas:
        pizza = Pizza.objects.filter(masa=masa).order_by('precio').first()
        if pizza:
            pizzas_destacadas.append(pizza)

    return render(request, 'mammaMia/index.html', {'pizzas': pizzas_destacadas})

class DetallePizza(DetailView):
    model = Pizza
    template_name = 'mammaMia/detallePizza.html'
    context_object_name = 'pizza'