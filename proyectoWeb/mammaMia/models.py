from django.db import models

# Create your models here.
class Masa(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)    
    
    def __str__(self):
        return self.nombre

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    alergeno = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Pizza(models.Model):
    nombre = models.CharField(max_length=100)
    masa = models.ForeignKey(Masa, on_delete=models.PROTECT, related_name='pizzas')
    ingredientes = models.ManyToManyField(Ingrediente, related_name='pizzas', blank=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} — {self.masa.nombre}"