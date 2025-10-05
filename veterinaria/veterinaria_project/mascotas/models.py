from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class AnimalType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class AnimalBreed(models.Model):
    name = models.CharField(max_length=100)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, related_name='breeds')
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.animal_type.name})"

class Animal(models.Model):
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]
    
    EAR_CHOICES = [
        ('long', 'Long'),
        ('short', 'Short'),
    ]
    
    name = models.CharField(max_length=100)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, related_name='animals')
    breed = models.ForeignKey(AnimalBreed, on_delete=models.CASCADE, related_name='animals')
    age = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='animals')
    
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, blank=True, null=True)
    trained = models.BooleanField(default=False)
    
    fur_type = models.CharField(max_length=50, blank=True, null=True)
    indoor = models.BooleanField(default=True)
    ear_type = models.CharField(max_length=20, choices=EAR_CHOICES, blank=True, null=True)
    vaccinated = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.animal_type.name}: {self.name} (Owner: {self.owner.name})"