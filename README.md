# 📊 Habit Tracker - Sistema Inteligente de Tracking de Hábitos

Un sistema completo de tracking de hábitos con **cruces múltiples** que permite que una actividad contribuya a varios hábitos simultáneamente.

## ✨ Características Principales

- 🎯 **Metas Completamente Personalizadas**: Crea exactamente las metas que necesitas, sin restricciones
- ⚡ **Cruce Inteligente**: Una actividad puede beneficiar múltiples hábitos con pesos ajustables
- 📈 **Dashboard Avanzado**: Visualizaciones con Plotly para analizar tu progreso
- 🔐 **Autenticación Completa**: Sistema de login/registro con Supabase Auth
- 📊 **Métricas Automáticas**: Cálculos automáticos de progreso, porcentajes y proyecciones
- 📝 **Registro Diario**: Interfaz intuitiva para registrar sesiones con mood y productividad
- 🎨 **Interfaz Moderna**: UI pulida con Streamlit

## 🏗️ Arquitectura

```
┌─────────────────────────────────────┐
│      FRONTEND: Streamlit            │
│  ├─ Login/Registro                  │
│  ├─ Dashboard con gráficos          │
│  ├─ CRUD de Hábitos                 │
│  ├─ CRUD de Actividades             │
│  └─ Registro de Sesiones            │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│    DATABASE: Supabase (PostgreSQL)  │
│  ├─ Autenticación (Supabase Auth)   │
│  ├─ 8 Tablas principales            │
│  ├─ 4 Vistas SQL precalculadas      │
│  └─ Triggers automáticos            │
└─────────────────────────────────────┘
```

## 📁 Estructura del Proyecto

```
goals_tracker/
├── main.py                     # Aplicación principal con login
├── requirements.txt            # Dependencias
├── .env.example               # Template de variables de entorno
├── .gitignore                 # Archivos a ignorar
│
├── utils/                     # Utilidades
│   ├── __init__.py
│   ├── database.py            # Clase SupabaseDB (30+ métodos)
│   └── helpers.py             # Funciones auxiliares
│
├── pages/                     # Páginas de Streamlit
│   ├── __init__.py
│   ├── 01_Dashboard.py        # Dashboard con gráficos
│   ├── 02_Mis_Habitos.py      # CRUD de hábitos
│   ├── 03_Actividades.py      # CRUD de actividades + vinculación
│   └── 04_Registrar_Sesion.py # Registro diario
│
├── components/                # Componentes reutilizables
│   └── (vacío por ahora)
│
└── config/                    # Configuraciones
    └── (vacío por ahora)
```

## 🚀 Instalación y Configuración

### Paso 1: Clonar el repositorio

```bash
git clone <tu-repo>
cd goals_tracker
```

### Paso 2: Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Supabase

