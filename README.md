# Secure Message Sharing App

Una aplicación segura para compartir mensajes que se autodestruyen después de ser vistos una vez, similar a scrt.link.

## Ejecución Rápida

**Solo se necesita un comando para ejecutar toda la aplicación:**

```bash
docker compose up --build
```

## Acceso a la Aplicación
Una vez que todos los contenedores estén en verde, accede a:

### Aplicación Principal (Frontend)
URL: http://localhost:5173/

### Base de Datos (Redis Commander)
URL: http://localhost:8081/

### API Backend
URL: http://127.0.0.1:8000/api/health/

### Servicios Incluidos
La aplicación consta de 4 servicios que se ejecutan automáticamente:

- Frontend: Aplicación React en puerto 5173

- Backend: API Django en puerto 8000

- Redis: Base de datos en puerto 6379

- Redis Commander: Interfaz visual para Redis en puerto 8081