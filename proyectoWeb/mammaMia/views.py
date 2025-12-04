from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.http import JsonResponse
import random
from .models import Masa, Ingrediente, Pizza

# --- VISTAS BASADAS EN CLASES ---

class IndexView(TemplateView):
    template_name = 'mammaMia/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        masas = Masa.objects.all()
        pizzas_destacadas = []
        for masa in masas:
            pizza = Pizza.objects.filter(masa=masa).order_by('precio').first()
            if pizza:
                pizzas_destacadas.append(pizza)
        context['pizzas'] = pizzas_destacadas
        return context

class ListaMasas(ListView):
    model = Masa
    # CORREGIDO: Apunta a tu archivo real
    template_name = 'mammaMia/todasMasas.html' 
    context_object_name = 'masas'
    ordering = ['nombre']

class ListaIngredientes(ListView):
    model = Ingrediente
    # CORREGIDO: Apunta a tu archivo real
    template_name = 'mammaMia/todosIngredientes.html'
    context_object_name = 'ingredientes'
    ordering = ['nombre']

class ListaPizzas(ListView):
    model = Pizza
    # CORREGIDO: Apunta a tu archivo real
    template_name = 'mammaMia/todasPizzas.html'
    context_object_name = 'pizzas'
    ordering = ['precio']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtros
        masa_id = self.request.GET.get('masa')
        ingredientes_ids = self.request.GET.getlist('ingredientes')

        if masa_id:
            queryset = queryset.filter(masa_id=masa_id)

        if ingredientes_ids:
            for ing_id in ingredientes_ids:
                if ing_id.isdigit():
                    queryset = queryset.filter(ingredientes__id=int(ing_id))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masas'] = Masa.objects.all().order_by('nombre')
        context['ingredientes'] = Ingrediente.objects.all().order_by('nombre')
        context['masa_seleccionada'] = self.request.GET.get('masa')
        
        ingredientes_ids = self.request.GET.getlist('ingredientes')
        if ingredientes_ids:
            context['ingredientes_seleccionados'] = [int(i) for i in ingredientes_ids if i.isdigit()]
        else:
            context['ingredientes_seleccionados'] = []
            
        return context

# --- VISTAS DETALLE ---

class DetallePizza(DetailView):
    model = Pizza
    # CORREGIDO: Nombre en singular
    template_name = 'mammaMia/detallePizza.html'
    context_object_name = 'pizza'
    
class DetalleMasa(DetailView):
    model = Masa
    # CORREGIDO: Nombre en singular
    template_name = 'mammaMia/detalleMasa.html'
    context_object_name = 'masa'

class DetalleIngrediente(DetailView):
    model = Ingrediente
    # CORREGIDO: Nombre en singular
    template_name = 'mammaMia/detalleIngrediente.html'
    context_object_name = 'ingrediente'

# --- VISTA AJAX ---
class OfertaAjaxView(View):
    def get(self, request, *args, **kwargs):
        ofertas = [
            "¡2x1 en todas las Pizzas Medianas!",
            "Postre gratis con tu pedido superior a 20€",
            "Envío gratis si pides en los próximos 10 minutos",
            "10% de descuento en Masas Finas"
        ]
        oferta_random = random.choice(ofertas)
        return JsonResponse({'mensaje': oferta_random})