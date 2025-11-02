from django.contrib import admin
from .models import Masa, Ingrediente, Pizza

# Register your models here.

@admin.register(Masa)
class MasaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nombre','alergeno')
    search_fields = ('nombre',)
    list_filter = ('alergeno',)

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('nombre','masa','precio','disponible')
    list_filter = ('masa','disponible')
    search_fields = ('nombre','descripcion')
    filter_horizontal = ('ingredientes',)