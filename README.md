# Proyecto Veterinaria - Comandos Docker

## Pasos para ejecutar la aplicación

### 1. Construir los servicios
```bash
docker-compose build
```

### 2. Ejecutar los contenedores
```bash
docker-compose up -d
```

### 3. Verificar que no hay errores
```bash
docker-compose logs
```

### 4. Ver el estado de los servicios
```bash
docker-compose ps
```

### 5. Acceder a la aplicación
Abrir en el navegador: http://localhost:8000/

### 6. Detener los contenedores
```bash
docker-compose down
```
## Comandos adicionales útiles

### Ver logs en tiempo real
docker-compose logs -f

### Crear superusuario Django
docker-compose exec web python manage.py createsuperuser

### Ejecutar migraciones manualmente
docker-compose exec web python manage.py migrate