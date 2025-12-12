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

## Postman Collection

A complete Postman collection is included to test all API endpoints.

**File:** `Beeneu_Challenge_API_Enhanced.postman_collection.json`

### Collection Features

- **Users API**: Covers Registration, Listing (with filters), and Updates.
- **Statistics API**: Endpoints for Total Users, Updates, and 24h metrics.
- **End-to-End Flow**: A step-by-step sequence to verify the entire system lifecycle.

---

## Testing

The project includes a comprehensive test suite covering both unit logic and integration scenarios.

### Prerequisites

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Running Tests

You can use the provided `Makefile` shortcuts or run `pytest` directly.

```bash
# Run all tests (Unit + Integration)
make test

# Run Unit Tests only (Handlers & Repositories)
make test-unit

# Run Integration Tests only (Router & RPC flows)
make test-integration

# Generate Coverage Report
make test-coverage
```
