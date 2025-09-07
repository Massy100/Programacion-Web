from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class Dog(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, default="Canino")
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='dogs')
    
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    trained = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Dog: {self.name}"
    
class Cat(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, default="Felino")
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='cats')
    
    fur_type = models.CharField(max_length=50)
    indoor = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Cat: {self.name}"
    
class Rabbit(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, default="Conejo")
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='rabbits')
    
    EAR_CHOICES = [
        ('long', 'Long'),
        ('short', 'Short'),
    ]
    ear_type = models.CharField(max_length=20, choices=EAR_CHOICES)
    vaccinated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Rabbit: {self.name}"

