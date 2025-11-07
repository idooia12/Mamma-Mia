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

def todasLasMasas(request):
    masas = Masa.objects.all().order_by('nombre')
    return render(request, 'mammaMia/todasMasas.html', {'masas': masas})

def todosLosIngredientes(request):
    ingredientes = Ingrediente.objects.all().order_by('nombre')
    return render(request, 'mammaMia/todosIngredientes.html', {'ingredientes': ingredientes})


def todasLasPizzas(request):
    pizzas = Pizza.objects.all().order_by('precio')
    masas = Masa.objects.all().order_by('nombre')
    ingredientes = Ingrediente.objects.all().order_by('nombre')
    
    # Obtenemos los filtros enviados desde el formulario
    masa_id = request.GET.get('masa')
    ingredientes_ids = request.GET.getlist('ingredientes')

    # Filtro por masa
    if masa_id:
        pizzas = pizzas.filter(masa_id=masa_id)

    # Filtro por ingredientes (todas las seleccionadas deben estar en la pizza)
    if ingredientes_ids:
        for ing_id in ingredientes_ids:
            pizzas = pizzas.filter(ingredientes__id=ing_id)

    pizzas = pizzas.distinct()  # evitar duplicados si hay joins

    context = {
        'pizzas': pizzas,
        'masas': masas,
        'ingredientes': ingredientes,
        'masa_seleccionada': masa_id,
        'ingredientes_seleccionados': [int(i) for i in ingredientes_ids],
    }

    return render(request, 'mammaMia/todasPizzas.html', context)


class DetallePizza(DetailView):
    model = Pizza
    template_name = 'mammaMia/detallePizza.html'
    context_object_name = 'pizza'
    
class DetalleMasa(DetailView):
    model = Masa
    template_name = 'mammaMia/detalleMasa.html'
    context_object_name = 'masa'

class DetalleIngrediente(DetailView):
    model = Ingrediente
    template_name = 'mammaMia/detalleIngrediente.html'
    context_object_name = 'ingrediente'