1. Ve a [supabase.com](https://supabase.com)
2. Crea una cuenta (gratis)
3. Crea un nuevo proyecto llamado "habit-tracker"
4. Espera a que se cree (1-2 minutos)

### Paso 5: Ejecutar SQL en Supabase

1. En Supabase Dashboard, ve a **SQL Editor**
2. Abre el archivo `12_SQL_ACTUALIZADO.md` de este proyecto
3. Copia TODO el SQL
4. Pégalo en el editor de Supabase
5. Click en **[▶ Run]**
6. ✅ Deberías ver "Success"

### Paso 6: Obtener credenciales

1. En Supabase Dashboard, ve a **Settings → API**
2. Copia:
   - **Project URL** (ej: `https://xxx.supabase.co`)
   - **anon public** key (la clave larga que empieza con `eyJ...`)

### Paso 7: Configurar variables de entorno

1. Copia `.env.example` a `.env`:

```bash
cp .env.example .env
```

2. Edita `.env` y pega tus credenciales:

```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=eyJhbGciOiJI...tu_clave_aqui
```

### Paso 8: Ejecutar la aplicación

```bash
streamlit run main.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

## 📖 Guía de Uso

### 1. Registro e Inicio de Sesión

- **Primera vez**: Regístrate con email y contraseña
- **Ya tienes cuenta**: Inicia sesión

### 2. Crear Hábitos/Metas

1. Ve a **🎯 Mis Hábitos**
2. Pestaña **➕ Crear Hábito**
3. Escribe tu meta personalizada (ej: "Aprender italiano")
4. Configura targets:
   - **Target semanal**: Mínimo que quieres hacer (ej: 420 min = 7h)
   - **Máximo semanal**: Para evitar burnout (ej: 900 min = 15h)
   - **Objetivo total**: Horas totales que quieres invertir (ej: 500h)
5. Click **Crear Meta**

### 3. Crear Actividades

1. Ve a **⚡ Actividades**
2. Pestaña **➕ Crear Actividad**
3. Escribe qué harás específicamente (ej: "Ver videos AWS en inglés")
4. Opcionalmente asigna una categoría
5. Click **Crear Actividad**

### 4. Vincular Actividades a Hábitos (EL CRUCE INTELIGENTE)

1. En **⚡ Actividades**, ve a **🔗 Vincular a Hábitos**
2. Selecciona una actividad
3. Para cada hábito:
   - ✅ Marca "Vincular" si quieres que contribuya
   - Ajusta el **peso** (0.0 a 1.0):
     - **1.0 (100%)**: Contribuye completamente
     - **0.8 (80%)**: Contribuye parcialmente
     - **0.5 (50%)**: Contribuye la mitad

**Ejemplo:**
```
Actividad: "Ver videos AWS en inglés"
├─ Aprender inglés: 100% (1.0)
└─ Dominar AWS: 80% (0.8)

Cuando registres 90 minutos:
→ 90 min a "Aprender inglés"
→ 72 min a "Dominar AWS" (90 × 0.8)
```

4. Click **Guardar Vínculos**

### 5. Registrar Sesiones Diarias

1. Ve a **📝 Registrar Sesión**
2. Selecciona la actividad que hiciste
3. Ingresa duración en minutos
4. Selecciona la fecha (default: hoy)
5. Opcionalmente:
   - Hora de inicio
   - Mood (1-5)
   - Productividad (1-5)
   - Notas
6. Click **Registrar Sesión**

**Magia:** El sistema automáticamente distribuye el tiempo entre todos los hábitos vinculados según los pesos configurados.

### 6. Ver Progreso en Dashboard

1. Ve a **📈 Dashboard**
2. Explora las 4 pestañas:
   - **Progreso General**: Barras de completación, métricas globales
   - **Resumen Semanal**: Cumplimiento de targets semanales
   - **Actividades**: Top actividades, multi-hábito
   - **Detalles**: Análisis profundo por hábito

## 🔑 Conceptos Clave

### El Cruce Inteligente

La característica principal del sistema. Permite que **una actividad beneficie múltiples hábitos** simultáneamente.

**Sin cruce inteligente:**
```
Estudias AWS en inglés 90 minutos
→ ¿Lo registro en "Inglés" o en "AWS"?
→ Tengo que elegir uno
```

**Con cruce inteligente:**
```
Estudias AWS en inglés 90 minutos
→ Se registra UNA vez
→ Beneficia automáticamente:
   - 90 min a "Aprender inglés" (100%)
   - 72 min a "Dominar AWS" (80%)
```

### Pesos (Weights)

- **Decimal entre 0.0 y 1.0**
- Representa qué porcentaje de la actividad contribuye al hábito
- **1.0 = 100%**: Contribuye completamente
- **0.8 = 80%**: Contribuye en gran medida
- **0.5 = 50%**: Contribuye parcialmente

### Targets Multinivel

Cada hábito tiene 3 niveles de objetivos:

1. **Target Semanal**: Mínimo que quieres hacer por semana
   - Ej: 420 min (7 horas)
   - Para consistencia

2. **Máximo Semanal**: Cap para evitar burnout
   - Ej: 900 min (15 horas)
   - Previene sobreexigencia

3. **Objetivo Total**: Horas totales acumuladas
   - Ej: 500 horas
   - Meta a largo plazo

## 🗄️ Base de Datos

### Tablas Principales

1. **users**: Usuarios del sistema
2. **categories**: Categorías predefinidas (Salud, Aprendizaje, etc.)
3. **user_categories**: Categorías personalizadas del usuario
4. **habits**: Hábitos/metas personalizadas
5. **activities**: Actividades concretas
6. **habit_activities**: **CRUCE INTELIGENTE** (relación muchos-a-muchos con pesos)
7. **sessions**: Registros de tiempo invertido
8. **habit_metrics**: Métricas precalculadas (auto-actualizadas)

### Vistas SQL

1. **habit_progress**: Progreso actual de cada hábito
2. **activity_habit_contribution**: Distribución de sesiones entre hábitos
3. **activity_habit_matrix**: Matriz de eficiencia de actividades
4. **weekly_summary**: Resumen semanal de cumplimiento

### Triggers Automáticos

- **register_session()**: Al insertar una sesión, automáticamente distribuye el tiempo entre hábitos vinculados y actualiza métricas

## 🎨 Stack Tecnológico

- **Frontend**: Streamlit 1.31.0
- **Backend**: Supabase (PostgreSQL + Auth)
- **Visualizaciones**: Plotly 5.18.0
- **Data**: Pandas 2.2.0
- **Env**: python-dotenv 1.0.0
- **Validación**: Pydantic 2.5.0

## 📊 Ejemplo de Flujo Completo

```
1. Elvis se registra
   └─ Email: elvis@example.com

2. Crea hábitos:
   ├─ "Aprender inglés" (500h objetivo)
   └─ "Dominar AWS" (200h objetivo)

3. Crea actividades:
   ├─ "Ver videos AWS en inglés"
   ├─ "Leer documentación AWS"
   └─ "Resolver ejercicios Cambridge"

4. Vincula actividades a hábitos:
   ├─ "Ver videos AWS" → Inglés (100%) + AWS (80%)
   ├─ "Leer docs AWS" → AWS (100%) + Inglés (70%)
   └─ "Ejercicios Cambridge" → Inglés (100%)

5. Registra sesión:
   └─ "Ver videos AWS" - 90 minutos - Hoy

6. Sistema automáticamente:
   ├─ Distribuye: 90 min a Inglés + 72 min a AWS
   ├─ Actualiza métricas
   └─ Recalcula porcentajes

7. Dashboard muestra:
   ├─ Inglés: 90 min invertidos (0.3% de 500h)
   └─ AWS: 72 min invertidos (0.6% de 200h)
```

## 🚀 Deployment

### Streamlit Cloud

1. Sube tu proyecto a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio
4. En **Advanced settings → Secrets**, agrega:

```toml
SUPABASE_URL = "https://..."
SUPABASE_KEY = "eyJ..."
```

5. Deploy

## 🔒 Seguridad

- ✅ Autenticación con Supabase Auth
- ✅ Passwords hasheadas automáticamente
- ✅ Variables de entorno para credenciales
- ✅ `.env` en `.gitignore`
- ⚠️ **Importante**: Usa `anon public` key en frontend (NO la `service_role` key)

## 🐛 Troubleshooting

### Error: "Missing credentials"

- Verifica que `.env` existe y tiene las credenciales correctas
- Reinicia Streamlit después de crear `.env`

### Error: "Table does not exist"

- Asegúrate de haber ejecutado TODO el SQL en Supabase
- Verifica en Supabase → Table Editor que las tablas existan

### Error al crear cuenta

- Supabase requiere email real para verificación
- Revisa tu email (puede estar en spam)
- Si es desarrollo local, desactiva confirmación de email en Supabase → Authentication → Settings

### Las sesiones no actualizan métricas

- Verifica que los triggers SQL se hayan creado correctamente
- Revisa en Supabase → Database → Triggers
- Debe existir `trg_register_session`

## 📝 Próximas Mejoras

- [ ] Exportar datos a PDF/Excel
- [ ] Notificaciones por email
- [ ] Modo oscuro
- [ ] Más tipos de gráficos
- [ ] Integración con calendario
- [ ] Mobile app
- [ ] Compartir progreso en redes sociales

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a branch (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 👨‍💻 Autor

Creado por Elvis - Senior Data Analyst & ML Specialist

## 🙏 Agradecimientos

- Streamlit por el framework
- Supabase por la infraestructura
- Plotly por las visualizaciones

---

**¿Preguntas?** Abre un issue en GitHub.

**¿Te gustó?** Dale una ⭐ al repo.
