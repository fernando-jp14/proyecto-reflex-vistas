# 📚 DOCUMENTACIÓN DE ENDPOINTS - MÓDULO 5 (APPOINTMENTS_STATUS)

## 🎯 **INFORMACIÓN GENERAL**

**Base URL:** `http://localhost:8000/appointments/api/`  
**Autenticación:** Requerida (Session/Basic Authentication)  
**Formato:** JSON  
**Namespace:** `appointments_status`

---

## 📋 **ÍNDICE DE ENDPOINTS**

### **1. APPOINTMENT STATUS (Estados de Citas)**
- [Listar Estados](#listar-estados-de-citas)
- [Crear Estado](#crear-estado-de-cita)
- [Obtener Estado](#obtener-estado-específico)
- [Actualizar Estado](#actualizar-estado)
- [Eliminar Estado](#eliminar-estado)
- [Estados Activos](#estados-activos)
- [Activar Estado](#activar-estado)
- [Desactivar Estado](#desactivar-estado)
- [Citas por Estado](#citas-por-estado)

### **2. APPOINTMENTS (Citas)**
- [Listar Citas](#listar-citas)
- [Crear Cita](#crear-cita)
- [Obtener Cita](#obtener-cita-específica)
- [Actualizar Cita](#actualizar-cita)
- [Eliminar Cita](#eliminar-cita)
- [Citas Completadas](#citas-completadas)
- [Citas Pendientes](#citas-pendientes)
- [Citas por Rango de Fecha](#citas-por-rango-de-fecha)
- [Cancelar Cita](#cancelar-cita)
- [Reprogramar Cita](#reprogramar-cita)

### **3. TICKETS (Tickets)**
- [Listar Tickets](#listar-tickets)
- [Crear Ticket](#crear-ticket)
- [Obtener Ticket](#obtener-ticket-específico)
- [Actualizar Ticket](#actualizar-ticket)
- [Eliminar Ticket](#eliminar-ticket)
- [Tickets Pagados](#tickets-pagados)
- [Tickets Pendientes](#tickets-pendientes)
- [Tickets Cancelados](#tickets-cancelados)
- [Tickets por Método de Pago](#tickets-por-método-de-pago)
- [Marcar como Pagado](#marcar-como-pagado)
- [Marcar como Cancelado](#marcar-como-cancelado)
- [Estadísticas de Tickets](#estadísticas-de-tickets)

---

## 🔧 **CONFIGURACIÓN DE AUTENTICACIÓN**

### **Headers Requeridos:**
```http
Content-Type: application/json
Authorization: Basic <base64_credentials>
```

### **Ejemplo con cURL:**
```bash
curl -H "Content-Type: application/json" \
     -u "admin:password" \
     http://localhost:8000/appointments/api/appointment-statuses/
```

---

## 📊 **1. APPOINTMENT STATUS ENDPOINTS**

### **Listar Estados de Citas**
```http
GET /appointments/api/appointment-statuses/
```

**Respuesta Exitosa (200):**
```json
[
    {
        "id": 1,
        "name": "Pendiente",
        "description": "Cita pendiente de confirmación",
        "is_active": true,
        "created_at": "2025-08-21T13:29:21.437480Z",
        "updated_at": "2025-08-21T13:29:21.437480Z",
        "appointments_count": 0
    }
]
```

### **Crear Estado de Cita**
```http
POST /appointments/api/appointment-statuses/
```

**Body:**
```json
{
    "name": "Confirmada",
    "description": "Cita confirmada por el paciente"
}
```

**Respuesta Exitosa (201):**
```json
{
    "id": 2,
    "name": "Confirmada",
    "description": "Cita confirmada por el paciente",
    "is_active": true,
    "created_at": "2025-08-21T13:30:00.000000Z",
    "updated_at": "2025-08-21T13:30:00.000000Z",
    "appointments_count": 0
}
```

### **Obtener Estado Específico**
```http
GET /appointments/api/appointment-statuses/{id}/
```

**Respuesta Exitosa (200):**
```json
{
    "id": 1,
    "name": "Pendiente",
    "description": "Cita pendiente de confirmación",
    "is_active": true,
    "created_at": "2025-08-21T13:29:21.437480Z",
    "updated_at": "2025-08-21T13:29:21.437480Z",
    "appointments_count": 0
}
```

### **Actualizar Estado**
```http
PUT /appointments/api/appointment-statuses/{id}/
```

**Body:**
```json
{
    "name": "Actualizada",
    "description": "Descripción actualizada"
}
```

**Respuesta Exitosa (200):**
```json
{
    "id": 1,
    "name": "Actualizada",
    "description": "Descripción actualizada",
    "is_active": true,
    "created_at": "2025-08-21T13:29:21.437480Z",
    "updated_at": "2025-08-21T13:31:00.000000Z",
    "appointments_count": 0
}
```

### **Eliminar Estado**
```http
DELETE /appointments/api/appointment-statuses/{id}/
```

**Respuesta Exitosa (204):** Sin contenido

### **Estados Activos**
```http
GET /appointments/api/appointment-statuses/active/
```

**Respuesta Exitosa (200):**
```json
[
    {
        "id": 1,
        "name": "Pendiente",
        "description": "Cita pendiente de confirmación",
        "is_active": true,
        "appointments_count": 0
    }
]
```

### **Activar Estado**
```http
POST /appointments/api/appointment-statuses/{id}/activate/
```

**Respuesta Exitosa (200):**
```json
{
    "message": "Estado activado correctamente",
    "is_active": true
}
```

### **Desactivar Estado**
```http
POST /appointments/api/appointment-statuses/{id}/deactivate/
```

**Respuesta Exitosa (200):**
```json
{
    "message": "Estado desactivado correctamente",
    "is_active": false
}
```

### **Citas por Estado**
```http
GET /appointments/api/appointment-statuses/{id}/appointments/
```

**Respuesta Exitosa (200):**
```json
[
    {
        "id": 1,
        "appointment_date": "2025-08-21",
        "appointment_hour": "14:30:00",
        "ailments": "Dolor de espalda",
        "diagnosis": "Lumbalgia",
        "appointment_type": "Consulta",
        "room": 1,
        "payment": "50.00",
        "is_completed": false,
        "is_pending": true
    }
]
```

---

## 📅 **2. APPOINTMENTS ENDPOINTS**

### **Listar Citas**
```http
GET /appointments/api/appointments/
```

**Parámetros de Filtrado:**
- `appointment_date`: Filtro por fecha
- `appointment_type`: Filtro por tipo de cita
- `room`: Filtro por sala
- `appointment_status`: Filtro por estado

**Respuesta Exitosa (200):**
```json
[
    {
        "id": 1,
        "appointment_date": "2025-08-21",
        "appointment_hour": "14:30:00",
        "ailments": "Dolor de espalda",
        "diagnosis": "Lumbalgia",
        "surgeries": null,
        "reflexology_diagnostics": null,
        "medications": null,
        "observation": null,
        "initial_date": null,
        "final_date": null,
        "appointment_type": "Consulta",
        "room": 1,
        "social_benefit": null,
        "payment_detail": null,
        "payment": "50.00",
        "ticket_number": null,
        "appointment_status": 1,
        "appointment_status_name": "Pendiente",
        "is_completed": false,
        "is_pending": true,
        "created_at": "2025-08-21T13:29:21.437480Z",
        "updated_at": "2025-08-21T13:29:21.437480Z"
    }
]
```

### **Crear Cita**
```http
POST /appointments/api/appointments/
```

**Body:**
```json
{
    "appointment_date": "2025-08-22",
    "appointment_hour": "15:00:00",
    "ailments": "Dolor de cabeza",
    "diagnosis": "Migraña",
    "appointment_type": "Consulta",
    "room": 2,
    "payment": "60.00",
    "appointment_status": 1
}
```

**Respuesta Exitosa (201):**
```json
{
    "id": 2,
    "appointment_date": "2025-08-22",
    "appointment_hour": "15:00:00",
    "ailments": "Dolor de cabeza",
    "diagnosis": "Migraña",
    "appointment_type": "Consulta",
    "room": 2,
    "payment": "60.00",
    "appointment_status": 1,
    "appointment_status_name": "Pendiente",
    "is_completed": false,
    "is_pending": true
}
```

### **Obtener Cita Específica**
```http
GET /appointments/api/appointments/{id}/
```

**Respuesta Exitosa (200):**
```json
{
    "id": 1,
    "appointment_date": "2025-08-21",
    "appointment_hour": "14:30:00",
    "ailments": "Dolor de espalda",
    "diagnosis": "Lumbalgia",
    "appointment_type": "Consulta",
    "room": 1,
    "payment": "50.00",
    "appointment_status": 1,
    "appointment_status_name": "Pendiente",
    "is_completed": false,
    "is_pending": true
}
```

### **Actualizar Cita**
```http
PUT /appointments/api/appointments/{id}/
```

**Body:**
```json
{
    "appointment_date": "2025-08-23",
    "appointment_hour": "16:00:00",
    "ailments": "Dolor de espalda crónico",
    "diagnosis": "Lumbalgia severa",
    "appointment_type": "Terapia",
    "room": 3,
    "payment": "80.00",
    "appointment_status": 2
}
```

### **Eliminar Cita**
```http
DELETE /appointments/api/appointments/{id}/
```

**Respuesta Exitosa (204):** Sin contenido

### **Citas Completadas**
```http
GET /appointments/api/appointments/completed/
```

**Respuesta Exitosa (200):**
```json
[
    {
        "id": 3,
        "appointment_date": "2025-08-20",
        "appointment_hour": "10:00:00",
        "ailments": "Dolor de rodilla",
        "diagnosis": "Artritis",
        "appointment_type": "Terapia",
        "room": 1,
        "payment": "70.00",
        "appointment_status": 3,
        "appointment_status_name": "Completada",
        "is_completed": true,
        "is_pending": false
    }
]
```

### **Citas Pendientes**
```http
GET /appointments/api/appointments/pending/
```

**Respuesta Exitosa (200):**
```json
[
    {
        "id": 1,
        "appointment_date": "2025-08-21",
        "appointment_hour": "14:30:00",
        "ailments": "Dolor de espalda",
        "diagnosis": "Lumbalgia",
        "appointment_type": "Consulta",
        "room": 1,
        "payment": "50.00",
        "appointment_status": 1,
        "appointment_status_name": "Pendiente",
        "is_completed": false,
        "is_pending": true
    }
]
```

### **Citas por Rango de Fecha**
```http
GET /appointments/api/appointments/by_date_range/
```

**Parámetros:**
- `start_date`: Fecha de inicio (YYYY-MM-DD)
- `end_date`: Fecha de fin (YYYY-MM-DD)

**Ejemplo:**
```http
GET /appointments/api/appointments/by_date_range/?start_date=2025-08-20&end_date=2025-08-25
```

### **Cancelar Cita**
```http
POST /appointments/api/appointments/{id}/cancel/
```

**Respuesta Exitosa (200):**
```json
{
    "message": "Cita cancelada correctamente",
    "appointment_status": "Cancelada"
}
```

### **Reprogramar Cita**
```http
POST /appointments/api/appointments/{id}/reschedule/
```

**Body:**
```json
{
    "appointment_date": "2025-08-24",
    "appointment_hour": "17:00:00"
}
```

**Respuesta Exitosa (200):**
```json
{
    "message": "Cita reprogramada correctamente",
    "new_date": "2025-08-24",
    "new_hour": "17:00:00"
}
```

---

## 🎫 **3. TICKETS ENDPOINTS**

### **Listar Tickets**
```http
GET /appointments/api/tickets/
```

**Parámetros de Filtrado:**
- `payment_method`: Filtro por método de pago
- `status`: Filtro por estado del ticket
- `payment_date`: Filtro por fecha de pago

**Respuesta Exitosa (200):**
```json
[
    {
        "id": 1,
        "ticket_number": "T001",
        "payment_date": "2025-08-21T13:29:21.437480Z",
        "amount": "50.00",
        "payment_method": "Efectivo",
        "description": "Pago por consulta",
        "status": "Pendiente",
        "is_paid": false,
        "is_pending": true,
        "created_at": "2025-08-21T13:29:21.437480Z",
        "updated_at": "2025-08-21T13:29:21.437480Z"
    }
]
```

### **Crear Ticket**
```http
POST /appointments/api/tickets/
```

**Body:**
```json
{
    "ticket_number": "T002",
    "amount": "60.00",
    "payment_method": "Tarjeta",
    "description": "Pago por terapia",
    "status": "Pendiente"
}
```

**Respuesta Exitosa (201):**
```json
{
    "id": 2,
    "ticket_number": "T002",
    "payment_date": "2025-08-21T13:35:00.000000Z",
    "amount": "60.00",
    "payment_method": "Tarjeta",
    "description": "Pago por terapia",
    "status": "Pendiente",
    "is_paid": false,
    "is_pending": true
}
```

### **Obtener Ticket Específico**
```http
GET /appointments/api/tickets/{id}/
```

**Respuesta Exitosa (200):**
```json
{
    "id": 1,
    "ticket_number": "T001",
    "payment_date": "2025-08-21T13:29:21.437480Z",
    "amount": "50.00",
    "payment_method": "Efectivo",
    "description": "Pago por consulta",
    "status": "Pendiente",
    "is_paid": false,
    "is_pending": true
}
```

### **Actualizar Ticket**
```http
PUT /appointments/api/tickets/{id}/
```

**Body:**
```json
{
    "amount": "55.00",
    "payment_method": "Transferencia",
    "description": "Pago por consulta actualizado",
    "status": "Pagado"
}
```

### **Eliminar Ticket**
```http
DELETE /appointments/api/tickets/{id}/
```

**Respuesta Exitosa (204):** Sin contenido

### **Tickets Pagados**
```http
GET /appointments/api/tickets/paid/
```

**Respuesta Exitosa (200):**
```json
[
    {
        "id": 2,
        "ticket_number": "T002",
        "payment_date": "2025-08-21T13:35:00.000000Z",
        "amount": "60.00",
        "payment_method": "Tarjeta",
        "description": "Pago por terapia",
        "status": "Pagado",
        "is_paid": true,
        "is_pending": false
    }
]
```

### **Tickets Pendientes**
```http
GET /appointments/api/tickets/pending/
```

**Respuesta Exitosa (200):**
```json
[
    {
        "id": 1,
        "ticket_number": "T001",
        "payment_date": "2025-08-21T13:29:21.437480Z",
        "amount": "50.00",
        "payment_method": "Efectivo",
        "description": "Pago por consulta",
        "status": "Pendiente",
        "is_paid": false,
        "is_pending": true
    }
]
```

### **Tickets Cancelados**
```http
GET /appointments/api/tickets/cancelled/
```

**Respuesta Exitosa (200):**
```json
[
    {
        "id": 3,
        "ticket_number": "T003",
        "payment_date": "2025-08-21T13:40:00.000000Z",
        "amount": "40.00",
        "payment_method": "Efectivo",
        "description": "Pago cancelado",
        "status": "Cancelado",
        "is_paid": false,
        "is_pending": false
    }
]
```

### **Tickets por Método de Pago**
```http
GET /appointments/api/tickets/by_payment_method/
```

**Parámetros:**
- `payment_method`: Método de pago específico

**Ejemplo:**
```http
GET /appointments/api/tickets/by_payment_method/?payment_method=Efectivo
```

### **Marcar como Pagado**
```http
POST /appointments/api/tickets/{id}/mark_as_paid/
```

**Respuesta Exitosa (200):**
```json
{
    "message": "Ticket marcado como pagado",
    "status": "Pagado",
    "is_paid": true
}
```

### **Marcar como Cancelado**
```http
POST /appointments/api/tickets/{id}/mark_as_cancelled/
```

**Respuesta Exitosa (200):**
```json
{
    "message": "Ticket marcado como cancelado",
    "status": "Cancelado",
    "is_paid": false
}
```

### **Estadísticas de Tickets**
```http
GET /appointments/api/tickets/statistics/
```

**Respuesta Exitosa (200):**
```json
{
    "total_tickets": 10,
    "paid_tickets": 6,
    "pending_tickets": 3,
    "cancelled_tickets": 1,
    "total_amount": "550.00",
    "paid_amount": "330.00",
    "pending_amount": "180.00",
    "cancelled_amount": "40.00",
    "payment_methods": {
        "Efectivo": 4,
        "Tarjeta": 3,
        "Transferencia": 3
    }
}
```

---

## 🔍 **FILTROS Y BÚSQUEDA**

### **Filtros Disponibles:**
- `search`: Búsqueda en campos de texto
- `ordering`: Ordenamiento por campos específicos
- `page`: Paginación
- `page_size`: Tamaño de página

### **Ejemplos de Uso:**

**Búsqueda:**
```http
GET /appointments/api/appointments/?search=dolor
```

**Ordenamiento:**
```http
GET /appointments/api/appointments/?ordering=-appointment_date
```

**Paginación:**
```http
GET /appointments/api/appointments/?page=2&page_size=10
```

**Filtros Combinados:**
```http
GET /appointments/api/appointments/?appointment_type=Consulta&room=1&ordering=appointment_date
```

---

## ⚠️ **CÓDIGOS DE ERROR COMUNES**

### **400 - Bad Request**
```json
{
    "error": "Datos de entrada inválidos",
    "details": {
        "appointment_date": ["Este campo es requerido."],
        "payment": ["Debe ser un número válido."]
    }
}
```

### **401 - Unauthorized**
```json
{
    "detail": "Las credenciales de autenticación no fueron proporcionadas."
}
```

### **403 - Forbidden**
```json
{
    "detail": "No tiene permisos para realizar esta acción."
}
```

### **404 - Not Found**
```json
{
    "detail": "No encontrado."
}
```

### **500 - Internal Server Error**
```json
{
    "error": "Error interno del servidor",
    "message": "Ha ocurrido un error inesperado"
}
```

---

## 📝 **NOTAS IMPORTANTES**

### **Validaciones:**
- Las fechas deben estar en formato `YYYY-MM-DD`
- Las horas deben estar en formato `HH:MM:SS`
- Los montos deben ser números decimales positivos
- Los nombres de estados deben ser únicos

### **Limitaciones Actuales:**
- Las dependencias externas (Patient, Therapist, PaymentType) están marcadas como TODO
- Algunas funcionalidades avanzadas requieren las dependencias completas
- Los tests de vistas requieren configuración de autenticación

### **Recomendaciones:**
- Usar siempre autenticación en las peticiones
- Validar los datos antes de enviarlos
- Manejar los errores apropiadamente
- Usar paginación para listas grandes

---

## 🚀 **EJEMPLOS DE USO COMPLETOS**

### **Crear una Cita Completa:**
```bash
curl -X POST \
  http://localhost:8000/appointments/api/appointments/ \
  -H "Content-Type: application/json" \
  -u "admin:password" \
  -d '{
    "appointment_date": "2025-08-25",
    "appointment_hour": "10:00:00",
    "ailments": "Dolor de espalda",
    "diagnosis": "Lumbalgia",
    "appointment_type": "Terapia",
    "room": 1,
    "payment": "80.00",
    "appointment_status": 1
  }'
```

### **Obtener Estadísticas:**
```bash
curl -X GET \
  http://localhost:8000/appointments/api/tickets/statistics/ \
  -H "Content-Type: application/json" \
  -u "admin:password"
```

### **Filtrar Citas por Fecha:**
```bash
curl -X GET \
  "http://localhost:8000/appointments/api/appointments/?appointment_date=2025-08-21" \
  -H "Content-Type: application/json" \
  -u "admin:password"
```

---

**📅 Última actualización:** 21 de Agosto, 2025  
**🔄 Versión:** 1.0  
**📋 Estado:** Activo y Funcional
