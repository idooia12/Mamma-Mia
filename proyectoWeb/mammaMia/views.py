#mammaMia/views.py
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from .models import Masa, Ingrediente, Pizza

#VISTAS BASADAS EN CLASES (OPCION 2)

'''
def index(request):
    masas = Masa.objects.all()
    pizzas_destacadas = []
    for masa in masas:
        pizza = Pizza.objects.filter(masa=masa).order_by('precio').first()
        if pizza:
            pizzas_destacadas.append(pizza)

    return render(request, 'mammaMia/index.html', {'pizzas': pizzas_destacadas})
'''

class IndexView(TemplateView):
    template_name = 'mammaMia/index.html'

    def get_context_data(self, **kwargs):
        # Recuperamos el contexto base
        context = super().get_context_data(**kwargs)
        
        # Lógica original: buscar la pizza más barata de cada masa
        masas = Masa.objects.all()
        pizzas_destacadas = []
        for masa in masas:
            pizza = Pizza.objects.filter(masa=masa).order_by('precio').first()
            if pizza:
                pizzas_destacadas.append(pizza)
        
        # Añadimos la variable al contexto
        context['pizzas'] = pizzas_destacadas
        return context

class ListaMasas(ListView):
    model = Masa
    template_name = 'mammaMia/todasMasas.html'
    context_object_name = 'masas'
    ordering = ['nombre'] # Ordenar por nombre

class ListaIngredientes(ListView):
    model = Ingrediente
    template_name = 'mammaMia/todosIngredientes.html'
    context_object_name = 'ingredientes'
    ordering = ['nombre']

class ListaPizzas(ListView):
    model = Pizza
    template_name = 'mammaMia/todasPizzas.html'
    context_object_name = 'pizzas'
    ordering = ['precio'] # Orden por defecto

    #Sobreescribir este metodo para aplicar los filtros
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros de la URL (GET)
        masa_id = self.request.GET.get('masa')
        ingredientes_ids = self.request.GET.getlist('ingredientes')

        # Filtro por masa
        if masa_id:
            queryset = queryset.filter(masa_id=masa_id)

        # Filtro por ingredientes
        if ingredientes_ids:
            for ing_id in ingredientes_ids:
                queryset = queryset.filter(ingredientes__id=ing_id)

        return queryset.distinct()

    #Sobreescribir método para enviar datos EXTRA al template y que pueda pintar el formulario de filtros.
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        # Listas para rellenar los selects/checkbox del formulario
        context['masas'] = Masa.objects.all().order_by('nombre')
        context['ingredientes'] = Ingrediente.objects.all().order_by('nombre')
        
        # Mantener lo seleccionado para que no se borre al filtrar
        context['masa_seleccionada'] = self.request.GET.get('masa')
        ingredientes_ids = self.request.GET.getlist('ingredientes')
        
        # Convertimos a enteros para poder comparar en el template
        if ingredientes_ids:
            context['ingredientes_seleccionados'] = [int(i) for i in ingredientes_ids if i.isdigit()]
        else:
            context['ingredientes_seleccionados'] = []
            
        return context

# VISTAS DETALLE
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