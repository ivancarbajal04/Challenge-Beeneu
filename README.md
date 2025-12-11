# Prueba técnica Beeneu

### Consigna:

Se deberán crear:

- un router en FastAPI
- microservicio de usuarios
- microservicio de estadísticas
- colección de Postman para probar los endpoints

Junto con todos los archivos que creas necesarios para poder enviar los mensajes a los servicios. Dichos mensajes los recibirán los dos microservicios mencionados,
comunicándose mediante un publisher.py y un consumer.py, archivos los cuales serán provistos. Sumado a esto, también será provisto el módulo main.py incompleto y un
archivo docker-compose.yaml para que puedas levantar la infraestructura.

### Lógica de negocio:

#### Microservicio de usuarios:

Hay dos tipos de mensajes posibles: Fire and Forget y Remote Procedure Call + Polling.
El evento FF envía un mensaje el cual ejecuta una acción sin esperar respuesta.
El evento RPC envía un mensaje por el cual se queda haciendo polling esperando una respuesta del servicio.

- `REGISTER_USER_RPC`: envía en el payload del mensaje un json con los siguientes campos: nombre, apellido, DNI, dirección
- `LIST_USERS_RPC`: solicita un listado con todos los usuarios registrados que cumplan con los filtros enviados, dichos filtros son los atributos del usuario
- `UPDATE_USER_RPC`: envía en su payload un diccionario que puede tener alguno de los campos nombre, apellido, CUIT, dirección y el campo id que es obligatorio
- `SEND_EMAIL`: enviar un correo al usuario cuando este es registrado (un simple print en el servicio basta)

#### Microservicio de estadistitcas:

- `TOTAL_USERS_RPC`: cantidad total de usuarios registrados
- `TOTAL_UPDATES_RPC`: cantidad total de actualizaciones realizadas sobre usuarios
- `REGISTERED_LAST_24_RPC`: cantidad de usuarios registrados en las últimas 24 horas
- `USER_REGISTERED_EVENT`: puede saber que se registro un usuario
- `USER_UPDATED_EVENT`: puede saber que se actualizo un usuario

Todo tipo de persistencia se hace sobre una lista en memoria. Por favor, Escribir el código en inglés y manejar correctamente los entornos.

Ante cualquier consulta, podés contactarnos.

Éxitos!

---

## 📮 Colección de Postman

Se incluye una colección completa de Postman para probar todos los endpoints del API.

**Archivo:** `Beeneu_Challenge_API_Enhanced.postman_collection.json`

### Endpoints Incluidos

- **Users API** (6 endpoints): Registro, Listado, Filtros, Actualización
- **Statistics API** (3 endpoints): Total usuarios, Total actualizaciones, Últimas 24h
- **Flujo Completo** (7 requests)

---

## 🧪 Testing

Este proyecto incluye una suite de tests con tests unitarios y de integración.

### Instalación

Instalar dependencias de testing:

```bash
pip install -r requirements.txt
```

### Ejecutar Tests

```bash
# Ejecutar todos los tests
make test

# Solo tests unitarios
make test-unit

# Solo tests de integración
make test-integration

# Tests con reporte de coverage
make test-coverage
```
