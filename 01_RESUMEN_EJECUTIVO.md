# HABIT TRACKER - RESUMEN EJECUTIVO

**Fecha de inicio del proyecto:** Enero 2026  
**Versión:** 1.0 - Concepto y diseño completo  
**Autor:** Elvis - Senior Data Analyst & ML Specialist (SUNAT)

---

## 📋 TABLA DE CONTENIDOS

1. [Visión General](#visión-general)
2. [El Problema](#el-problema)
3. [La Solución](#la-solución)
4. [Arquitectura del Sistema](#arquitectura-del-sistema)
5. [Componentes Clave](#componentes-clave)
6. [Siguientes Pasos](#siguientes-pasos)

---

## 🎯 VISIÓN GENERAL

**Objetivo:** Crear un aplicativo web profesional de tracking de hábitos que:
- Capture actividades y tiempo invertido en metas de largo plazo
- Permita que una actividad contribuya a múltiples metas simultáneamente (con pesos ajustables)
- Proporcione análisis avanzados con visualizaciones de progreso
- Se ejecute en la nube (Supabase + Streamlit)
- Sea accesible desde cualquier dispositivo

**Usuarios objetivo:** Elvis (personal use case)

---

## ❌ EL PROBLEMA

### Limitaciones del tracker actual (Google Sheets manual):

1. **Duplicación de registros**: Si estudias AWS en inglés, ¿registras 1 hora en AWS o 1 hora en inglés o ambas?
2. **No captura cruces**: No hay forma de decir "esta actividad beneficia 2 metas a la vez"
3. **Cálculos manuales**: Las métricas, rachas, porcentajes se calculan manualmente
4. **Sin análisis**: No hay visualizaciones, tendencias, proyecciones
5. **No escalable**: Difícil agregar nuevas metas o actividades
6. **Inconsistencia**: Fácil cometer errores al registrar

### Caso de uso específico de Elvis:

- Estudia **AWS** en **Inglés** → beneficia 2 metas a la vez
- Necesita tracking preciso de horas acumuladas
- Quiere visualizar progreso hacia objetivos a largo plazo (ej: 500 horas en inglés)
- Requiere análisis de eficiencia de actividades

---

## ✅ LA SOLUCIÓN

### Concepto Core:

**3 niveles de organización jerárquica:**

1. **METAS (Hábitos)**: Los objetivos a largo plazo
   - Ejemplo: "Aprender inglés", "Dominar AWS", "Hacer ejercicio"
   - Tienen: objetivo total (500h), target semanal (7h), máximo semanal (15h)

2. **ACTIVIDADES**: Las cosas concretas que haces
   - Ejemplo: "Ver videos AWS en YouTube", "Resolver ejercicios Cambridge"
   - Son específicas y medibles

3. **RELACIONES (El cruce inteligente)**: Cómo cada actividad contribuye a múltiples metas
   - "Ver videos AWS" → 100% a "Aprender inglés", 80% a "Dominar AWS"
   - "Leer documentación AWS" → 100% a "Dominar AWS", 50% a "Aprender inglés"

### Flujo de uso:

**Fase 1: Setup (Una sola vez)**
```
Crear actividades → Vincular a metas con pesos → Configurar
```

**Fase 2: Uso diario**
```
Registrar: "Hoy hice Ver videos AWS - 90 minutos"
↓
Sistema automáticamente distribuye:
- 90 min a "Aprender inglés" (100% × 90 = 90 min)
- 72 min a "Dominar AWS" (80% × 90 = 72 min)
↓
Dashboard actualiza automáticamente
```

### Ventaja principal:

**Registras una sola vez, el sistema inteligentemente distribuye el tiempo entre múltiples metas según los pesos que configuraste.**

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Stack Técnico:

```
┌─────────────────────────────────────┐
│      HABIT TRACKER STACK            │
├─────────────────────────────────────┤
│                                     │
│  Frontend: Streamlit (Python)       │
│  ├─ Interfaz web interactiva        │
│  ├─ Gráficos con Plotly             │
│  └─ Hosting: Streamlit Cloud        │
│                                     │
│  Backend: Supabase (Cloud)          │
│  ├─ Base de datos: PostgreSQL       │
│  ├─ API REST auto-generada          │
│  ├─ Funciones SQL: PL/pgSQL         │
│  └─ Row Level Security (RLS)        │
│                                     │
│  Hosting:                           │
│  ├─ Supabase Cloud (BD)             │
│  └─ Streamlit Cloud (App)           │
│                                     │
└─────────────────────────────────────┘
```

### Flujo de datos:

```
Usuario en Streamlit
        ↓
   Interfaz Web
        ↓
   Python/Streamlit
        ↓
   Supabase REST API
        ↓
   PostgreSQL Queries
        ↓
   BD en Supabase
```

---

## 🔧 COMPONENTES CLAVE

### 1. Base de Datos (PostgreSQL en Supabase)

**Tablas principales:**
- `users`: Usuarios del sistema
- `categories`: Categorías de hábitos (Salud, Aprendizaje, etc.)
- `habits`: Definición de metas
- `activities`: Actividades concretas
- `habit_activities`: Relación muchos-a-muchos (el cruce inteligente)
- `sessions`: Registros de tiempo invertido
- `habit_metrics`: Métricas precalculadas

**Vistas:**
- `activity_habit_contribution`: Ve cómo cada actividad contribuye a cada hábito
- `habit_progress`: Progreso actual de cada hábito
- `activity_habit_matrix`: Matriz de eficiencia de actividades

**Funciones SQL:**
- `register_session()`: Registra una sesión y distribuye tiempo automáticamente
- `link_activity_to_habit()`: Vincula actividad a hábito con peso
- `calculate_current_streak()`: Calcula racha actual (opcional)

### 2. Interfaz Streamlit

**Páginas principales:**

1. **main.py** - Landing page
2. **01_Dashboard.py** - Visualización general
   - Progreso por meta
   - Gráficos de tendencias
   - Resumen de actividades
3. **02_Agregar_Habito.py** - CRUD de metas
   - Crear metas con targets (mín/máx semanal, total acumulado)
   - Editar/eliminar metas
4. **03_Registrar_Progreso.py** - Registrar sesiones
   - Seleccionar actividad
   - Ingresar duración
   - Registrar mood/productividad
5. **04_Configurar_Actividades.py** - Gestión de actividades
   - Crear actividades
   - Vincular a metas con pesos
6. **05_Analytics.py** - Análisis avanzados
   - Eficiencia de actividades
   - Matriz de cruces
   - Proyecciones

### 3. Visualizaciones (Gráficos Plotly)

**10 tipos de gráficos:**
1. Barras de progreso por meta
2. Timeline de progreso acumulado
3. Desglose de actividades por meta
4. Matriz de metas vs actividades (heatmap)
5. Contribución de actividades a múltiples metas
6. Cumplimiento semanal vs target
7. Proyecciones de finalización
8. Pie chart de tiempo por categoría
9. Calendario de sesiones
10. Eficiencia de actividades (ROI de tiempo)

---

## 📊 FLUJO COMPLETO DE EJEMPLO

### Escenario: Elvis registra su día

**Actividad registrada:**
```
Hoy hice: "Ver videos AWS en YouTube"
Duración: 90 minutos
Fecha: Miércoles 8 de enero 2026
Notas: "Serverless y EventBridge en inglés"
```

**Lo que pasa automáticamente en la BD:**

1. ✅ Se inserta registro en tabla `sessions`
   - activity_id = Ver videos AWS
   - duration_minutes = 90
   - completed_date = 2026-01-08

2. ✅ Sistema calcula distribución según pesos configurados:
   - "Ver videos AWS" → 100% a "Aprender inglés", 80% a "Dominar AWS"

3. ✅ Se actualizan métricas en `habit_metrics` para ambas metas:
   - Aprender inglés: +90 minutos
   - Dominar AWS: +72 minutos (90 × 0.8)

4. ✅ Se recalculan automáticamente:
   - Total acumulado de cada meta
   - Porcentaje de completación
   - Rachas (si aplica)
   - Fecha estimada de finalización

5. ✅ Dashboard se actualiza automáticamente

**Lo que Elvis ve:**

```
META: APRENDER INGLÉS
├─ Objetivo total: 500 horas
├─ Invertidas: 127.5 horas (27%)
├─ Esta semana: 8.5/7 horas ✅
├─ Racha: 18 días consecutivos
└─ Estimado completar: Agosto 2026

META: DOMINAR AWS
├─ Objetivo total: 200 horas
├─ Invertidas: 89 horas (45%)
├─ Esta semana: 7.2/6 horas ✅
├─ Racha: 22 días consecutivos
└─ Estimado completar: Marzo 2026
```

---

## 📁 ESTRUCTURA DEL PROYECTO

```
habit-tracker/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── main.py
├── pages/
│   ├── 01_Dashboard.py
│   ├── 02_Agregar_Habito.py
│   ├── 03_Registrar_Progreso.py
│   ├── 04_Configurar_Actividades.py
│   └── 05_Analytics.py
├── utils/
│   ├── __init__.py
│   ├── database.py          # Clase SupabaseDB
│   └── helpers.py           # Funciones auxiliares
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml         # (No commitear a Git)
├── docs/
│   ├── 01_RESUMEN_EJECUTIVO.md
│   ├── 02_ARQUITECTURA_DETALLADA.md
│   ├── 03_SCHEMA_SQL.md
│   ├── 04_GUIA_STREAMLIT.md
│   ├── 05_DIAGRAMAS.md
│   └── 06_CASOS_DE_USO.md
└── diagrams/
    └── architecture.mermaid
```

---

## 🚀 SIGUIENTES PASOS

### Fase 1: Base de Datos (Semana 1)
- [ ] Crear cuenta en Supabase
- [ ] Ejecutar script SQL completo
- [ ] Verificar tablas, índices, vistas
- [ ] Probar funciones SQL
- [ ] Población inicial de datos de prueba

### Fase 2: Backend Python (Semana 1-2)
- [ ] Crear clase SupabaseDB en `utils/database.py`
- [ ] Implementar métodos CRUD
- [ ] Implementar funciones de cálculo
- [ ] Crear funciones auxiliares

### Fase 3: Frontend Streamlit (Semana 2-3)
- [ ] Crear estructura de páginas
- [ ] Implementar formularios (crear metas, actividades)
- [ ] Implementar registro de sesiones
- [ ] Implementar configuración de relaciones

### Fase 4: Visualizaciones (Semana 3-4)
- [ ] Implementar los 10 gráficos
- [ ] Crear dashboard principal
- [ ] Crear páginas de análisis

### Fase 5: Deployment (Semana 4)
- [ ] Configurar secrets en Streamlit Cloud
- [ ] Desplegar app
- [ ] Pruebas end-to-end
- [ ] Documentación final

---

## 📚 DOCUMENTACIÓN

Consulta los siguientes archivos para detalles:

1. **02_ARQUITECTURA_DETALLADA.md** - Explicación profunda de cada componente
2. **03_SCHEMA_SQL.md** - SQL completo para ejecutar en Supabase
3. **04_GUIA_STREAMLIT.md** - Implementación de páginas y componentes
4. **05_DIAGRAMAS.md** - Diagramas ER, flujos, arquitectura
5. **06_CASOS_DE_USO.md** - Ejemplos prácticos y escenarios

---

## 🎓 CONCEPTOS CLAVE

### Peso (Weight) en relaciones
- Valor decimal entre 0 y 1
- Representa qué porcentaje de la actividad contribuye a la meta
- Ejemplo: "Ver videos AWS" = 0.8 (80%) a AWS, 1.0 (100%) a Inglés

### Target vs Goal
- **Target semanal**: Mínimo que quieres hacer por semana (ej: 7h)
- **Goal total**: Horas totales que quieres invertir en la meta (ej: 500h)

### Racha (Streak)
- Número de días consecutivos que completaste una meta
- Se reinicia si falta un día

### Proyección de finalización
- Basada en ritmo actual de inversión de tiempo
- Se recalcula automáticamente cada día

---

## 💡 CASOS DE USO PRINCIPALES

1. **Tracking de estudio**: Medir horas en certificaciones (AWS, Cambridge)
2. **Desarrollo personal**: Hábitos de ejercicio, meditación, lectura
3. **Trabajo**: Proyectos y desarrollo profesional
4. **Multicruce**: Una actividad beneficia múltiples metas
5. **Análisis de eficiencia**: Identificar actividades más productivas

---

## ✨ CARACTERÍSTICAS DESTACADAS

✅ **Muchos-a-muchos inteligente**: Una actividad → múltiples metas  
✅ **Pesos ajustables**: Controla contribución de cada actividad  
✅ **Tracking multinivel**: Diario, semanal, mensual, total  
✅ **Automático**: Cálculos automáticos, sin entrada manual  
✅ **Análisis avanzado**: 10 tipos de gráficos diferentes  
✅ **Cloud**: Accesible desde cualquier lugar  
✅ **Escalable**: Fácil agregar metas/actividades  
✅ **Profesional**: Stack tech moderno y robusto  

---

## 📞 REFERENCIA RÁPIDA

| Concepto | Definición | Ejemplo |
|----------|-----------|---------|
| **Hábito/Meta** | Objetivo a largo plazo | "Aprender inglés" |
| **Actividad** | Cosa concreta que haces | "Ver videos AWS" |
| **Sesión** | Registro de tiempo invertido | 90 minutos hoy |
| **Peso/Weight** | Contribución a una meta | 80% a AWS, 100% a Inglés |
| **Target** | Mínimo semanal | 7 horas por semana |
| **Goal** | Máximo acumulado | 500 horas totales |
| **Racha** | Días consecutivos | 18 días seguidos |

---

**Última actualización:** Enero 8, 2026  
**Estado:** Diseño completo, listo para implementación  
**Próxima revisión:** Después de Fase 1
