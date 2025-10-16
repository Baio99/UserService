## 📦 Versión y Autor
- **Versión:** 1.0.0  
- **Autor:** Adrián Iza 
- **Rol:** Desarrollador Backend  
- **Stack:** FastAPI · MongoDB · RabbitMQ · Docker · Railway  


# Reto 1: User Service - CRUD API

API REST para gestión de usuarios desarrollada con FastAPI y MongoDB.

## Tecnologías

- Python 3.11
- FastAPI
- MongoDB (Motor - async driver)
- Bcrypt (encriptación de contraseñas)
- Pydantic (validaciones)
- Docker

## Configuración de la Base de Datos

### MongoDB Atlas

1. La base de datos ya está configurada en MongoDB Atlas
2. El cluster está disponible en: `cluster0.e0yzybl.mongodb.net`
3. La base de datos `users_db` y la colección `users` se crearán automáticamente al insertar el primer documento

### Conexión

No es necesario crear manualmente la base de datos ni la colección. MongoDB las creará automáticamente cuando se ejecute la primera operación de inserción.

## Instalación Local

### 1. Clonar o descargar el proyecto

```bash
cd user_service
```

### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
MONGODB_URI=mongodb+srv://bayini99_db_user:prueba01@cluster0.e0yzybl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
DATABASE_NAME=users_db
```

### 5. Ejecutar la aplicación

```bash
python main.py
```

O usando uvicorn directamente:

```bash
uvicorn main:app --reload
```

La API estará disponible en: `http://localhost:8000`

## Documentación

## Local

- API : `http://localhost:8000/`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Produccion

- API : `https://userservice-production-3871.up.railway.app/`
- Swagger UI: `https://userservice-production-3871.up.railway.app/docs`
- ReDoc: `https://userservice-production-3871.up.railway.app/redoc`

## Endpoints

### 1. Crear Usuario
- **POST** `/users/`
- **Body:**
```json
{
  "name": "Juan Pérez",
  "email": "juan.perez@example.com",
  "password": "password123"
}
```
- **Respuesta exitosa (201):**
```json
{
  "_id": "65f8a1b2c3d4e5f6g7h8i9j0",
  "name": "Juan Pérez",
  "email": "juan.perez@example.com"
}
```

### 2. Obtener Usuario por ID
- **GET** `/users/{id}`
- **Respuesta exitosa (200):**
```json
{
  "_id": "65f8a1b2c3d4e5f6g7h8i9j0",
  "name": "Juan Pérez",
  "email": "juan.perez@example.com"
}
```

### 3. Actualizar Usuario
- **PUT** `/users/{id}`
- **Body (todos los campos son opcionales):**
```json
{
  "name": "Juan Carlos Pérez",
  "email": "juancarlos@example.com",
  "password": "newpassword456"
}
```

### 4. Eliminar Usuario
- **DELETE** `/users/{id}`
- **Respuesta exitosa (204):** Sin contenido

## Ejemplos de Uso

### Con curl

**Crear usuario:**
```bash
curl -X POST "http://localhost:8000/users/" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Juan Pérez\",\"email\":\"juan.perez@example.com\",\"password\":\"password123\"}"
```

**Obtener usuario:**
```bash
curl -X GET "http://localhost:8000/users/65f8a1b2c3d4e5f6g7h8i9j0"
```

**Actualizar usuario:**
```bash
curl -X PUT "http://localhost:8000/users/65f8a1b2c3d4e5f6g7h8i9j0" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Juan Carlos Pérez\"}"
```

**Eliminar usuario:**
```bash
curl -X DELETE "http://localhost:8000/users/65f8a1b2c3d4e5f6g7h8i9j0"
```

### Con Postman

1. **Crear nuevo usuario:**
   - Método: POST
   - URL: `http://localhost:8000/users/`
   - Headers: `Content-Type: application/json`
   - Body (raw JSON):
   ```json
   {
     "name": "María García",
     "email": "maria.garcia@example.com",
     "password": "secure123"
   }
   ```

2. **Obtener usuario:**
   - Método: GET
   - URL: `http://localhost:8000/users/{id_obtenido_del_paso_anterior}`

3. **Actualizar usuario:**
   - Método: PUT
   - URL: `http://localhost:8000/users/{id}`
   - Body (raw JSON):
   ```json
   {
     "name": "María Fernanda García"
   }
   ```

4. **Eliminar usuario:**
   - Método: DELETE
   - URL: `http://localhost:8000/users/{id}`

## Ejecución con Docker

### Construir imagen

```bash
docker build -t user-service .
```

### Ejecutar contenedor

```bash
docker run -d -p 8000:8000 ^
  -e MONGODB_URI=mongodb+srv://bayini99_db_user:prueba01@cluster0.e0yzybl.mongodb.net/?retryWrites=true^&w=majority^&appName=Cluster0 ^
  -e DATABASE_NAME=users_db ^
  --name user-service ^
  user-service
```

## Características Implementadas

✅ CRUD completo de usuarios  
✅ Encriptación de contraseñas con bcrypt  
✅ Validaciones con Pydantic  
✅ Conexión asíncrona a MongoDB con Motor  
✅ Middleware de logging con tiempo de respuesta  
✅ Documentación automática con Swagger  
✅ Manejo de errores HTTP apropiados  
✅ Validación de emails duplicados  
✅ Validación de ObjectId de MongoDB  

## Logs

El middleware registra en consola:
- Método HTTP y ruta de cada petición
- Tiempo de respuesta en segundos
- Código de estado HTTP

Ejemplo:
```
2024-01-15 10:30:45 - INFO - 📨 Request: POST /users/
2024-01-15 10:30:45 - INFO - ⏱️  Response time: 0.1523s | Status: 201
```

## Notas Importantes

- Las contraseñas se encriptan con bcrypt antes de guardarse en la base de datos
- Los emails deben ser únicos en el sistema
- El ObjectId debe ser válido para las operaciones GET, PUT y DELETE
- La base de datos y colección se crean automáticamente en el primer uso