# 🔐 AUTENTICACIÓN EN STREAMLIT - GUÍA COMPLETA

**Cómo los usuarios se loguean y registran su progreso**

---

## 📋 TABLA DE CONTENIDOS

1. [Flujo General](#flujo-general)
2. [Opción 1: Login Simple (Recomendado)](#opción-1-login-simple-recomendado)
3. [Opción 2: Login con Contraseña (Más seguro)](#opción-2-login-con-contraseña-más-seguro)
4. [Opción 3: Supabase Auth (Profesional)](#opción-3-supabase-auth-profesional)
5. [Flujo Visual Paso a Paso](#flujo-visual-paso-a-paso)
6. [Código Implementación](#código-implementación)
7. [Seguridad y Mejores Prácticas](#seguridad-y-mejores-prácticas)

---

## 🔄 FLUJO GENERAL

### ¿Qué pasa cuando Elvis abre la app?

```
1. Elvis abre: https://habit-tracker.streamlit.app
                    ↓
2. Streamlit carga main.py
                    ↓
3. Verifica si hay sesión activa en st.session_state
                    ├─ SI: Muestra Dashboard
                    └─ NO: Muestra página de Login
                    ↓
4. Elvis ingresa email: "elvis@example.com"
                    ↓
5. Presiona botón "Conectar"
                    ↓
6. Python verifica en BD si usuario existe
                    ├─ SI: Carga su user_id
                    └─ NO: Crea nuevo usuario
                    ↓
7. Guarda en st.session_state:
   - user_id = "uuid-12345"
   - user_email = "elvis@example.com"
                    ↓
8. Streamlit renderiza Dashboard
                    ↓
9. Elvis ahora puede:
   ✓ Ver progreso (Dashboard)
   ✓ Registrar sesiones
   ✓ Crear metas y actividades
```

---

## 🔓 OPCIÓN 1: LOGIN SIMPLE (Recomendado)

### ¿Cómo funciona?

- Usuario ingresa email
- Sistema verifica en BD
- Si existe: obtiene user_id
- Si NO existe: crea usuario automáticamente
- **NO hay contraseña**

### Ventajas vs Desventajas

```
✅ VENTAJAS:
├─ Súper rápido de implementar
├─ Cero fricción para usuarios
├─ Perfecto para desarrollo
├─ Ideal para uso personal/equipo pequeño
└─ Sin manejo de contraseñas

❌ DESVENTAJAS:
├─ Sin seguridad (cualquiera con email = acceso)
├─ No ideal para producción pública
├─ Fácil impersonación
└─ Mejor para ambiente cerrado
```

### Cuándo usar Opción 1

```
✓ En desarrollo
✓ Uso personal
✓ Equipo pequeño confiable (2-5 personas)
✓ Detrás de firewall/VPN
✗ Aplicación pública
✗ Múltiples usuarios desconocidos
✗ Datos muy sensibles
```

---

## 🔐 OPCIÓN 2: LOGIN CON CONTRASEÑA (Más seguro)

### ¿Cómo funciona?

- Usuario ingresa email + contraseña
- Sistema hashea contraseña
- Verifica en BD
- Si coincide: login
- Si NO coincide: error

### Ventajas vs Desventajas

```
✅ VENTAJAS:
├─ Mucho más seguro que Opción 1
├─ Control de acceso real
├─ Múltiples usuarios seguros
├─ Estándar de industria
└─ Mejor para producción

❌ DESVENTAJAS:
├─ Más código para implementar
├─ Gestión de contraseñas
├─ Recuperación de contraseñas
├─ Usuarios olvidan contraseñas
└─ Más fricción al registrarse
```

### Cuándo usar Opción 2

```
✓ Aplicación con múltiples usuarios
✓ Datos sensibles
✓ Producción pública
✓ Equipo grande
✗ Desarrollo inicial
✗ Prototipado rápido
```

---

## 🪄 OPCIÓN 3: SUPABASE AUTH (Profesional)

### ¿Cómo funciona?

- Supabase maneja toda la autenticación
- Opciones: email/password, Google, GitHub, etc.
- JWT tokens seguros
- Recuperación de contraseña automática
- Multi-factor authentication (MFA)

### Ventajas vs Desventajas

```
✅ VENTAJAS:
├─ Profesional, enterprise-grade
├─ Supabase maneja toda seguridad
├─ OAuth integrado (Google, GitHub)
├─ Multi-factor authentication
├─ Recuperación automática
├─ Menos código en tu app
└─ Escalable

❌ DESVENTAJAS:
├─ Más configuración inicial
├─ Requiere entender JWT
├─ Ligeramente más complejo
└─ Para desarrollo grande
```

### Cuándo usar Opción 3

```
✓ Aplicación grande y profesional
✓ Múltiples usuarios públicos
✓ Necesitas OAuth (Google Sign-In)
✓ Escalabilidad importante
✗ Prototipo rápido
✗ Desarrollo inicial
```

---

## 📊 FLUJO VISUAL PASO A PASO

### Paso 1: Usuario abre la app

```
┌─────────────────────────────────────────────────┐
│                                                 │
│           📊 HABIT TRACKER                      │
│                                                 │
│      Tu gestor inteligente de hábitos          │
│                                                 │
│                                                 │
│  Información de bienvenida...                  │
│                                                 │
│                                                 │
└─────────────────────────────────────────────────┘

     ┌─────────────────────────────────┐
     │  🔐 AUTENTICACIÓN (Sidebar)     │
     ├─────────────────────────────────┤
     │                                 │
     │  Iniciar Sesión                 │
     │                                 │
     │  Email:                         │
     │  ┌────────────────────────────┐ │
     │  │ tu@email.com           ← input
     │  └────────────────────────────┘ │
     │                                 │
     │  ┌────────────────────────────┐ │
     │  │  🔓 Conectar               │ │ ← Botón
     │  └────────────────────────────┘ │
     │                                 │
     └─────────────────────────────────┘
```

### Paso 2: Usuario ingresa email

```
┌─────────────────────────────────────────────────┐
│  Email: elvis@example.com                      │
└─────────────────────────────────────────────────┘

Usuario presiona: [🔓 Conectar]
       ↓
Python ejecuta: login_user("elvis@example.com")
       ↓
Secuencia:
1. Valida que email sea válido
2. Consulta BD: ¿Existe usuario con email?
   
   Query SQL:
   SELECT id FROM users WHERE email = 'elvis@example.com'
   
3. Resultado de BD:
   ├─ SI EXISTE: Obtiene user_id
   └─ NO EXISTE: Crea usuario nuevo
   
   INSERT INTO users (email) VALUES ('elvis@example.com')
   RETURNING id
   
4. Guarda en sesión:
   st.session_state.user_id = "f336d0bc-b841-465b-8045-024475c079dd"
   st.session_state.user_email = "elvis@example.com"
   
5. Streamlit re-renderiza la app
```

### Paso 3: Usuario logueado - Sidebar actualizado

```
     ┌─────────────────────────────────┐
     │  🔐 AUTENTICACIÓN (Sidebar)     │
     ├─────────────────────────────────┤
     │                                 │
     │  ✅ Sesión activa               │
     │                                 │
     │  elvis@example.com              │
     │                                 │
     │  ┌─ 👤 Mi Perfil  (desplegable)│
     │  │  Email: elvis@example.com    │
     │  │  User ID: f336d0bc...        │
     │  └─────────────────────────────┘│
     │                                 │
     │  ┌────────────────────────────┐ │
     │  │  🔓 Desconectar            │ │ ← Logout
     │  └────────────────────────────┘ │
     │                                 │
     └─────────────────────────────────┘
```

### Paso 4: Dashboard cargado

```
┌─────────────────────────────────────────────────────────┐
│ 📊 Habit Tracker > Dashboard                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Tabs: [📈 Progreso] [📊 Actividades] [⚡ Eficiencia]   │
│                                                         │
│ ┌──────────────┬──────────────┬──────────────┐         │
│ │ Hábitos      │ Promedio     │ Últimas      │         │
│ │ Activos      │ Cumplimiento │ Sesiones     │         │
│ │              │              │              │         │
│ │      4       │    82.5%     │    3 hoy     │         │
│ └──────────────┴──────────────┴──────────────┘         │
│                                                         │
│ [Gráficos, tablas, datos del usuario...]              │
│                                                         │
└─────────────────────────────────────────────────────────┘

Ahora Elvis puede:
✓ Ver su Dashboard personal
✓ Crear hábitos (metas)
✓ Crear actividades
✓ Registrar sesiones diarias
✓ Ver análisis
```

### Paso 5: Registrar una sesión

```
Usuario va a: "Registrar Progreso"

┌──────────────────────────────────────────────┐
│ 📝 Registrar Sesión                          │
├──────────────────────────────────────────────┤
│                                              │
│ ¿Qué actividad realizaste?                  │
│ ┌────────────────────────────────────────┐  │
│ │ Ver videos AWS en YouTube           ▼  │  │
│ └────────────────────────────────────────┘  │
│                                              │
│ Duración (minutos)                          │
│ ┌────────────────────────────────────────┐  │
│ │ 90                                     │  │
│ └────────────────────────────────────────┘  │
│                                              │
│ Fecha: 2026-01-08                           │
│ Hora: 18:30                                 │
│ Notas: "Serverless y EventBridge"           │
│ Mood: 😊 (4/5)                             │
│ Productividad: ⚡⚡⚡⚡⚡ (5/5)                 │
│                                              │
│ ┌────────────────────────────────────────┐  │
│ │ 📤 Registrar Sesión                    │  │
│ └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘

Usuario presiona: [📤 Registrar Sesión]
       ↓
Python ejecuta:
db.register_session(
    activity_id=5,
    duration_minutes=90,
    session_date="2026-01-08",
    start_time="18:30",
    notes="Serverless y EventBridge",
    mood=4,
    productivity=5
)
       ↓
SQL function: register_session()
├─ Inserta en tabla sessions
├─ Calcula distribución automática
├─ Actualiza habit_metrics
└─ Retorna success
       ↓
Streamlit muestra:
┌────────────────────────────────────────┐
│ ✅ ¡Sesión registrada! 90 minutos en    │
│    Ver videos AWS en YouTube            │
│                                         │
│ ℹ️ Esta sesión automáticamente ha       │
│    actualizado tus 2 hábitos vinculados │
│                                         │
│ Ve al Dashboard para ver cambios       │
└────────────────────────────────────────┘
       ↓
Dashboard se actualiza automáticamente
```

---

## 💻 CÓDIGO IMPLEMENTACIÓN

### Para Opción 1: Login Simple (Recomendado)

**Archivo: `main.py`**

```python
"""
main.py - Autenticación simple en Streamlit
"""

import streamlit as st
from utils.database import SupabaseDB
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== SETUP ====================

st.set_page_config(
    page_title="Habit Tracker",
    page_icon="📊",
    layout="wide"
)

# Inicializar sesión
if 'db' not in st.session_state:
    st.session_state.db = SupabaseDB()

if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# ==================== FUNCIONES ====================

def login_user(email: str) -> bool:
    """
    LOGIN SIMPLE
    - Valida email
    - Verifica en BD si existe
    - Si NO existe: crea usuario nuevo
    - Guarda en sesión
    """
    
    # Validar email
    if not email or "@" not in email:
        st.error("❌ Por favor ingresa un email válido")
        return False
    
    try:
        # Obtener o crear usuario en BD
        user_id = st.session_state.db.get_or_create_user(email)
        
        if user_id:
            # Guardarlo en sesión (persiste mientras navega)
            st.session_state.user_id = user_id
            st.session_state.user_email = email
            return True
        else:
            st.error("❌ Error en la base de datos")
            return False
    
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return False

def logout_user():
    """Desloguear: Limpiar sesión"""
    st.session_state.user_id = None
    st.session_state.user_email = None

# ==================== SIDEBAR ====================

with st.sidebar:
    st.header("🔐 AUTENTICACIÓN")
    st.markdown("---")
    
    if not st.session_state.user_id:
        # ESTADO: NO LOGUEADO
        st.subheader("Iniciar Sesión")
        st.write("Ingresa tu email para continuar")
        
        email_input = st.text_input(
            label="Email",
            placeholder="tu@email.com",
            key="login_email_input"
        )
        
        if st.button(
            label="🔓 Conectar",
            use_container_width=True,
            type="primary"
        ):
            if login_user(email_input):
                st.success(f"✅ ¡Bienvenido {email_input}!")
                st.rerun()  # Recarga la app
            # Si no es exitoso, el error ya se mostró
    
    else:
        # ESTADO: LOGUEADO
        st.success("✅ Sesión activa", icon="✓")
        
        # Mostrar email del usuario
        st.markdown(f"### {st.session_state.user_email}")
        
        st.markdown("---")
        
        # Perfil expandible
        with st.expander("👤 Mi Perfil"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Email", st.session_state.user_email)
            with col2:
                st.metric("User ID", st.session_state.user_id[:8] + "...")
        
        st.markdown("---")
        
        # Botón de logout
        if st.button(
            label="🔓 Desconectar",
            use_container_width=True
        ):
            logout_user()
            st.info("Sesión cerrada. Recargando...")
            st.rerun()

# ==================== CONTENIDO PRINCIPAL ====================

if not st.session_state.user_id:
    # PÁGINA DE LOGIN (No logueado)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("📊 Habit Tracker")
        st.markdown("### Tu gestor inteligente de hábitos")
        st.markdown("---")
        
        st.markdown("""
        ## ¿Qué es Habit Tracker?
        
        Un aplicativo que te ayuda a rastrear tus hábitos de forma inteligente:
        
        - 📌 **Cruces inteligentes**: Una actividad beneficia múltiples metas
        - 📊 **Análisis automático**: Cálculos y métricas sin esfuerzo
        - 📈 **Visualizaciones**: Gráficos que motivan y enseñan
        - 🎯 **Targets flexibles**: Mínimos, máximos y objetivos a largo plazo
        
        ### Ejemplo real:
        
        *Estudias "AWS en inglés" 90 minutos:*
        - ✓ 90 minutos a "Aprender inglés"
        - ✓ 72 minutos a "Dominar AWS" (80% del tiempo)
        
        **Registras UNA VEZ, beneficia DOS metas automáticamente**
        
        ---
        
        ### Características
        
        ✨ Tracking multinivel (sesión, semanal, mensual, total)
        ⚡ Distribución automática entre metas
        📱 Accesible desde cualquier dispositivo
        🔒 Tus datos privados y seguros
        
        ---
        
        ### Cómo empezar
        
        1. **Ingresa tu email** en la barra lateral
        2. **Presiona "Conectar"**
        3. **¡Listo!** Comienza a crear hábitos
        
        No necesitas contraseña. Solo tu email.
        """)

else:
    # CONTENIDO PRINCIPAL (Logueado)
    
    st.title("📊 Dashboard")
    st.markdown(f"Bienvenido, **{st.session_state.user_email}**")
    
    db = st.session_state.db
    user_id = st.session_state.user_id
    
    # Tabs principales
    tab1, tab2, tab3 = st.tabs(["📈 Progreso", "⚙️ Setup", "📊 Analytics"])
    
    with tab1:
        st.subheader("Tu Progreso")
        
        # Obtener datos del usuario
        progress_df = db.get_habit_progress(user_id)
        
        if len(progress_df) == 0:
            st.info("📝 No tienes hábitos creados. Ve a Setup para crear algunos.")
        else:
            # Mostrar hábitos en cards
            for idx, row in progress_df.iterrows():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(row['name'])
                    
                    # Barra de progreso
                    completion = min(row['completion_percentage'] / 100, 1.0)
                    st.progress(
                        completion,
                        text=f"{row['completion_percentage']:.1f}% completado"
                    )
                    
                    # Métricas
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Invertido", f"{row['total_minutes_invested']}m")
                    with col_b:
                        st.metric("Objetivo", f"{row['total_minutes_goal']}m")
                    with col_c:
                        st.metric("Sesiones", row['total_sessions'])
                
                with col2:
                    if row['is_active']:
                        st.success("Activo")
                    else:
                        st.warning("Pausado")
                
                st.markdown("---")
    
    with tab2:
        st.subheader("Setup Inicial")
        
        setup_tab1, setup_tab2 = st.tabs(["Crear Hábito", "Crear Actividad"])
        
        with setup_tab1:
            st.write("**Crear una nueva meta/hábito**")
            
            with st.form("create_habit_form"):
                habit_name = st.text_input("Nombre del hábito")
                category_options = {c['name']: c['id'] for c in db.get_categories()}
                category_id = st.selectbox(
                    "Categoría",
                    options=list(category_options.keys()),
                    format_func=str
                )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    target_weekly = st.number_input(
                        "Target semanal (minutos)",
                        value=420
                    )
                with col2:
                    max_weekly = st.number_input(
                        "Máximo semanal (minutos)",
                        value=900
                    )
                with col3:
                    total_goal = st.number_input(
                        "Objetivo total (horas)",
                        value=100
                    )
                
                description = st.text_area("Descripción (opcional)")
                
                if st.form_submit_button("✅ Crear Hábito"):
                    if habit_name:
                        new_habit = db.create_habit(
                            user_id=user_id,
                            name=habit_name,
                            category_id=category_options[category_id],
                            target_minutes_per_week=target_weekly,
                            max_minutes_per_week=max_weekly,
                            total_hours_goal=total_goal,
                            description=description
                        )
                        if new_habit:
                            st.success(f"✅ Hábito '{habit_name}' creado")
                            st.rerun()
                        else:
                            st.error("Error creando hábito")
                    else:
                        st.error("Ingresa un nombre")
        
        with setup_tab2:
            st.write("**Crear una nueva actividad**")
            
            with st.form("create_activity_form"):
                activity_name = st.text_input("Nombre de la actividad")
                category_options = {c['name']: c['id'] for c in db.get_categories()}
                category_id = st.selectbox(
                    "Categoría",
                    options=list(category_options.keys()),
                    format_func=str,
                    key="activity_category"
                )
                description = st.text_area("Descripción (opcional)")
                
                if st.form_submit_button("✅ Crear Actividad"):
                    if activity_name:
                        new_activity = db.create_activity(
                            user_id=user_id,
                            name=activity_name,
                            category_id=category_options[category_id],
                            description=description
                        )
                        if new_activity:
                            st.success(f"✅ Actividad '{activity_name}' creada")
                            st.rerun()
                        else:
                            st.error("Error creando actividad")
                    else:
                        st.error("Ingresa un nombre")
    
    with tab3:
        st.subheader("Analytics")
        st.info("Dashboard de análisis avanzados (implementar con gráficos Plotly)")
```

**Archivo: `pages/03_Registrar_Progreso.py`**

```python
"""
pages/03_Registrar_Progreso.py - Registrar sesiones diarias
"""

import streamlit as st
from datetime import datetime
from utils.database import SupabaseDB

st.set_page_config(page_title="Registrar Progreso")

# Verificar que esté logueado
if 'user_id' not in st.session_state or not st.session_state.user_id:
    st.warning("⚠️ Por favor loguéate primero desde la página principal")
    st.stop()

st.title("📝 Registrar Sesión")

db = st.session_state.db
user_id = st.session_state.user_id

# Obtener actividades del usuario
activities_df = db.get_all_activities(user_id)

if len(activities_df) == 0:
    st.error("❌ No hay actividades. Crea algunas en la página principal primero.")
    st.stop()

# FORMULARIO DE REGISTRO
with st.form("register_session_form"):
    st.subheader("Datos de la sesión")
    
    # Seleccionar actividad
    activity_options = {
        row['name']: row['id']
        for idx, row in activities_df.iterrows()
    }
    
    selected_activity = st.selectbox(
        "¿Qué actividad realizaste?",
        options=list(activity_options.keys()),
        index=0
    )
    
    activity_id = activity_options[selected_activity]
    
    # Duración
    col1, col2 = st.columns(2)
    with col1:
        duration_minutes = st.number_input(
            "Duración (minutos)",
            min_value=1,
            max_value=480,
            value=60
        )
    
    # Fecha
    with col2:
        session_date = st.date_input(
            "Fecha",
            value=datetime.now().date()
        )
    
    # Hora
    session_time = st.time_input(
        "Hora de inicio (opcional)",
        value=datetime.now().time()
    )
    
    # Notas
    notes = st.text_area(
        "Notas (opcional)",
        placeholder="Detalles sobre la sesión..."
    )
    
    # Mood y Productividad
    col1, col2 = st.columns(2)
    
    with col1:
        mood = st.slider(
            "¿Cómo te sentías?",
            min_value=1,
            max_value=5,
            value=3,
            format="😐"
        )
    
    with col2:
        productivity = st.slider(
            "Nivel de productividad",
            min_value=1,
            max_value=5,
            value=3
        )
    
    # BOTÓN DE ENVÍO
    if st.form_submit_button("📤 Registrar Sesión", use_container_width=True):
        
        # Convertir a string para SQL
        session_date_str = session_date.isoformat()
        session_time_str = session_time.isoformat()
        
        # Registrar
        success = db.register_session(
            activity_id=activity_id,
            duration_minutes=duration_minutes,
            session_date=session_date_str,
            start_time=session_time_str,
            notes=notes,
            mood=mood,
            productivity=productivity
        )
        
        if success:
            st.success(
                f"✅ ¡Sesión registrada!\n\n"
                f"{duration_minutes} minutos en {selected_activity}\n\n"
                f"Esta sesión automáticamente ha actualizado tus hábitos vinculados."
            )
            st.balloons()
        else:
            st.error("❌ Error al registrar sesión")
```

---

## 🔐 SEGURIDAD Y MEJORES PRÁCTICAS

### Session State en Streamlit

```python
# ✅ CORRECTO: Usar session_state para datos de sesión
st.session_state.user_id = user_id
st.session_state.user_email = email

# ❌ INCORRECTO: Guardar en variables locales
user_id = user_id  # Se pierde al recargar
```

### Verificar Login en Cada Página

```python
# Al inicio de cada página secundaria:

if 'user_id' not in st.session_state or not st.session_state.user_id:
    st.warning("⚠️ Por favor loguéate primero")
    st.stop()  # Detiene la ejecución

# Continuar con código protegido
user_id = st.session_state.user_id
```

### Flujo de Seguridad

```
1. Usuario abre app
   ↓
2. Verifica: ¿Tiene session_state.user_id?
   ├─ NO → Muestra login
   └─ SÍ → Carga dashboard
   
3. Usuario va a /pages/03_Registrar_Progreso
   ↓
4. Verifica nuevamente: ¿Tiene user_id?
   ├─ NO → Muestra warning y detiene
   └─ SÍ → Permite registrar
   
5. Usuario presiona logout
   ↓
6. Limpia session_state
   ↓
7. Recarga → Vuelve al login
```

### Password Security (Si usas Opción 2)

```python
# NUNCA HAGAS ESTO:
if password == "1234":  # ❌ Inseguro
    login()

# SIEMPRE HAZE ESTO:
from bcrypt import hashpw, checkpw

# Al registrar:
hashed = hashpw(password.encode(), salt=bcrypt.gensalt())
db.save_password_hash(user_id, hashed)

# Al verificar:
stored_hash = db.get_password_hash(user_id)
if checkpw(password.encode(), stored_hash):
    login()
```

---

## 🎯 RESUMEN VISUAL

### Arquitectura de Login

```
┌─────────────────────────────────────┐
│         main.py                     │
│  (Página principal con login)       │
├─────────────────────────────────────┤
│                                     │
│  1. Sidebar: Input email            │
│  2. Botón: [🔓 Conectar]            │
│  3. Valida email                    │
│  4. Query BD: get_or_create_user()  │
│  5. Guarda en st.session_state      │
│  6. Recarga → Muestra dashboard     │
│                                     │
└─────────────────────────────────────┘
         ↓ (Logueado)
┌─────────────────────────────────────┐
│    /pages/01_Dashboard.py           │
│    /pages/03_Registrar_Progreso.py  │
│    /pages/04_Configurar_Act.py      │
├─────────────────────────────────────┤
│                                     │
│  Verifican: ¿user_id en session?   │
│  SI → Muestra contenido             │
│  NO → Muestra warning               │
│                                     │
│  Todas acceden a:                   │
│  - st.session_state.user_id         │
│  - st.session_state.user_email      │
│                                     │
└─────────────────────────────────────┘
```

---

## 📝 CHECKLIST AUTENTICACIÓN

Para Opción 1 (Simple):

- [ ] Crear main.py con sidebar login
- [ ] Implementar login_user() function
- [ ] Implementar logout_user() function
- [ ] Guardar en st.session_state
- [ ] Verificar en cada página secundaria
- [ ] Método get_or_create_user() en SupabaseDB
- [ ] Probar login/logout flujo
- [ ] Probar persistencia entre páginas

---

**Estado:** ✅ Autenticación simple lista para implementar  
**Última actualización:** Enero 8, 2026  
**Versión:** 1.0
