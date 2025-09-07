from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

# Modelo abstracto Pet
class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='pets')
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return f"{self.name} ({self.species})"