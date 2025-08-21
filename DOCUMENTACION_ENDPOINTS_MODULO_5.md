# 📚 DOCUMENTACIÓN DE ENDPOINTS - MÓDULO 5 (APPOINTMENTS_STATUS) - INTEGRACIÓN COMPLETA

## 🎯 **INFORMACIÓN GENERAL**

**Base URL:** `http://localhost:8000/appointments/`  
**Autenticación:** Requerida (Session/Basic Authentication)  
**Formato:** JSON  
**Namespace:** `appointments_status`  
**Estado:** ✅ **INTEGRACIÓN COMPLETA CON TODOS LOS MÓDULOS**

### **🔗 Módulos Integrados:**
- ✅ **Módulo 3:** `patients_diagnoses` - Pacientes y Diagnósticos
- ✅ **Módulo 4:** `therapists` - Terapeutas y Ubicaciones
- ✅ **Módulo 6:** `histories_configurations` - Tipos de Pago
- ✅ **Módulo 5:** `appointments_status` - Citas y Tickets

---

## 📋 **ÍNDICE DE ENDPOINTS**

### **1. APPOINTMENT STATUS (Estados de Citas)** ✅
- [Listar Estados](#listar-estados-de-citas)
- [Crear Estado](#crear-estado-de-cita)
- [Obtener Estado](#obtener-estado-específico)
- [Actualizar Estado](#actualizar-estado)
- [Eliminar Estado](#eliminar-estado)

### **2. APPOINTMENTS (Citas)** ✅ **INTEGRADO COMPLETAMENTE**
- [Listar Citas](#listar-citas)
- [Crear Cita](#crear-cita)
- [Obtener Cita](#obtener-cita-específica)
- [Actualizar Cita](#actualizar-cita)
- [Eliminar Cita](#eliminar-cita)
- [Citas por Paciente](#citas-por-paciente)
- [Citas por Terapeuta](#citas-por-terapeuta)
- [Citas por Tipo de Pago](#citas-por-tipo-de-pago)

### **3. TICKETS (Tickets)** ✅ **INTEGRADO COMPLETAMENTE**
- [Listar Tickets](#listar-tickets)
- [Crear Ticket](#crear-ticket)
- [Obtener Ticket](#obtener-ticket-específico)
- [Actualizar Ticket](#actualizar-ticket)
- [Eliminar Ticket](#eliminar-ticket)
- [Tickets por Cita](#tickets-por-cita)

### **4. DEPENDENCIAS INTEGRADAS** 🔗
- [Pacientes (Módulo 3)](#pacientes-módulo-3)
- [Terapeutas (Módulo 4)](#terapeutas-módulo-4)
- [Tipos de Pago (Módulo 6)](#tipos-de-pago-módulo-6)
- [Ubicaciones (Módulo 4)](#ubicaciones-módulo-4)

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
     http://localhost:8000/appointments/appointment-statuses/
```

---

## 📊 **1. APPOINTMENT STATUS ENDPOINTS**

### **Listar Estados de Citas**
```http
GET /appointments/appointment-statuses/
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
POST /appointments/appointment-statuses/
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
GET /appointments/appointment-statuses/{id}/
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
PUT /appointments/appointment-statuses/{id}/
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
DELETE /appointments/appointment-statuses/{id}/
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
GET /appointments/appointments/
```

**Parámetros de Filtrado:**
- `appointment_date`: Filtro por fecha
- `appointment_type`: Filtro por tipo de cita
- `room`: Filtro por sala
- `appointment_status`: Filtro por estado
- `patient`: Filtro por paciente (ID)
- `therapist`: Filtro por terapeuta (ID)
- `payment_type`: Filtro por tipo de pago (ID)

**Respuesta Exitosa (200):**
```json
[
    {
        "id": 1,
        "patient": 1,
        "patient_name": "María González López",
        "therapist": 1,
        "therapist_name": "Juan Pérez García",
        "appointment_date": "2025-08-25",
        "appointment_hour": "10:00:00",
        "ailments": "Dolor de espalda",
        "diagnosis": "Lumbalgia",
        "surgeries": null,
        "reflexology_diagnostics": null,
        "medications": null,
        "observation": null,
        "initial_date": null,
        "final_date": null,
        "appointment_type": "Consulta",
        "room": "1",
        "social_benefit": null,
        "payment_detail": null,
        "payment": "50.00",
        "payment_type": 1,
        "payment_type_name": "Efectivo",
        "ticket_number": null,
        "appointment_status": 1,
        "appointment_status_name": "Pendiente",
        "is_completed": false,
        "is_pending": true,
        "created_at": "2025-08-21T13:29:21.437480Z",
        "updated_at": "2025-08-21T13:29:21.437480Z",
        "is_active": true
    }
]
```

### **Crear Cita**
```http
POST /appointments/appointments/
```

**Body:**
```json
{
    "patient": 1,
    "therapist": 1,
    "appointment_date": "2025-08-25",
    "appointment_hour": "15:00:00",
    "ailments": "Dolor de cabeza",
    "diagnosis": "Migraña",
    "appointment_type": "Consulta",
    "room": "2",
    "payment": "60.00",
    "payment_type": 1,
    "appointment_status": 1
}
```

**Respuesta Exitosa (201):**
```json
{
    "id": 2,
    "patient": 1,
    "patient_name": "María González López",
    "therapist": 1,
    "therapist_name": "Juan Pérez García",
    "appointment_date": "2025-08-25",
    "appointment_hour": "15:00:00",
    "ailments": "Dolor de cabeza",
    "diagnosis": "Migraña",
    "appointment_type": "Consulta",
    "room": "2",
    "payment": "60.00",
    "payment_type": 1,
    "payment_type_name": "Efectivo",
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

### **Obtener Cita Específica**
```http
GET /appointments/appointments/{id}/
```

**Respuesta Exitosa (200):**
```json
{
    "id": 1,
    "patient": 1,
    "patient_name": "María González López",
    "therapist": 1,
    "therapist_name": "Juan Pérez García",
    "appointment_date": "2025-08-25",
    "appointment_hour": "10:00:00",
    "ailments": "Dolor de espalda",
    "diagnosis": "Lumbalgia",
    "appointment_type": "Consulta",
    "room": "1",
    "payment": "50.00",
    "payment_type": 1,
    "payment_type_name": "Efectivo",
    "appointment_status": 1,
    "appointment_status_name": "Pendiente",
    "is_completed": false,
    "is_pending": true
}
```

### **Actualizar Cita**
```http
PUT /appointments/appointments/{id}/
```

**Body:**
```json
{
    "patient": 1,
    "therapist": 1,
    "appointment_date": "2025-08-26",
    "appointment_hour": "16:00:00",
    "ailments": "Dolor de espalda crónico",
    "diagnosis": "Lumbalgia severa",
    "appointment_type": "Terapia",
    "room": "3",
    "payment": "80.00",
    "payment_type": 2,
    "appointment_status": 2
}
```

### **Eliminar Cita**
```http
DELETE /appointments/appointments/{id}/
```

**Respuesta Exitosa (204):** Sin contenido

### **Citas por Paciente**
```http
GET /appointments/appointments/?patient={patient_id}
```

**Ejemplo:**
```http
GET /appointments/appointments/?patient=1
```

### **Citas por Terapeuta**
```http
GET /appointments/appointments/?therapist={therapist_id}
```

**Ejemplo:**
```http
GET /appointments/appointments/?therapist=1
```

### **Citas por Tipo de Pago**
```http
GET /appointments/appointments/?payment_type={payment_type_id}
```

**Ejemplo:**
```http
GET /appointments/appointments/?payment_type=1
```

---

## 🎫 **3. TICKETS ENDPOINTS**

### **Listar Tickets**
```http
GET /appointments/tickets/
```

**Parámetros de Filtrado:**
- `payment_method`: Filtro por método de pago
- `status`: Filtro por estado del ticket
- `payment_date`: Filtro por fecha de pago
- `appointment`: Filtro por cita (ID)

**Respuesta Exitosa (200):**
```json
[
    {
        "id": 1,
        "appointment": 1,
        "appointment_details": "Cita 1 - 2025-08-25 10:00:00",
        "ticket_number": "T001",
        "payment_date": "2025-08-21T13:29:21.437480Z",
        "amount": "50.00",
        "payment_method": "efectivo",
        "description": "Pago por consulta",
        "status": "pending",
        "is_paid": false,
        "is_pending": true,
        "created_at": "2025-08-21T13:29:21.437480Z",
        "updated_at": "2025-08-21T13:29:21.437480Z",
        "is_active": true
    }
]
```

### **Crear Ticket**
```http
POST /appointments/tickets/
```

**Body:**
```json
{
    "appointment": 1,
    "ticket_number": "T002",
    "amount": "60.00",
    "payment_method": "tarjeta",
    "description": "Pago por terapia",
    "status": "pending"
}
```

**Respuesta Exitosa (201):**
```json
{
    "id": 2,
    "appointment": 1,
    "appointment_details": "Cita 1 - 2025-08-25 10:00:00",
    "ticket_number": "T002",
    "payment_date": "2025-08-21T13:35:00.000000Z",
    "amount": "60.00",
    "payment_method": "tarjeta",
    "description": "Pago por terapia",
    "status": "pending",
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

### **Obtener Ticket Específico**
```http
GET /appointments/tickets/{id}/
```

**Respuesta Exitosa (200):**
```json
{
    "id": 1,
    "appointment": 1,
    "appointment_details": "Cita 1 - 2025-08-25 10:00:00",
    "ticket_number": "T001",
    "payment_date": "2025-08-21T13:29:21.437480Z",
    "amount": "50.00",
    "payment_method": "efectivo",
    "description": "Pago por consulta",
    "status": "pending",
    "is_paid": false,
    "is_pending": true
}
```

### **Actualizar Ticket**
```http
PUT /appointments/tickets/{id}/
```

**Body:**
```json
{
    "appointment": 1,
    "amount": "55.00",
    "payment_method": "transferencia",
    "description": "Pago por consulta actualizado",
    "status": "paid"
}
```

### **Eliminar Ticket**
```http
DELETE /appointments/tickets/{id}/
```

**Respuesta Exitosa (204):** Sin contenido

### **Tickets por Cita**
```http
GET /appointments/tickets/?appointment={appointment_id}
```

**Ejemplo:**
```http
GET /appointments/tickets/?appointment=1
```

---

## 🔗 **4. DEPENDENCIAS INTEGRADAS**

### **Pacientes (Módulo 3)**
```http
GET /patients/patients/
POST /patients/patients/
GET /patients/patients/{id}/
PUT /patients/patients/{id}/
DELETE /patients/patients/{id}/
```

### **Terapeutas (Módulo 4)**
```http
GET /therapists/therapists/
POST /therapists/therapists/
GET /therapists/therapists/{id}/
PUT /therapists/therapists/{id}/
DELETE /therapists/therapists/{id}/
```

### **Tipos de Pago (Módulo 6)**
```http
GET /configurations/payment-types/
POST /configurations/payment-types/
GET /configurations/payment-types/{id}/
PUT /configurations/payment-types/{id}/
DELETE /configurations/payment-types/{id}/
```

### **Ubicaciones (Módulo 4)**
```http
GET /therapists/regions/
GET /therapists/provinces/
GET /therapists/districts/
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

### **Integración Completa:**
- ✅ **Todas las dependencias externas están integradas y funcionando**
- ✅ **Patient, Therapist, PaymentType completamente vinculados**
- ✅ **Relaciones bidireccionales establecidas**
- ✅ **Validaciones cruzadas implementadas**

### **Recomendaciones:**
- Usar siempre autenticación en las peticiones
- Validar los datos antes de enviarlos
- Manejar los errores apropiadamente
- Usar paginación para listas grandes

---

## 🚀 **EJEMPLOS DE USO COMPLETOS**

### **Crear una Cita Completa Integrada:**
```bash
curl -X POST \
  http://localhost:8000/appointments/appointments/ \
  -H "Content-Type: application/json" \
  -u "admin:password" \
  -d '{
    "patient": 1,
    "therapist": 1,
    "appointment_date": "2025-08-25",
    "appointment_hour": "10:00:00",
    "ailments": "Dolor de espalda",
    "diagnosis": "Lumbalgia",
    "appointment_type": "Terapia",
    "room": "1",
    "payment": "80.00",
    "payment_type": 1,
    "appointment_status": 1
  }'
```

### **Crear un Ticket para una Cita:**
```bash
curl -X POST \
  http://localhost:8000/appointments/tickets/ \
  -H "Content-Type: application/json" \
  -u "admin:password" \
  -d '{
    "appointment": 1,
    "ticket_number": "T001",
    "amount": "80.00",
    "payment_method": "efectivo",
    "description": "Pago por terapia de reflexología",
    "status": "pending"
  }'
```

### **Filtrar Citas por Paciente:**
```bash
curl -X GET \
  "http://localhost:8000/appointments/appointments/?patient=1" \
  -H "Content-Type: application/json" \
  -u "admin:password"
```

### **Filtrar Citas por Terapeuta:**
```bash
curl -X GET \
  "http://localhost:8000/appointments/appointments/?therapist=1" \
  -H "Content-Type: application/json" \
  -u "admin:password"
```

### **Obtener Tickets de una Cita:**
```bash
curl -X GET \
  "http://localhost:8000/appointments/tickets/?appointment=1" \
  -H "Content-Type: application/json" \
  -u "admin:password"
```

---

**📅 Última actualización:** 21 de Agosto, 2025  
**🔄 Versión:** 2.0 - Integración Completa  
**📋 Estado:** ✅ Activo, Funcional e Integrado  
**🔗 Módulos Integrados:** 6/6 (100%)
