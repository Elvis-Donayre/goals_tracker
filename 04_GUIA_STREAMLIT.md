# GUÍA DE IMPLEMENTACIÓN STREAMLIT

**Para:** Habit Tracker  
**Framework:** Streamlit  
**Versión:** 1.0  

---

## 📋 TABLA DE CONTENIDOS

1. [Setup Inicial](#setup-inicial)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Clase SupabaseDB](#clase-supabasedb)
4. [Archivo main.py](#archivo-mainpy)
5. [Páginas Streamlit](#páginas-streamlit)
6. [Funciones Auxiliares](#funciones-auxiliares)
7. [Configuración](#configuración)

---

## 🚀 SETUP INICIAL

### 1. Crear estructura de carpetas

```bash
mkdir habit-tracker
cd habit-tracker

# Crear estructura
mkdir pages
mkdir utils
mkdir .streamlit
mkdir docs
mkdir diagrams
```

### 2. Crear archivos

```bash
# Archivos raíz
touch main.py
touch requirements.txt
touch .env
touch .gitignore
touch README.md

# Archivos en utils
touch utils/__init__.py
touch utils/database.py
touch utils/helpers.py

# Archivos en .streamlit
touch .streamlit/config.toml
touch .streamlit/secrets.toml
```

### 3. Crear requirements.txt

```txt
streamlit==1.28.0
supabase==2.4.0
python-dotenv==1.0.0
pandas==2.1.0
plotly==5.17.0
numpy==1.24.0
```

### 4. Crear .gitignore

```
.env
.streamlit/secrets.toml
__pycache__/
*.pyc
.DS_Store
*.egg-info/
dist/
build/
.venv/
venv/
```

### 5. Instalar dependencias

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📁 ESTRUCTURA DEL PROYECTO

```
habit-tracker/
├── main.py                           # Landing page principal
├── requirements.txt                  # Dependencias
├── .env                             # Variables de entorno (local)
├── .gitignore
├── README.md
│
├── pages/
│   ├── 01_Dashboard.py              # Visualización general
│   ├── 02_Agregar_Habito.py         # Crear/editar metas
│   ├── 03_Registrar_Progreso.py     # Registrar sesiones
│   ├── 04_Configurar_Actividades.py # Crear/vincular actividades
│   └── 05_Analytics.py              # Análisis avanzados
│
├── utils/
│   ├── __init__.py
│   ├── database.py                  # Clase SupabaseDB
│   └── helpers.py                   # Funciones auxiliares
│
├── .streamlit/
│   ├── config.toml                  # Configuración Streamlit
│   └── secrets.toml                 # Secrets (no comitear)
│
└── docs/
    ├── 01_RESUMEN_EJECUTIVO.md
    ├── 02_ARQUITECTURA_DETALLADA.md
    ├── 03_SCHEMA_SQL.md
    └── 04_GUIA_STREAMLIT.md
```

---

## 🔌 CLASE SUPABASEDB

Archivo: `utils/database.py`

Esta es la clase que gestiona toda la comunicación con Supabase.

```python
"""
utils/database.py - Clase SupabaseDB
Gestiona toda la conexión y operaciones con Supabase
"""

import os
from supabase import create_client, Client
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple


class SupabaseDB:
    """Clase para interactuar con Supabase"""
    
    def __init__(self):
        """Inicializar conexión a Supabase"""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL y SUPABASE_KEY no configuradas")
        
        self.client: Client = create_client(self.url, self.key)
    
    # ========== CATEGORÍAS ==========
    
    def get_categories(self) -> List[Dict]:
        """Obtener todas las categorías"""
        try:
            response = self.client.table("categories").select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    # ========== USUARIOS ==========
    
    def get_or_create_user(self, email: str, full_name: str = "") -> str:
        """Obtener o crear usuario. Retorna user_id"""
        try:
            # Intentar obtener
            response = self.client.table("users").select("id").eq("email", email).execute()
            if response.data:
                return response.data[0]['id']
            
            # Crear si no existe
            response = self.client.table("users").insert({
                "email": email,
                "full_name": full_name
            }).execute()
            
            return response.data[0]['id']
        except Exception as e:
            print(f"Error with user: {e}")
            return None
    
    # ========== HÁBITOS ==========
    
    def get_all_habits(self, user_id: str) -> pd.DataFrame:
        """Obtener todos los hábitos del usuario"""
        try:
            response = self.client.table("habits").select("*").eq("user_id", user_id).execute()
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error getting habits: {e}")
            return pd.DataFrame()
    
    def get_active_habits(self, user_id: str) -> pd.DataFrame:
        """Obtener solo hábitos activos"""
        try:
            response = (
                self.client.table("habits")
                .select("*")
                .eq("user_id", user_id)
                .eq("is_active", True)
                .execute()
            )
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error getting active habits: {e}")
            return pd.DataFrame()
    
    def create_habit(
        self,
        user_id: str,
        name: str,
        category_id: int,
        target_minutes_per_week: int = 420,
        max_minutes_per_week: int = 900,
        total_hours_goal: int = 100,
        description: str = "",
        notes: str = ""
    ) -> Optional[Dict]:
        """Crear nuevo hábito"""
        try:
            data = {
                "user_id": user_id,
                "name": name,
                "category_id": category_id,
                "target_minutes_per_week": target_minutes_per_week,
                "max_minutes_per_week": max_minutes_per_week,
                "total_hours_goal": total_hours_goal,
                "description": description,
                "notes": notes,
                "is_active": True
            }
            response = self.client.table("habits").insert(data).execute()
            
            # Crear métrica asociada
            if response.data:
                habit_id = response.data[0]['id']
                self.client.table("habit_metrics").insert({
                    "habit_id": habit_id
                }).execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating habit: {e}")
            return None
    
    def update_habit(self, habit_id: int, **kwargs) -> bool:
        """Actualizar un hábito"""
        try:
            self.client.table("habits").update(kwargs).eq("id", habit_id).execute()
            return True
        except Exception as e:
            print(f"Error updating habit: {e}")
            return False
    
    def delete_habit(self, habit_id: int) -> bool:
        """Eliminar un hábito"""
        try:
            self.client.table("habits").delete().eq("id", habit_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting habit: {e}")
            return False
    
    # ========== ACTIVIDADES ==========
    
    def get_all_activities(self, user_id: str) -> pd.DataFrame:
        """Obtener todas las actividades del usuario"""
        try:
            response = self.client.table("activities").select("*").eq("user_id", user_id).execute()
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error getting activities: {e}")
            return pd.DataFrame()
    
    def create_activity(
        self,
        user_id: str,
        name: str,
        category_id: int = None,
        description: str = ""
    ) -> Optional[Dict]:
        """Crear nueva actividad"""
        try:
            data = {
                "user_id": user_id,
                "name": name,
                "category_id": category_id,
                "description": description
            }
            response = self.client.table("activities").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating activity: {e}")
            return None
    
    # ========== RELACIONES (El cruce inteligente) ==========
    
    def link_activity_to_habit(
        self,
        habit_id: int,
        activity_id: int,
        weight: float = 1.0
    ) -> bool:
        """Vincular actividad a hábito con peso"""
        try:
            # Usar función SQL
            response = self.client.rpc(
                "link_activity_to_habit",
                {
                    "habit_id_param": habit_id,
                    "activity_id_param": activity_id,
                    "weight_param": weight
                }
            ).execute()
            
            return response.data[0]['success'] if response.data else False
        except Exception as e:
            print(f"Error linking activity to habit: {e}")
            return False
    
    def get_activity_habit_links(self, activity_id: int) -> pd.DataFrame:
        """Obtener todos los hábitos a los que contribuye una actividad"""
        try:
            response = (
                self.client.table("habit_activities")
                .select("habit_id, weight")
                .eq("activity_id", activity_id)
                .execute()
            )
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error getting activity-habit links: {e}")
            return pd.DataFrame()
    
    # ========== SESIONES ==========
    
    def register_session(
        self,
        activity_id: int,
        duration_minutes: int,
        session_date: str = None,
        start_time: str = None,
        notes: str = "",
        mood: int = None,
        productivity: int = None
    ) -> bool:
        """Registrar una sesión. Usa función SQL para distribución automática"""
        try:
            if session_date is None:
                session_date = datetime.now().date().isoformat()
            
            # Usar función SQL que automáticamente distribuye tiempo entre hábitos
            response = self.client.rpc(
                "register_session",
                {
                    "activity_id_param": activity_id,
                    "duration_minutes_param": duration_minutes,
                    "session_date_param": session_date,
                    "start_time_param": start_time,
                    "notes_param": notes,
                    "mood_param": mood,
                    "productivity_param": productivity
                }
            ).execute()
            
            return response.data[0]['success'] if response.data else False
        except Exception as e:
            print(f"Error registering session: {e}")
            return False
    
    def get_sessions_by_activity(
        self,
        activity_id: int,
        days: int = 30
    ) -> pd.DataFrame:
        """Obtener sesiones de una actividad en los últimos N días"""
        try:
            start_date = (datetime.now() - timedelta(days=days)).date().isoformat()
            response = (
                self.client.table("sessions")
                .select("*")
                .eq("activity_id", activity_id)
                .gte("session_date", start_date)
                .order("session_date", desc=False)
                .execute()
            )
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error getting sessions: {e}")
            return pd.DataFrame()
    
    def get_recent_sessions(self, user_id: str, limit: int = 10) -> pd.DataFrame:
        """Obtener sesiones recientes del usuario"""
        try:
            response = (
                self.client.table("sessions")
                .select("""
                    id, activity_id, session_date, duration_minutes, mood,
                    productivity_level, notes, 
                    activities(name)
                """)
                .eq("activities.user_id", user_id)
                .order("session_date", desc=True)
                .limit(limit)
                .execute()
            )
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error getting recent sessions: {e}")
            return pd.DataFrame()
    
    # ========== VISTAS ==========
    
    def get_habit_progress(self, user_id: str) -> pd.DataFrame:
        """Obtener vista de progreso de hábitos"""
        try:
            response = (
                self.client.table("habit_progress")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error getting habit progress: {e}")
            return pd.DataFrame()
    
    def get_activity_habit_matrix(self, user_id: str) -> pd.DataFrame:
        """Obtener matriz de eficiencia de actividades"""
        try:
            response = (
                self.client.table("activity_habit_matrix")
                .select("*")
                .eq("user_id", user_id)
                .order("total_weighted_minutes", desc=True)
                .execute()
            )
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error getting activity habit matrix: {e}")
            return pd.DataFrame()
    
    def get_activity_habit_contribution(self, user_id: str) -> pd.DataFrame:
        """Obtener vista de contribución de actividades a hábitos"""
        try:
            # Nota: Esta vista podría necesitar ajustes en RLS si es restricta
            response = self.client.table("activity_habit_contribution").select("*").execute()
            
            if not response.data:
                return pd.DataFrame()
            
            # Filtrar por user_id
            df = pd.DataFrame(response.data)
            # Aquí necesitaríamos un join con habits para filtrar por user
            return df
        except Exception as e:
            print(f"Error getting activity-habit contribution: {e}")
            return pd.DataFrame()
    
    def get_weekly_summary(self, user_id: str) -> pd.DataFrame:
        """Obtener resumen semanal"""
        try:
            response = (
                self.client.table("weekly_summary")
                .select("*")
                .execute()
            )
            
            if not response.data:
                return pd.DataFrame()
            
            # Filtrar por user_id si es necesario
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error getting weekly summary: {e}")
            return pd.DataFrame()
    
    # ========== MÉTRICAS ==========
    
    def get_habit_metrics(self, habit_id: int) -> Optional[Dict]:
        """Obtener métricas de un hábito"""
        try:
            response = (
                self.client.table("habit_metrics")
                .select("*")
                .eq("habit_id", habit_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting habit metrics: {e}")
            return None
    
    def update_habit_metrics(self, habit_id: int) -> bool:
        """Recalcular métricas de un hábito"""
        try:
            response = self.client.rpc(
                "update_habit_metrics",
                {"habit_id_param": habit_id}
            ).execute()
            
            return bool(response.data)
        except Exception as e:
            print(f"Error updating habit metrics: {e}")
            return False
```

---

## 🎨 ARCHIVO main.py

```python
"""
main.py - Página principal de Habit Tracker
"""

import streamlit as st
from utils.database import SupabaseDB
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Habit Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
<style>
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --background-color: #F7F9FC;
    }
    
    .main {
        background-color: var(--background-color);
    }
    
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar sesión
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if 'db' not in st.session_state:
    try:
        st.session_state.db = SupabaseDB()
    except Exception as e:
        st.error(f"Error conectando a Supabase: {e}")
        st.session_state.db = None

# ========== INTERFAZ ==========

st.title("📊 Habit Tracker")
st.markdown("**Tu gestor inteligente de hábitos con cruces múltiples**")

# Sidebar para login
with st.sidebar:
    st.header("👤 Usuario")
    
    # Simular login (en producción usar Supabase Auth)
    email = st.text_input(
        "Email",
        placeholder="tu@email.com",
        key="email_input"
    )
    
    if st.button("Conectar"):
        if email:
            user_id = st.session_state.db.get_or_create_user(email)
            if user_id:
                st.session_state.user_id = user_id
                st.success(f"✅ Conectado como {email}")
                st.rerun()
            else:
                st.error("Error al conectar")
    
    if st.session_state.user_id:
        st.success(f"✅ Conectado")
        if st.button("Desconectar"):
            st.session_state.user_id = None
            st.rerun()

# Contenido principal
if st.session_state.user_id and st.session_state.db:
    # Obtener datos del usuario
    db = st.session_state.db
    user_id = st.session_state.user_id
    
    # Tabs principales
    tab1, tab2, tab3 = st.tabs(["🏠 Inicio", "📈 Progreso", "⚙️ Setup"])
    
    with tab1:
        st.header("Bienvenido a tu Habit Tracker")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            habits = db.get_active_habits(user_id)
            st.metric("Hábitos Activos", len(habits))
        
        with col2:
            progress = db.get_habit_progress(user_id)
            if len(progress) > 0:
                avg_completion = progress['completion_percentage'].mean()
                st.metric("Promedio Cumplimiento", f"{avg_completion:.1f}%")
            else:
                st.metric("Promedio Cumplimiento", "0%")
        
        with col3:
            st.metric("Últimas Sesiones", "Accede a la página de Dashboard")
        
        with col4:
            st.metric("Actividades", "Configuradas")
        
        st.markdown("---")
        st.subheader("Próximos pasos:")
        st.info("""
        1. **Configurar Actividades**: Crea las actividades que harás día a día
        2. **Crear Metas**: Define tus objetivos con targets (mín/máx semanal y total)
        3. **Vincular**: Conecta actividades con metas (con pesos)
        4. **Registrar**: Empieza a registrar tu progreso diario
        5. **Analizar**: Visualiza tus progreso con gráficos
        """)
    
    with tab2:
        st.header("Tu Progreso")
        
        progress_df = db.get_habit_progress(user_id)
        
        if len(progress_df) > 0:
            for idx, row in progress_df.iterrows():
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.subheader(row['name'])
                        
                        # Barra de progreso
                        completion = min(row['completion_percentage'] / 100, 1.0)
                        st.progress(
                            completion,
                            text=f"{row['completion_percentage']:.1f}% ({row['total_minutes_invested']}m / {row['total_minutes_goal']}m)"
                        )
                        
                        # Info adicional
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("Esta semana", f"{row['minutes_this_week']}m")
                        with col_b:
                            st.metric("Total", f"{row['total_minutes_invested']}m")
                        with col_c:
                            st.metric("Sesiones", row['total_sessions'])
                    
                    with col2:
                        if row['is_active']:
                            st.success("Activo")
                        else:
                            st.warning("Pausado")
                    
                    st.markdown("---")
        else:
            st.info("No tienes hábitos creados. Crea uno en la página 'Configurar Actividades'")
    
    with tab3:
        st.header("Setup Inicial")
        
        setup_tab1, setup_tab2 = st.tabs(["Crear Actividades", "Crear Metas"])
        
        with setup_tab1:
            st.subheader("Nueva Actividad")
            
            with st.form("new_activity"):
                activity_name = st.text_input("Nombre de la actividad")
                category_id = st.selectbox(
                    "Categoría",
                    options=[c['id'] for c in db.get_categories()],
                    format_func=lambda x: next(c['name'] for c in db.get_categories() if c['id'] == x)
                )
                description = st.text_area("Descripción (opcional)")
                
                if st.form_submit_button("Crear Actividad"):
                    if activity_name:
                        new_activity = db.create_activity(
                            user_id=user_id,
                            name=activity_name,
                            category_id=category_id,
                            description=description
                        )
                        if new_activity:
                            st.success(f"✅ Actividad '{activity_name}' creada")
                            st.rerun()
                        else:
                            st.error("Error creando actividad")
                    else:
                        st.error("Por favor ingresa un nombre")
        
        with setup_tab2:
            st.subheader("Nueva Meta/Hábito")
            
            with st.form("new_habit"):
                habit_name = st.text_input("Nombre del hábito/meta")
                category_id = st.selectbox(
                    "Categoría",
                    options=[c['id'] for c in db.get_categories()],
                    format_func=lambda x: next(c['name'] for c in db.get_categories() if c['id'] == x),
                    key="habit_category"
                )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    target_weekly = st.number_input("Target semanal (minutos)", value=420)
                with col2:
                    max_weekly = st.number_input("Máximo semanal (minutos)", value=900)
                with col3:
                    total_goal = st.number_input("Objetivo total (horas)", value=100)
                
                description = st.text_area("Descripción (opcional)")
                notes = st.text_area("Notas (opcional)")
                
                if st.form_submit_button("Crear Hábito"):
                    if habit_name:
                        new_habit = db.create_habit(
                            user_id=user_id,
                            name=habit_name,
                            category_id=category_id,
                            target_minutes_per_week=target_weekly,
                            max_minutes_per_week=max_weekly,
                            total_hours_goal=total_goal,
                            description=description,
                            notes=notes
                        )
                        if new_habit:
                            st.success(f"✅ Hábito '{habit_name}' creado")
                            st.rerun()
                        else:
                            st.error("Error creando hábito")
                    else:
                        st.error("Por favor ingresa un nombre")

else:
    st.warning("⚠️ Por favor conecta tu cuenta primero")
    st.info("""
    Usa el campo de email en la barra lateral para conectarte.
    """)
```

---

## 📄 PÁGINAS STREAMLIT

### Página: 01_Dashboard.py

```python
"""
pages/01_Dashboard.py - Dashboard principal de visualizaciones
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.database import SupabaseDB
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Dashboard", layout="wide")

# Inicializar
if 'db' not in st.session_state:
    st.session_state.db = SupabaseDB()

if 'user_id' not in st.session_state or not st.session_state.user_id:
    st.warning("⚠️ Por favor conéctate primero desde la página principal")
    st.stop()

st.title("📊 Dashboard")

db = st.session_state.db
user_id = st.session_state.user_id

# Obtener datos
progress_df = db.get_habit_progress(user_id)
activity_matrix = db.get_activity_habit_matrix(user_id)

if len(progress_df) == 0:
    st.info("No hay datos para mostrar. Crea hábitos y registra sesiones primero.")
    st.stop()

# TABS
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Progreso",
    "📊 Actividades",
    "⚡ Eficiencia",
    "📅 Detalles"
])

with tab1:
    st.subheader("Progreso por Meta")
    
    # Gráfico 1: Barras de progreso
    fig_progress = px.bar(
        progress_df,
        x='name',
        y='completion_percentage',
        color='completion_percentage',
        color_continuous_scale='RdYlGn',
        title='Porcentaje de Completación por Meta',
        labels={'completion_percentage': 'Completación (%)', 'name': 'Meta'},
        text_auto='.1f'
    )
    
    fig_progress.update_layout(
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_progress, use_container_width=True)
    
    # Gráfico 2: Comparación inverida (target vs real)
    comparison_data = progress_df[['name', 'total_minutes_invested', 'total_minutes_goal']].copy()
    comparison_data['Restante'] = comparison_data['total_minutes_goal'] - comparison_data['total_minutes_invested']
    
    fig_comparison = px.bar(
        comparison_data,
        x='name',
        y=['total_minutes_invested', 'Restante'],
        barmode='stack',
        title='Tiempo Invertido vs Objetivo',
        labels={'value': 'Minutos', 'name': 'Meta'},
        color_discrete_map={'total_minutes_invested': '#2ECC71', 'Restante': '#ECF0F1'}
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)

with tab2:
    st.subheader("Análisis de Actividades")
    
    if len(activity_matrix) > 0:
        # Gráfico 3: Actividades más usadas
        fig_activities = px.bar(
            activity_matrix.head(10),
            x='activity_name',
            y='total_minutes_invested',
            title='Top 10 Actividades por Tiempo Invertido',
            labels={'total_minutes_invested': 'Minutos', 'activity_name': 'Actividad'},
            color='total_sessions',
            color_continuous_scale='Viridis'
        )
        
        fig_activities.update_layout(
            xaxis_tickangle=-45,
            height=400
        )
        
        st.plotly_chart(fig_activities, use_container_width=True)
    else:
        st.info("No hay actividades registradas")

with tab3:
    st.subheader("Eficiencia de Actividades")
    
    if len(activity_matrix) > 0:
        # Actividades que benefician múltiples metas
        multi_benefit = activity_matrix[activity_matrix['num_habits_connected'] > 1].sort_values(
            'total_weighted_minutes',
            ascending=False
        )
        
        if len(multi_benefit) > 0:
            st.write("**Actividades que benefician múltiples metas:**")
            
            fig_multi = px.bar(
                multi_benefit,
                x='activity_name',
                y='num_habits_connected',
                title='Actividades Multi-beneficio (# de metas)',
                labels={'num_habits_connected': 'Metas beneficiadas'},
                color='num_habits_connected',
                color_continuous_scale='Blues'
            )
            
            st.plotly_chart(fig_multi, use_container_width=True)
            
            st.dataframe(
                multi_benefit[['activity_name', 'num_habits_connected', 'contributes_to_habits', 'total_minutes_invested']],
                use_container_width=True
            )
        else:
            st.info("No hay actividades que beneficien múltiples metas")

with tab4:
    st.subheader("Detalles de Hábitos")
    
    st.dataframe(
        progress_df[[
            'name',
            'category',
            'total_minutes_invested',
            'total_minutes_goal',
            'completion_percentage',
            'minutes_this_week',
            'total_sessions',
            'last_session_date'
        ]],
        use_container_width=True
    )
```

### Página: 03_Registrar_Progreso.py

```python
"""
pages/03_Registrar_Progreso.py - Registrar sesiones diarias
"""

import streamlit as st
from utils.database import SupabaseDB
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Registrar Progreso", layout="centered")

if 'db' not in st.session_state:
    st.session_state.db = SupabaseDB()

if 'user_id' not in st.session_state or not st.session_state.user_id:
    st.warning("⚠️ Por favor conéctate primero")
    st.stop()

st.title("📝 Registrar Sesión")

db = st.session_state.db
user_id = st.session_state.user_id

# Obtener actividades del usuario
activities_df = db.get_all_activities(user_id)

if len(activities_df) == 0:
    st.info("❌ No hay actividades. Crea algunas en 'Configurar Actividades' primero")
    st.stop()

# Formulario
with st.form("register_session"):
    st.subheader("Datos de la Sesión")
    
    # Seleccionar actividad
    activity_options = {
        row['name']: row['id']
        for idx, row in activities_df.iterrows()
    }
    
    selected_activity = st.selectbox(
        "¿Qué actividad realizaste?",
        options=list(activity_options.keys())
    )
    
    activity_id = activity_options[selected_activity]
    
    # Duración
    duration_minutes = st.number_input(
        "Duración (minutos)",
        min_value=1,
        max_value=480,
        value=60
    )
    
    # Fecha
    session_date = st.date_input(
        "Fecha",
        value=datetime.now().date()
    )
    
    # Hora (opcional)
    session_time = st.time_input(
        "Hora de inicio (opcional)",
        value=datetime.now().time()
    )
    
    # Notas
    notes = st.text_area(
        "Notas (opcional)",
        placeholder="Detalles sobre tu sesión..."
    )
    
    # Mood
    mood = st.slider(
        "¿Cómo te sentías? (1=mal, 5=excelente)",
        min_value=1,
        max_value=5,
        value=3
    )
    
    # Productividad
    productivity = st.slider(
        "Nivel de productividad (1=bajo, 5=muy alto)",
        min_value=1,
        max_value=5,
        value=3
    )
    
    # Botón de envío
    if st.form_submit_button("📤 Registrar Sesión", use_container_width=True):
        # Convertir a string para SQL
        session_date_str = session_date.isoformat()
        session_time_str = session_time.isoformat() if session_time else None
        
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
            st.success(f"✅ ¡Sesión registrada! {duration_minutes} minutos en {selected_activity}")
            st.balloons()
            
            # Mostrar impacto
            st.info("""
            Esta sesión automáticamente ha actualizado todos tus hábitos vinculados.
            Ve al Dashboard para ver el progreso actualizado.
            """)
        else:
            st.error("❌ Error registrando la sesión")
```

---

## 🛠️ FUNCIONES AUXILIARES

Archivo: `utils/helpers.py`

```python
"""
utils/helpers.py - Funciones auxiliares
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


def calculate_streak(dates: List[str]) -> int:
    """
    Calcula racha de días consecutivos
    Args:
        dates: Lista de fechas ISO format (YYYY-MM-DD)
    Returns:
        Número de días consecutivos
    """
    if not dates:
        return 0
    
    dates = sorted([datetime.fromisoformat(d).date() for d in dates], reverse=True)
    
    streak = 1
    for i in range(len(dates) - 1):
        if (dates[i] - dates[i + 1]).days == 1:
            streak += 1
        else:
            break
    
    return streak


def estimate_completion_date(total_minutes: int, goal_minutes: int, daily_rate: float) -> datetime:
    """
    Estima fecha de completación basada en ritmo actual
    Args:
        total_minutes: Minutos ya invertidos
        goal_minutes: Minutos objetivo
        daily_rate: Promedio de minutos por día
    Returns:
        Fecha estimada de completación
    """
    if daily_rate <= 0:
        return None
    
    remaining = goal_minutes - total_minutes
    if remaining <= 0:
        return datetime.now().date()
    
    days_remaining = remaining / daily_rate
    return (datetime.now() + timedelta(days=days_remaining)).date()


def format_duration(minutes: int) -> str:
    """Convierte minutos a formato legible (ej: '2h 30m')"""
    hours = minutes // 60
    mins = minutes % 60
    
    if hours == 0:
        return f"{mins}m"
    elif mins == 0:
        return f"{hours}h"
    else:
        return f"{hours}h {mins}m"


def get_week_range(date: datetime.date) -> Tuple[datetime.date, datetime.date]:
    """Obtiene el inicio y fin de la semana para una fecha"""
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return start, end
```

---

## ⚙️ CONFIGURACIÓN

### Archivo: .streamlit/config.toml

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true

[logger]
level = "info"

[server]
headless = true
port = 8501
maxUploadSize = 200
runOnSave = true
```

### Archivo: .streamlit/secrets.toml

```toml
# NO COMITEAR ESTE ARCHIVO
# Local development only

SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Archivo: .env (para desarrollo local)

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🚀 CÓMO EJECUTAR

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar en desarrollo
streamlit run main.py

# La app estará en http://localhost:8501
```

---

**Última actualización:** Enero 8, 2026  
**Estado:** Estructura lista, código base funcional
