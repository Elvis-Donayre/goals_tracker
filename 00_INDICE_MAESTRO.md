# 📚 HABIT TRACKER - ÍNDICE MAESTRO

**Proyecto:** Habit Tracker con cruces de actividades  
**Fecha:** Enero 8, 2026  
**Estado:** 🟢 Diseño completo, listo para implementación  

---

## 🗂️ DOCUMENTACIÓN DISPONIBLE

### 1️⃣ **01_RESUMEN_EJECUTIVO.md**
**¿QUÉ ES?** El documento para entender la idea completa de un vistazo.

**Contiene:**
- Visión general del proyecto
- El problema que resuelve
- La solución con 3 niveles (Metas → Actividades → Relaciones)
- Flujo de ejemplo completo
- Stack técnico
- Características destacadas
- Próximos pasos

**LEER PRIMERO:** Sí, si es tu primer contacto con el proyecto.

---

### 2️⃣ **03_SCHEMA_SQL.md**
**¿QUÉ ES?** SQL completo para ejecutar en Supabase - La base de datos.

**Contiene:**
- 8 tablas principales (users, categories, habits, activities, habit_activities, sessions, habit_metrics, habit_changes_log)
- **TABLA CLAVE:** `habit_activities` - El cruce inteligente
- Índices para optimización
- 4 vistas SQL precalculadas
- 3 funciones SQL críticas:
  - `register_session()` - Registra y distribuye automáticamente
  - `link_activity_to_habit()` - Vincula con peso
  - `update_habit_metrics()` - Recalcula métricas
- Datos iniciales de prueba
- Queries de verificación

**USAR:** Copia todo el SQL y ejecuta en Supabase SQL Editor.

---

### 3️⃣ **04_GUIA_STREAMLIT.md**
**¿QUÉ ES?** Implementación completa de la interfaz web en Streamlit.

**Contiene:**
- Setup inicial (crear proyecto, instalar dependencias)
- Estructura de carpetas completa
- **Clase SupabaseDB** - 30+ métodos CRUD
- Archivo `main.py` - Landing page
- Páginas Streamlit:
  - `01_Dashboard.py` - Visualizaciones
  - `03_Registrar_Progreso.py` - Registro diario
- Funciones auxiliares
- Configuración (config.toml, secrets.toml)
- Cómo ejecutar

**USAR:** Código base para copiar a tu proyecto.

---

### 4️⃣ **05_MOCKUP_VISUAL.md**
**¿QUÉ ES?** Mockup visual detallado de cómo se ve la interfaz Streamlit.

**Contiene:**
- Página principal de login
- Dashboard con todos los gráficos
- Formulario de registrar sesión
- Configurar actividades y vincular (el cruce)
- Crear hábitos con targets
- Analytics avanzados
- Paleta de colores
- Responsive layout
- Interacciones visuales

**USAR:** Para visualizar exactamente qué verá Elvis en pantalla.

---

### 6️⃣ **07_CREAR_TABLAS_SUPABASE.md**
**¿QUÉ ES?** Guía PASO A PASO con screenshots ASCII de cómo crear tablas en Supabase.

**Contiene:**
- Crear cuenta en supabase.com
- Crear proyecto "habit-tracker"
- Acceder al SQL Editor
- Copiar y ejecutar TODO el SQL
- Verificar tablas creadas
- Obtener credenciales (SUPABASE_URL y KEY)
- Guardar en archivo .env
- Solucionar problemas comunes
- Checklist completo

**USAR:** Cuando estés en Supabase y necesites saber exactamente dónde hacer click.

---

### 7️⃣ **08_SUPABASE_RAPIDO.md**
**¿QUÉ ES?** Resumen super simple en 5 minutos - Solo los pasos esenciales.

**Contiene:**
- 6 pasos principales
- Versión "clicks exactos"
- Checklist más simple
- Cuánto tarda cada cosa
- FAQ rápidas
- GIF imaginario del flujo

