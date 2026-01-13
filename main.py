"""
=============================================================================
HABIT TRACKER - APLICACIÓN PRINCIPAL
=============================================================================
Sistema de tracking de hábitos con cruces inteligentes entre actividades y metas
"""

import streamlit as st
import time
from utils.database import SupabaseDB
from utils.helpers import validate_email, validate_password

# Configuración de la página
st.set_page_config(
    page_title="Habit Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Personalizado
st.markdown("""
<style>
    /* Estilos generales */
    .main {
        padding-top: 2rem;
    }

    /* Título principal */
    .app-title {
        text-align: center;
        color: #262730;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .app-subtitle {
        text-align: center;
        color: #636E72;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #3B82F6;
    }

    /* Botones */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar la base de datos
@st.cache_resource
def init_database():
    """Inicializar conexión con Supabase"""
    try:
        return SupabaseDB()
    except Exception as e:
        st.error(f"Error conectando con Supabase: {e}")
        st.stop()

db = init_database()

# Inicializar session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None


def login_page():
    """Página de login/registro"""

    # Título
    st.markdown('<h1 class="app-title">📊 Habit Tracker</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="app-subtitle">Tu gestor inteligente de hábitos con cruces múltiples</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Tabs de Login y Registro
    tab1, tab2 = st.tabs(["🔑 Iniciar Sesión", "📝 Registrarse"])

    # TAB 1: LOGIN
    with tab1:
        st.subheader("Inicia Sesión")

        with st.form("login_form"):
            email = st.text_input(
                "Email",
                placeholder="tu@email.com",
                key="login_email"
            )
            password = st.text_input(
                "Contraseña",
                type="password",
                placeholder="Tu contraseña",
                key="login_password"
            )

            col1, col2 = st.columns([1, 1])

            with col1:
                submit = st.form_submit_button(
                    "🔓 Iniciar Sesión",
                    use_container_width=True,
                    type="primary"
                )

            if submit:
                if not email or not password:
                    st.error("❌ Debes completar todos los campos")
                else:
                    with st.spinner("Verificando credenciales..."):
                        result = db.sign_in(email, password)

                        if result.get("success"):
                            st.session_state.authenticated = True
                            st.session_state.user = result.get("user")
                            st.session_state.user_id = result["user"].id
                            st.success("✅ ¡Bienvenido de vuelta!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ {result.get('message', 'Error al iniciar sesión')}")

    # TAB 2: REGISTRO
    with tab2:
        st.subheader("Crear Nueva Cuenta")

        with st.form("signup_form"):
            full_name = st.text_input(
                "Nombre Completo",
                placeholder="Tu nombre",
                key="signup_name"
            )
            email = st.text_input(
                "Email",
                placeholder="tu@email.com",
                key="signup_email"
            )
            password = st.text_input(
                "Contraseña",
                type="password",
                placeholder="Mínimo 8 caracteres",
                key="signup_password",
                help="Debe incluir mayúsculas, minúsculas y números"
            )
            password_confirm = st.text_input(
                "Confirmar Contraseña",
                type="password",
                placeholder="Repite tu contraseña",
                key="signup_password_confirm"
            )

            submit = st.form_submit_button(
                "🚀 Crear Cuenta",
                use_container_width=True,
                type="primary"
            )

            if submit:
                # Validaciones
                if not all([full_name, email, password, password_confirm]):
                    st.error("❌ Debes completar todos los campos")
                elif password != password_confirm:
                    st.error("❌ Las contraseñas no coinciden")
                elif not validate_email(email):
                    st.error("❌ Email inválido")
                else:
                    is_valid, msg = validate_password(password)
                    if not is_valid:
                        st.error(f"❌ {msg}")
                    else:
                        with st.spinner("Creando cuenta..."):
                            result = db.sign_up(email, password, full_name)

                            if result.get("success"):
                                st.success(
                                    "✅ ¡Cuenta creada exitosamente!\n\n"
                                    "Por favor revisa tu email para verificar tu cuenta."
                                )
                                st.info("Ahora puedes iniciar sesión en la pestaña '🔑 Iniciar Sesión'")
                            else:
                                st.error(f"❌ {result.get('message', 'Error al crear cuenta')}")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #636E72; padding: 2rem 0;'>
            <p><strong>Habit Tracker</strong> - Tu aliado para alcanzar metas</p>
            <p style='font-size: 0.9rem;'>Track inteligente • Cruces múltiples • Analytics avanzado</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def main_app():
    """Aplicación principal (después de login)"""

    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user.email}")
        st.markdown(f"ID: `{st.session_state.user_id[:8]}...`")
        st.markdown("---")

        # Navegación
        st.markdown("### 📊 Navegación")

        # Usar markdown con links en lugar de page_link para compatibilidad
        st.markdown("""
        - [📈 Dashboard](pages/01_Dashboard.py)
        - [🎯 Mis Hábitos](pages/02_Mis_Habitos.py)
        - [⚡ Actividades](pages/03_Actividades.py)
        - [📝 Registrar Sesión](pages/04_Registrar_Sesion.py)
        """)

        st.markdown("---")

        # Estadísticas rápidas
        st.markdown("### 📊 Resumen Rápido")

        # Obtener datos
        habits = db.get_user_habits(st.session_state.user_id)
        activities = db.get_user_activities(st.session_state.user_id)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Hábitos", len(habits))
        with col2:
            st.metric("Actividades", len(activities))

        st.markdown("---")

        # Botón de cerrar sesión
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            db.sign_out()
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.user_id = None
            st.rerun()

    # Contenido principal
    st.markdown('<h1 class="app-title">📊 Habit Tracker</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Tabs principales
    tab1, tab2, tab3 = st.tabs(["🏠 Inicio", "📈 Progreso", "⚙️ Setup"])

    # TAB 1: INICIO
    with tab1:
        st.subheader("¡Bienvenido!")

        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h3 style="color: #3B82F6; margin: 0;">Hábitos Activos</h3>
                    <h1 style="margin: 0.5rem 0;">{len(habits)}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h3 style="color: #10B981; margin: 0;">Actividades</h3>
                    <h1 style="margin: 0.5rem 0;">{len(activities)}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Obtener progreso
        progress = db.get_habit_progress(st.session_state.user_id)

        if not progress.empty:
            avg_completion = progress["completion_percentage"].mean()

            with col3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <h3 style="color: #F59E0B; margin: 0;">Progreso Promedio</h3>
                        <h1 style="margin: 0.5rem 0;">{avg_completion:.1f}%</h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Sesiones recientes
        from datetime import date, timedelta
        recent_sessions = db.get_user_sessions(
            st.session_state.user_id,
            limit=10,
            start_date=date.today() - timedelta(days=7)
        )

        with col4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h3 style="color: #EF4444; margin: 0;">Sesiones (7 días)</h3>
                    <h1 style="margin: 0.5rem 0;">{len(recent_sessions)}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        # Primeros pasos
        st.subheader("🚀 Próximos Pasos")

        if len(habits) == 0:
            st.info(
                "👋 **¡Comienza creando tu primer hábito!**\n\n"
                "1. Ve a la página **🎯 Mis Hábitos**\n"
                "2. Crea un hábito con tus objetivos personalizados\n"
                "3. Configura actividades y vincúlalas"
            )
        elif len(activities) == 0:
            st.info(
                "⚡ **Ahora crea actividades**\n\n"
                "1. Ve a la página **⚡ Actividades**\n"
                "2. Crea actividades concretas que realizarás\n"
                "3. Vincúlalas a tus hábitos con pesos"
            )
        else:
            st.success(
                "✅ **¡Todo listo!**\n\n"
                "Ahora puedes:\n"
                "- 📝 **Registrar sesiones** diarias\n"
                "- 📈 **Ver tu progreso** en el Dashboard\n"
                "- 🎯 **Ajustar tus hábitos** según necesites"
            )

    # TAB 2: PROGRESO
    with tab2:
        st.subheader("📈 Resumen de Progreso")

        if progress.empty:
            st.info("No hay datos de progreso aún. Crea hábitos y registra sesiones para ver tu progreso.")
        else:
            # Mostrar tabla de progreso
            st.dataframe(
                progress[[
                    "name", "total_minutes_invested",
                    "total_hours_goal", "completion_percentage",
                    "is_active"
                ]],
                use_container_width=True
            )

    # TAB 3: SETUP
    with tab3:
        st.subheader("⚙️ Configuración")

        st.info(
            "**Configuración Rápida:**\n\n"
            "1. **Hábitos**: Define tus metas personalizadas\n"
            "2. **Actividades**: Crea actividades concretas\n"
            "3. **Vinculación**: Conecta actividades con hábitos (con pesos)\n"
            "4. **Registro**: Empieza a registrar tu progreso"
        )

        with st.expander("ℹ️ ¿Cómo funciona el cruce inteligente?"):
            st.markdown(
                """
                El **cruce inteligente** te permite que una actividad contribuya a **múltiples hábitos** simultáneamente.

                **Ejemplo:**
                - Actividad: "Ver videos AWS en inglés" (90 minutos)
                - Contribuye a:
                  - **Aprender inglés** → 100% (90 minutos)
                  - **Dominar AWS** → 80% (72 minutos)

                **Resultado:** Registras UNA vez, pero beneficia MÚLTIPLES metas.

                Los **pesos** (0.0 a 1.0) controlan qué porcentaje contribuye a cada hábito.
                """
            )


# Ejecutar aplicación
if __name__ == "__main__":
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()
