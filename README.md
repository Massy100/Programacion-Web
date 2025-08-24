# CDN: [d17ztf8mfjui20.cloudfront.net](https://d17ztf8mfjui20.cloudfront.net/)

# HOOKS:
## 1. useState - Gestión de Estado Local
**Propósito:** Gestionar el estado interno de los componentes.

**Implementación:**

```bash
jsx
// Para el estado del filtro activo
const [filter, setFilter] = useState('all');
```
```bash
// Para el input de nueva tarea
const [taskName, setTaskName] = useState('');
```

**Razón de uso:**
- Manejar estados simples que no requieren persistencia
- Actualizar la UI de forma reactiva cuando cambia el estado
- Sencillo y eficiente para estados independientes

## 2. useEffect - Efectos Secundarios (uso interno)
**Propósito:** Sincronizar el estado de React con APIs externas (localStorage).

**Implementación (dentro del custom hook):**

```bash
javascript
// Efecto para guardar en localStorage cuando cambia el valor
useEffect(() => {
  window.localStorage.setItem(key, JSON.stringify(storedValue));
}, [key, storedValue]);
```

**Razón de uso:**
- Automatizar la persistencia de datos
- Responder a cambios en el estado de la aplicación

## 3. Custom Hook: useLocalStorage - Persistencia de Estado
**Propósito:** Sincronizar el estado de React con el localStorage del navegador.

**Implementación:**

```bash
javascript
const [tasks, setTasks] = useLocalStorage('tasks', []);
```

**Razón de uso:**
- Abstracción: Simplifica la compleja lógica de localStorage
- Reutilización: Puede usarse en cualquier componente
- Mantenibilidad: Centraliza el manejo de errores
- Sincronización automática: Los datos persisten tras recargar la página

**Funcionamiento interno:**
- Inicialización: Lee del localStorage al montar el componente
- Persistencia: Guarda automáticamente en cada cambio
- Manejo de errores: Captura errores de localStorage

## 4. useState con Función Inicializadora - Optimización
**Propósito:** Optimizar el rendimiento evitando acceder a localStorage en cada render.

**Implementación:**
```bash
javascript
const [storedValue, setStoredValue] = useState(() => {
  // Lógica que solo se ejecuta en el render inicial
  const item = window.localStorage.getItem(key);
  return item ? JSON.parse(item) : initialValue;
});
```

**Razón de uso:**
- Rendimiento: Evita operaciones costosas en cada render
- Lazy initialization: La función solo se ejecuta una vez
- Prevención de errores: Evita problemas en entornos SSR

