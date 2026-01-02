# Task Manager - Documentación del Proyecto

##  Índice
1. [Visión del Proyecto](#visión-del-proyecto)
2. [Problemas que Resuelve](#problemas-que-resuelve)
3. [Tipos de Items](#tipos-de-items)
4. [Características Principales](#características-principales)
5. [Vistas de la Aplicación](#vistas-de-la-aplicación)
6. [Diseño de Base de Datos](#diseño-de-base-de-datos)
7. [Flujos de Usuario](#flujos-de-usuario-principales)
8. [Roadmap](#roadmap)

---

##  Visión del Proyecto

Un task manager profesional que elimina la ambigüedad entre tareas y eventos, proporcionando claridad en las fechas (vencimiento vs realización) y un sistema de clasificación eficiente mediante inbox, listas y tipos.

**Usuario objetivo:** Profesionales y estudiantes que necesitan gestionar tanto tareas recurrentes como eventos puntuales con claridad temporal.

---

## Problemas que Resuelve

1. **Ambigüedad en fechas**: Diferencia clara entre "cuándo vence" y "cuándo debo hacerla"
2. **Visualización por contexto**: Tableros que muestran items según su tipo (inbox, tareas, eventos)
3. **Sistema de clasificación mejorado**: Tipos + Listas + Prioridad (opcional)
4. **Gestión de inbox**: Items sin clasificar que esperan ser procesados

---

## Tipos de Items

### 1. Inbox (Por Defecto)
- **Propósito**: Items recién creados que necesitan ser clasificados
- **Característica especial**: Se priorizan por antigüedad (mientras más tiempo sin clasificar, más arriba aparecen)
- **Campos**:
  - Título
  - Descripción (opcional)

### 2. Tarea
Items con fecha límite y fecha objetivo de realización.

**Campos obligatorios:**
- Título
- Fecha de vencimiento
- Fecha de realización

**Campos opcionales:**
- Descripción
- Subtareas (máximo 2 niveles)
- Prioridad (Alta, Media, Baja)
- Estado (Pendiente, En progreso, Completada, Cancelada)
- Adjuntos
- Lista asignada

**Comportamiento:**
- Contador regresivo hasta fecha de vencimiento
- Recordatorio en fecha de realización
- Aparece en vista "Hoy" si fecha de realización = hoy

### 3. Evento
Items con fecha y hora específica.

**Campos obligatorios:**
- Título
- Fecha

**Campos opcionales:**
- Descripción
- Subeventos (máximo 2 niveles)
- Prioridad
- Estado
- Adjuntos
- Lista asignada

**Comportamiento:**
- Aparece en calendario
- No tiene fecha de vencimiento separada

---

## Características Principales

### Sistema de Listas
- Funcionan como proyectos/categorías
- Cada lista puede contener tareas y eventos
- Un item puede pertenecer a una lista
- Ejemplos: "Trabajo", "Personal", "Universidad"

### Subtareas/Subeventos
- Máximo 2 niveles de profundidad:
  - Tarea → Subtarea → Sub-subtarea ❌ (NO permitido)
  - Tarea → Subtarea ✅
- Heredan el tipo del padre (subtarea de tarea = tarea)
- Tienen los mismos campos que el padre

### Campos Opcionales Activables
Los siguientes campos solo se muestran si el usuario los agrega:
- Prioridad (Alta, Media, Baja)
- Estado (Pendiente, En progreso, Completada, Cancelada)
- Adjuntos

---

## Vistas de la Aplicación

### Autenticación
- **Login**: Inicio de sesión
- **Register**: Registro de nuevos usuarios

### Vistas Principales

#### 1. Wait List (Inbox)
- Muestra todos los items tipo "Inbox"
- Ordenados por antigüedad (más antiguos primero)
- Permite reclasificar como Tarea o Evento

#### 2. Dashboard
- Vista general de todas las tareas y eventos
- Filtros por tipo, lista, prioridad
- Resumen de tareas próximas a vencer

#### 3. Scrum Dashboard
- Vista tipo Kanban
- Columnas por estado (Pendiente, En progreso, Completada)
- Solo muestra tareas (no eventos)

#### 4. Calendar
- Vista mensual/semanal/diaria
- Muestra principalmente eventos
- Puede mostrar tareas con fecha de realización

#### 5. Vista de Hoy
- Tareas con fecha de realización = hoy
- Eventos programados para hoy
- Priorización automática

#### 6. Vista Semanal
- Tareas y eventos de los próximos 7 días
- Agrupados por día

#### 7. Settings
- Configuración de cuenta
- Preferencias de la aplicación
- Gestión de listas

---

## Diseño de Base de Datos

Se presentan dos versiones del diseño de base de datos: una versión simplificada para MVP y una versión avanzada (2.0) con mayor flexibilidad.

---

### Versión MVP - Diseño Simplificado (Recomendado para Inicio)

Este diseño prioriza simplicidad y velocidad de desarrollo, manteniendo todas las funcionalidades core del proyecto.

#### Tablas Principales

```sql
-- Usuarios
users
├── id (PK)
├── email (UNIQUE)
├── password_hash
├── name
├── created_at
└── updated_at

-- Tipos de Items (Tabla)
item_types
├── id (PK)
├── name VARCHAR(50) -- inbox, task, event
├── slug VARCHAR(50) (UNIQUE) -- para consultas programáticas
└── is_system BOOLEAN -- tipos predefinidos del sistema

-- Prioridades (Tabla)
priorities
├── id (PK)
├── name VARCHAR(50) -- Alta, Media, Baja
├── order_index INTEGER -- para ordenar
└── color VARCHAR(7) -- hex color

-- Estados (Tabla)
statuses
├── id (PK)
├── name VARCHAR(50) -- Pendiente, En progreso, Completada, Cancelada
├── order_index INTEGER -- para ordenar
└── color VARCHAR(7) -- hex color

-- Items (tareas, eventos, inbox)
items
├── id (PK)
├── user_id (FK → users)
├── type_id (FK → item_types)
├── title VARCHAR(200)
├── description TEXT
├── due_date TIMESTAMP (solo para tasks)
├── realization_date TIMESTAMP (solo para tasks)
├── event_date TIMESTAMP (solo para events)
├── location VARCHAR(200) (opcional, común en events)
├── priority_id (FK → priorities, NULL)
├── status_id (FK → statuses, NULL)
├── list_id (FK → lists, NULL)
├── parent_id (FK → items, NULL) -- Para subtareas
├── position INTEGER -- orden manual en listas
├── completed_at TIMESTAMP
├── deleted_at TIMESTAMP -- soft delete
├── created_at TIMESTAMP
└── updated_at TIMESTAMP

-- Listas/Proyectos
lists
├── id (PK)
├── user_id (FK → users)
├── name VARCHAR(100)
├── color VARCHAR(7) -- hex color
├── parent_id (FK → lists, NULL) -- listas jerárquicas
├── created_at TIMESTAMP
└── updated_at TIMESTAMP

-- Adjuntos
attachments
├── id (PK)
├── item_id (FK → items)
├── file_name VARCHAR(255)
├── file_url VARCHAR(500)
├── file_size INTEGER
└── uploaded_at TIMESTAMP
```

#### Relaciones MVP
- Un usuario tiene muchas listas (1:N)
- Un usuario tiene muchos items (1:N)
- Una lista puede tener sublistas (1:N)
- Una lista tiene muchos items (1:N)
- Un item tiene un tipo (N:1)
- Un item puede tener una prioridad (N:1, opcional)
- Un item puede tener un estado (N:1, opcional)
- Un item puede tener muchos adjuntos (1:N)
- Un item puede tener un padre (subtarea) (1:1 opcional, máx 2 niveles)

#### Datos de Seed Necesarios (MVP)
```sql
-- Tipos del sistema (siempre presentes)
INSERT INTO item_types (name, slug, is_system) VALUES 
  ('Inbox', 'inbox', true),
  ('Tarea', 'task', true),
  ('Evento', 'event', true);

-- Prioridades predefinidas
INSERT INTO priorities (name, order_index, color) VALUES 
  ('Alta', 1, '#EF4444'),
  ('Media', 2, '#F59E0B'),
  ('Baja', 3, '#10B981');

-- Estados predefinidos
INSERT INTO statuses (name, order_index, color) VALUES 
  ('Pendiente', 1, '#6B7280'),
  ('En progreso', 2, '#3B82F6'),
  ('Completada', 3, '#10B981'),
  ('Cancelada', 4, '#EF4444');
```

#### Índices Recomendados MVP
```sql
CREATE INDEX idx_items_user_id ON items(user_id);
CREATE INDEX idx_items_type_id ON items(type_id);
CREATE INDEX idx_items_list_id ON items(list_id);
CREATE INDEX idx_items_parent_id ON items(parent_id);
CREATE INDEX idx_items_priority_id ON items(priority_id);
CREATE INDEX idx_items_status_id ON items(status_id);
CREATE INDEX idx_items_realization_date ON items(realization_date);
CREATE INDEX idx_items_due_date ON items(due_date);
CREATE INDEX idx_items_event_date ON items(event_date);
CREATE INDEX idx_items_deleted_at ON items(deleted_at);
CREATE INDEX idx_items_created_at ON items(created_at);
CREATE INDEX idx_lists_user_id ON lists(user_id);
CREATE INDEX idx_lists_parent_id ON lists(parent_id);
CREATE INDEX idx_attachments_item_id ON attachments(item_id);
CREATE INDEX idx_item_types_slug ON item_types(slug);
```

---

### Versión 2.0 - Diseño Avanzado (Sistema EAV Flexible)

Este diseño utiliza el patrón Entity-Attribute-Value (EAV) para máxima flexibilidad, permitiendo tipos de items personalizables y campos dinámicos.

#### Tablas Principales v2.0

```sql
-- Usuarios
users
├── id (PK)
├── email (UNIQUE)
├── password_hash
├── name
├── created_at
└── updated_at

-- Tipos de Items (personalizables por usuario)
item_types
├── id (PK)
├── user_id (FK → users, NULL para tipos del sistema)
├── name VARCHAR(50) -- Task, Event, Note, Meeting, etc.
├── icon VARCHAR(50)
├── color VARCHAR(7)
├── is_system BOOLEAN -- true para Inbox, Task, Event
├── created_at TIMESTAMP
└── updated_at TIMESTAMP

-- Items base
items
├── id (PK)
├── user_id (FK → users)
├── type_id (FK → item_types)
├── list_id (FK → lists, NULL)
├── title VARCHAR(200)
├── description TEXT
├── status_id (FK → statuses, NULL)
├── priority_id (FK → priorities, NULL)
├── parent_id (FK → items, NULL)
├── position INTEGER
├── completed_at TIMESTAMP
├── deleted_at TIMESTAMP
├── created_at TIMESTAMP
└── updated_at TIMESTAMP

-- Listas jerárquicas
lists
├── id (PK)
├── user_id (FK → users)
├── name VARCHAR(100)
├── color VARCHAR(7)
├── parent_id (FK → lists, NULL)
├── created_at TIMESTAMP
└── updated_at TIMESTAMP

-- Prioridades (configurables)
priorities
├── id (PK)
├── name VARCHAR(50) -- Alta, Media, Baja
├── order_index INTEGER
└── color VARCHAR(7)

-- Estados (configurables)
statuses
├── id (PK)
├── name VARCHAR(50) -- Pendiente, En progreso, etc.
├── order_index INTEGER
└── color VARCHAR(7)

-- Definición de campos dinámicos
fields
├── id (PK)
├── type_id (FK → item_types)
├── name VARCHAR(50) -- due_date, event_date, location, url, etc.
├── field_type VARCHAR(20) -- text, date, datetime, number, boolean, url
├── is_required BOOLEAN
├── created_at TIMESTAMP
└── updated_at TIMESTAMP

-- Valores de campos dinámicos (EAV)
field_values
├── id (PK)
├── item_id (FK → items)
├── field_id (FK → fields)
└── value TEXT -- almacena cualquier tipo como texto

-- Sistema de etiquetas
tags
├── id (PK)
├── user_id (FK → users)
├── name VARCHAR(50)
├── color VARCHAR(7)
└── created_at TIMESTAMP

-- Relación items-tags (muchos a muchos)
item_tags
├── item_id (FK → items)
├── tag_id (FK → tags)
└── PRIMARY KEY (item_id, tag_id)

-- Adjuntos
attachments
├── id (PK)
├── item_id (FK → items)
├── file_name VARCHAR(255)
├── file_url VARCHAR(500)
├── file_size INTEGER
└── uploaded_at TIMESTAMP
```

#### Relaciones v2.0
- Un usuario puede crear tipos de items personalizados (1:N)
- Un tipo de item tiene campos definidos (1:N)
- Un item tiene valores para sus campos (1:N)
- Un item puede tener múltiples tags (N:M)
- Todas las relaciones de MVP se mantienen

#### Índices Recomendados v2.0
```sql
-- Índices de MVP +
CREATE INDEX idx_items_type_id ON items(type_id);
CREATE INDEX idx_items_status_id ON items(status_id);
CREATE INDEX idx_items_priority_id ON items(priority_id);
CREATE INDEX idx_item_types_user_id ON item_types(user_id);
CREATE INDEX idx_item_types_is_system ON item_types(is_system);
CREATE INDEX idx_fields_type_id ON fields(type_id);
CREATE INDEX idx_field_values_item_id ON field_values(item_id);
CREATE INDEX idx_field_values_field_id ON field_values(field_id);
CREATE INDEX idx_tags_user_id ON tags(user_id);
CREATE INDEX idx_item_tags_item_id ON item_tags(item_id);
CREATE INDEX idx_item_tags_tag_id ON item_tags(tag_id);
```

---

### Recomendación de Implementación

**Para MVP (primeros 1-3 meses):** 
- Usar Versión Simplificada
- Permite lanzar rápido y validar el concepto
- Todas las features core funcionan perfectamente

**Para v2.0 (después de tener usuarios):**
- Migrar a diseño avanzado
- Implementar cuando el producto esté validado
- Añadir flexibilidad basada en feedback real



## Flujos de Usuario Principales

### Crear un Item Nuevo
1. Usuario hace clic en "Nuevo item"
2. Item se crea como tipo "Inbox" por defecto
3. Usuario ingresa título
4. Usuario puede:
   - Dejarlo en Inbox para clasificar después
   - Clasificarlo inmediatamente como Tarea o Evento

### Clasificar desde Inbox
1. Usuario va a "Wait List"
2. Selecciona un item
3. Elige tipo: Tarea o Evento
4. Completa campos obligatorios según el tipo
5. Item desaparece de Inbox

### Crear Subtarea
1. Usuario abre una tarea existente
2. Hace clic en "Agregar subtarea"
3. La subtarea hereda el tipo del padre
4. Usuario completa campos
5. Limitación: Si es una subtarea de segundo nivel, no permite más sub-niveles

---

## Roadmap

### MVP (Versión 1.0)
- [x] Sistema de autenticación (login/register)
- [ ] Creación de items (inbox por defecto)
- [ ] Clasificación de items (tarea/evento)
- [ ] Vista de Wait List
- [ ] Dashboard básico
- [ ] Vista de Hoy
- [ ] Sistema de listas
- [ ] Subtareas (1 nivel)

### Versión 1.1
- [ ] Vista de calendario
- [ ] Vista semanal
- [ ] Subtareas (2 niveles)
- [ ] Campos opcionales (prioridad, estado)
- [ ] Scrum Dashboard

### Versión 1.2
- [ ] Adjuntos
- [ ] Filtros avanzados
- [ ] Búsqueda
- [ ] Notificaciones

### Futuro
- [ ] Colaboración (compartir listas)
- [ ] Recordatorios automáticos
- [ ] Integraciones (Google Calendar, etc.)
- [ ] App móvil

---

**Última actualización:** Octubre 5, 2025  
**Versión del documento:** 1.0
