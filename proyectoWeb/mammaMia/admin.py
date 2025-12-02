# mammaMia/admin.py
from django.contrib import admin
from .models import Masa, Ingrediente, Pizza

'''
#Version basica. Register your models here.
admin.site.register(Masa)
admin.site.register(Ingrediente)
admin.site.register(Pizza)

'''
# 1. CONFIGURACIÓN GENERAL DEL PANEL
admin.site.site_header = "🍕 Administración Mamma Mia"
admin.site.site_title = "Portal Mamma Mia"
admin.site.index_title = "Gestión de la Pizzería"

# 2. CONFIGURACIÓN AVANZADA DE MODELOS
@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'alergeno') 
    list_filter = ('alergeno',) # Filtro útil para ver qué ingredientes dan alergia
    search_fields = ('nombre',)

@admin.register(Masa)
class MasaAdmin(admin.ModelAdmin):
    list_display = ('nombre',) 
    search_fields = ('nombre',)
    
@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'masa') 
    list_filter = ('masa', 'ingredientes')
    search_fields = ('nombre', 'descripcion')
    filter_horizontal = ('ingredientes',) 
    fieldsets = (
        ('Datos Principales', {
            'fields': ('nombre', 'precio', 'imagen', 'descripcion')
        }),
        ('Composición', {
            'fields': ('masa', 'ingredientes'),
            'classes': ('collapse',),
        }),
    )