**USAR:** Si tienes prisa. Es la versión TL;DR (Too Long; Didn't Read).

---

### 8️⃣ **habit_tracker_architecture.md**
**¿QUÉ ES?** 10 diagramas visuales del proyecto en Mermaid.

**Contiene:**
1. Arquitectura general
2. Flujo de datos
3. Diagrama Entidad-Relación
4. Estructura de carpetas
5. Secuencia de registro
6. Estadísticas y vistas
7. Ciclo de vida de hábito
8. Matriz de seguridad
9. Componentes Streamlit
10. Flujo usuario → datos

**USAR:** Para visualizar cómo funciona. Copia a mermaid.live si quieres editarlos.

---

## 🚀 FLUJO DE IMPLEMENTACIÓN

### Semana 1: Base de Datos

```
1. Crear cuenta Supabase
2. Abrir SQL Editor
3. Copiar schema de 03_SCHEMA_SQL.md
4. Ejecutar
5. Verificar con queries de verificación
```

**Archivos clave:** 03_SCHEMA_SQL.md

### Semana 2: Backend Python

```
1. Crear carpeta proyecto
2. Copiar estructura de carpetas
3. Instalar dependencias (requirements.txt)
4. Copiar clase SupabaseDB de 04_GUIA_STREAMLIT.md
5. Configurar secrets (SUPABASE_URL, SUPABASE_KEY)
6. Probar conexión
```

**Archivos clave:** 04_GUIA_STREAMLIT.md (secciones: Setup, SupabaseDB)

### Semana 3-4: Frontend Streamlit

```
1. Copiar main.py
2. Crear páginas en /pages/
3. Implementar Dashboard
4. Implementar Registrar Sesión
5. Agregar gráficos Plotly
6. Pruebas locales
```

**Archivos clave:** 04_GUIA_STREAMLIT.md (secciones: main.py, páginas)

### Semana 5: Deployment

```
1. Push a GitHub
2. Conectar Streamlit Cloud
3. Configurar secrets en Streamlit Cloud
4. Deploy
```

---

## 💡 CONCEPTOS CLAVE (Quick Reference)

### El Cruce Inteligente (Tabla: habit_activities)

```
Actividad: "Ver videos AWS en YouTube" → 90 minutos
        ↓
Sistema distribuye automáticamente:
├─ Aprender inglés: +90 min (weight = 1.0 = 100%)
└─ Dominar AWS: +72 min (weight = 0.8 = 80%)
        ↓
Registras UNA VEZ, beneficia MÚLTIPLES METAS
```

### Tres Niveles de Tracking

```
SEMANAL:     Target mínimo que quieres hacer (ej: 7h/semana)
             Máximo para evitar burnout (ej: 15h/semana)

TOTAL:       Objetivo acumulado (ej: 500 horas totales)
             Se calcula: % completado, fecha estimada

SESIÓN:      Lo que registras diariamente (ej: 90 minutos hoy)
             Incluye: mood, productividad, notas
```

### Funciones SQL Críticas

```
register_session()          → Registra sesión + distribuye automáticamente
link_activity_to_habit()    → Vincula actividad con peso
update_habit_metrics()      → Recalcula todas las métricas
```

---

## 📊 TABLAS PRINCIPALES

| Tabla | Propósito | Relación Clave |
|-------|-----------|----------------|
| **habits** | Definición de metas | ← tiene |
| **activities** | Actividades concretas | → contribuye a |
| **habit_activities** | **EL CRUCE INTELIGENTE** | muchos-a-muchos con weight |
| **sessions** | Registros de tiempo | cuándo hiciste qué |
| **habit_metrics** | Métricas precalculadas | actualizado automáticamente |
| **categories** | Categorías (Salud, Aprendizaje, etc.) | clasificación |

---

## 🔌 ESTRUCTURA STREAMLIT

```
main.py
├─ Landing page / Login
├─ Tabs principales (Dashboard, Setup, etc.)
└─ Inicializa session_state (db, user_id)

pages/
├─ 01_Dashboard.py      → Gráficos y visualizaciones
├─ 02_Agregar_Habito.py → CRUD de metas
├─ 03_Registrar_Progreso.py → Registrar sesiones DIARIAMENTE
├─ 04_Configurar_Actividades.py → Crear actividades + vincular
└─ 05_Analytics.py      → Análisis avanzados

utils/
├─ database.py          → Clase SupabaseDB (30+ métodos)
└─ helpers.py           → Funciones auxiliares
```

---

## 🎯 VERIFICACIÓN POST-SETUP

### Después de crear BD:
```sql
SELECT COUNT(*) FROM habits;
SELECT COUNT(*) FROM activities;
SELECT COUNT(*) FROM habit_activities;
SELECT * FROM habit_progress LIMIT 5;
SELECT * FROM activity_habit_matrix LIMIT 5;
```

### Después de implementar Streamlit:
```python
# Probar conexión
from utils.database import SupabaseDB
db = SupabaseDB()
categories = db.get_categories()
print(categories)  # Debería printear las categorías
```

---

## 📝 CHECKLIST DE IMPLEMENTACIÓN

### Base de Datos ✅
- [ ] Crear cuenta Supabase
- [ ] Ejecutar schema SQL
- [ ] Verificar tablas creadas
- [ ] Verificar índices creados
- [ ] Verificar vistas creadas
- [ ] Verificar funciones creadas
- [ ] Insertar categorías de prueba

### Backend ✅
- [ ] Crear proyecto local
- [ ] Instalar dependencias
- [ ] Crear archivo .env
- [ ] Configurar SUPABASE_URL y KEY
- [ ] Crear clase SupabaseDB
- [ ] Probar conexión
- [ ] Implementar métodos CRUD

### Frontend ✅
- [ ] Crear main.py
- [ ] Crear carpeta pages/
- [ ] Crear Dashboard
- [ ] Crear Registrar Sesión
- [ ] Crear Configurar Actividades
- [ ] Agregar gráficos
- [ ] Pruebas locales

### Deployment ✅
- [ ] Push a GitHub
- [ ] Conectar Streamlit Cloud
- [ ] Configurar secrets
- [ ] Deploy
- [ ] Pruebas en producción

---

## 🎓 APRENDIZAJE

### Para entender mejor:

1. **Concepto general:** Lee 01_RESUMEN_EJECUTIVO.md
2. **Diagrama visual:** Mira habit_tracker_architecture.md
3. **Modelo de datos:** Estudia 03_SCHEMA_SQL.md (especialmente tabla habit_activities)
4. **Implementación:** Sigue 04_GUIA_STREAMLIT.md paso a paso

### Conceptos importantes:

- **Relación muchos-a-muchos:** Una actividad → múltiples metas (tabla habit_activities)
- **Pesos (weights):** Controlan % de contribución (0-1, donde 1 = 100%)
- **Distribución automática:** La función SQL `register_session()` lo hace
- **Métricas precalculadas:** Se actualizan automáticamente para rapidez

---

## 📞 REFERENCIA RÁPIDA

### Crear hábito con targets

```python
db.create_habit(
    user_id="uuid",
    name="Aprender inglés",
    category_id=2,
    target_minutes_per_week=420,      # 7 horas mín/semana
    max_minutes_per_week=900,         # 15 horas máx/semana
    total_hours_goal=500              # 500 horas objetivo total
)
```

### Vincular actividad a hábito

```python
db.link_activity_to_habit(
    habit_id=1,
    activity_id=5,
    weight=0.8  # 80% contribuye a este hábito
)
```

### Registrar sesión (HACE TODO AUTOMÁTICAMENTE)

```python
db.register_session(
    activity_id=5,
    duration_minutes=90,
    session_date="2026-01-08",
    notes="Serverless en AWS",
    mood=4,
    productivity=5
)
# El sistema automáticamente:
# - Registra la sesión
# - Distribuye 90 min entre hábitos vinculados (con sus pesos)
# - Actualiza métricas
# - Recalcula porcentajes y fechas estimadas
```

### Obtener progreso

```python
progress_df = db.get_habit_progress(user_id)
# Retorna tabla con:
# - name, category, total_minutes_invested, total_minutes_goal
# - completion_percentage, minutes_this_week, is_active, etc.
```

---

## 🔐 SEGURIDAD

- **Supabase Auth:** Implementar para multi-user (futuro)
- **RLS (Row Level Security):** Activar en Supabase para que cada usuario solo vea sus datos
- **API Key:** Usar ANON KEY en frontend (no SERVICE KEY)
- **.env:** Nunca commitear secrets.toml a Git

---

## 📈 ESCALABILIDAD FUTURA

**Fácil de agregar:**
- Más tipos de análisis
- Integración con calendarios
- Notificaciones (email, Telegram, WhatsApp)
- Exportar datos (CSV, PDF)
- Modo dark/light
- Multi-idioma
- Mobile app (Flutter, React Native)

**Difícil de cambiar:**
- Modelo de datos (ya está optimizado)
- Stack tech (Supabase + Streamlit = buena opción)

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Qué pasa si una actividad contribuye a 3 hábitos?**
A: Cada uno recibe su % según el weight. Ej: 90min × 1.0 a A, 90min × 0.8 a B, 90min × 0.5 a C.

**P: ¿Se registra dos veces el tiempo?**
A: No. Registras UNA sesión. El sistema la distribuye automáticamente.

**P: ¿Qué es el weight?**
A: Un decimal 0-1 que controla % de contribución. 0.8 = 80%.

**P: ¿Puedo cambiar los weights después?**
A: Sí, pero no recalcula el pasado. Solo se aplica a futuras sesiones.

**P: ¿Necesito escribir código para usar la app?**
A: No. Es interfaz web. Solo necesitas registrar actividades y sesiones.

---

## 🎬 PRÓXIMOS PASOS

1. **Este chat:** Consolidar docs (✅ HECHO)
2. **Siguiente chat:** Implementar base de datos en Supabase
3. **Chat después:** Implementar Streamlit
4. **Final:** Desplegar en producción

---

**Última actualización:** Enero 8, 2026  
**Versión:** 1.0 - Diseño Completo  
**Estado:** 🟢 Listo para Implementación
