# 📡 API Endpoints - Sistema de Terapeutas

## 🌐 URLs Externas (Públicas)

### Base URL
```
http://localhost:8000/  # Desarrollo local
```

### Página Principal
- **GET** `/` - Interfaz web principal de terapeutas

### Panel de Administración
- **GET** `/admin/` - Panel de administración de Django

---

## 🔌 Endpoints de la API

### 1. **Terapeutas** (`/therapists/`)

#### Operaciones CRUD Básicas
| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| **GET** | `/therapists/` | Listar todos los terapeutas | Query params |
| **POST** | `/therapists/` | Crear nuevo terapeuta | JSON body |
| **GET** | `/therapists/{id}/` | Obtener terapeuta específico | `id` en path |
| **PUT** | `/therapists/{id}/` | Actualizar terapeuta completo | `id` + JSON body |
| **PATCH** | `/therapists/{id}/` | Actualizar terapeuta parcial | `id` + JSON body |
| **DELETE** | `/therapists/{id}/` | Soft delete (marcar inactivo) | `id` en path |

#### Endpoints Especiales
| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| **GET** | `/therapists/inactive/` | Listar terapeutas inactivos | Query params |
| **POST** | `/therapists/{id}/restore/` | Restaurar terapeuta inactivo | `id` en path |

#### Parámetros de Filtrado
```
GET /therapists/?active=true          # Solo activos (default)
GET /therapists/?active=false         # Solo inactivos
GET /therapists/?region=1             # Por ID de región
GET /therapists/?province=5           # Por ID de provincia
GET /therapists/?district=25          # Por ID de distrito
GET /therapists/?search=ana           # Búsqueda por texto
```

#### Campos de Búsqueda
- `first_name`
- `last_name_paternal`
- `last_name_maternal`
- `document_number`
- `document_type`
- `email`
- `phone`
- `address`
- `region_fk__name`
- `province_fk__name`
- `district_fk__name`

---

### 5. **Ubicaciones Geográficas**

#### Regiones (`/regions/`)
| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| **GET** | `/regions/` | Listar todas las regiones | - |
| **GET** | `/regions/{id}/` | Obtener región específica | `id` en path |

#### Provincias (`/provinces/`)
| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| **GET** | `/provinces/` | Listar provincias | Query params |
| **GET** | `/provinces/{id}/` | Obtener provincia | `id` en path |

**Filtros disponibles:**
```
GET /provinces/?region=1              # Por ID de región
GET /provinces/?region_ubigeo=15      # Por código UBIGEO de región
```

#### Distritos (`/districts/`)
| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| **GET** | `/districts/` | Listar distritos | Query params |
| **GET** | `/districts/{id}/` | Obtener distrito | `id` en path |

**Filtros disponibles:**
```
GET /districts/?province=5             # Por ID de provincia
GET /districts/?province_ubigeo=1501   # Por código UBIGEO de provincia
```

---

## 📊 Ejemplos de Respuestas

### Terapeuta Individual
```json
{
  "id": 1,
  "document_type": "DNI",
  "document_number": "12345678",
  "first_name": "Ana",
  "last_name_paternal": "García",
  "last_name_maternal": "López",
  "birth_date": "1990-01-01",
  "gender": "M",
  "phone": "999999999",
  "email": "ana@gmail.com",
  "location": "Lima",
  "address": "Av. Siempre Viva 123",
  "personal_reference": "Referencia",
  "is_active": true,
  "profile_picture": "http://localhost:8000/media/profile_pictures/ana.jpg",
  "region_fk": {
    "id": 15,
    "name": "Lima",
    "ubigeo_code": "15"
  },
  "province_fk": {
    "id": 1501,
    "name": "Lima",
    "ubigeo_code": "1501",
    "region": 15
  },
  "district_fk": {
    "id": 150101,
    "name": "Lima",
    "ubigeo_code": "150101",
    "province": 1501
  }
}
```

### Lista de Regiones
```json
[
  {
    "id": 1,
    "name": "Amazonas",
    "ubigeo_code": "01"
  },
  {
    "id": 15,
    "name": "Lima",
    "ubigeo_code": "15"
  }
]
```

---

## 🔍 Filtros y Búsquedas

### Filtros por Estado
- `active=true` - Solo registros activos (por defecto)
- `active=false` - Solo registros inactivos

### Filtros por Ubicación
- `region={id}` - Filtrar por ID de región
- `province={id}` - Filtrar por ID de provincia  
- `district={id}` - Filtrar por ID de distrito

### Filtros por Código UBIGEO
- `region_ubigeo={code}` - Filtrar por código UBIGEO de región
- `province_ubigeo={code}` - Filtrar por código UBIGEO de provincia

### Búsqueda por Texto
- `search={texto}` - Búsqueda en múltiples campos

---

## 📝 Notas Importantes

1. **Soft Delete**: Los terapeutas no se eliminan físicamente, se marcan como inactivos
2. **Filtros de Ubicación**: Se pueden combinar múltiples filtros
3. **Búsqueda**: La búsqueda es case-insensitive y busca en múltiples campos
4. **Paginación**: Todos los endpoints listan con paginación automática
5. **Relaciones**: Las ubicaciones se incluyen automáticamente en las respuestas

## 🔄 Sistema de Serialización Anidada

### **Para Lectura (GET)**
- **`region_fk`**: Devuelve objeto completo con `id`, `name`, `ubigeo_code`
- **`province_fk`**: Devuelve objeto completo con `id`, `name`, `ubigeo_code`, `region`
- **`district_fk`**: Devuelve objeto completo con `id`, `name`, `ubigeo_code`, `province`

### **Para Escritura (POST/PUT/PATCH)**
- **`region_fk_id`**: Envía solo el ID de la región
- **`province_fk_id`**: Envía solo el ID de la provincia  
- **`district_fk_id`**: Envía solo el ID del distrito

### **Ejemplo de Uso**

**Crear terapeuta:**
```json
{
  "document_type": "DNI",
  "document_number": "12345678",
  "first_name": "Juan",
  "last_name_paternal": "Pérez",
  "gender": "M",
  "birth_date": "1990-01-01",
  "phone": "999999999",
  "email": "juan@gmail.com",
  "region_fk_id": 15,
  "province_fk_id": 1501,
  "district_fk_id": 150101
}
```

**Respuesta con datos completos:**
```json
{
  "id": 1,
  "first_name": "Juan",
  "last_name_paternal": "Pérez",
  "region_fk": {
    "id": 15,
    "name": "Lima",
    "ubigeo_code": "15"
  },
  "province_fk": {
    "id": 1501,
    "name": "Lima",
    "ubigeo_code": "1501",
    "region": 15
  },
  "district_fk": {
    "id": 150101,
    "name": "Lima",
    "ubigeo_code": "150101",
    "province": 1501
  }
}
```

---

## 🚀 Uso en Otros Módulos

### Integración Básica
```python
import requests

# Obtener terapeutas de una región específica
response = requests.get('http://localhost:8000/therapists/?region=15')
therapists = response.json()

# Obtener provincias de Lima
response = requests.get('http://localhost:8000/provinces/?region_ubigeo=15')
provinces = response.json()
```

### Importación de Modelos
```python
from therapists.models import Therapist, Region, Province, District
from therapists.services import TherapistService

# Usar servicios directamente
therapist_service = TherapistService()
active_therapists = therapist_service.get_active_therapists()
```
