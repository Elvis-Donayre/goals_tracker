"""
=============================================================================
REGISTRAR SESIÓN - TRACKING DIARIO
=============================================================================
"""

import streamlit as st
import time
from datetime import date, datetime, timedelta
import pandas as pd
from utils.database import SupabaseDB
from utils.helpers import (
    format_duration,
    get_mood_emoji,
    get_productivity_bars,
    format_date_spanish
)

st.set_page_config(
    page_title="Registrar Sesión - Habit Tracker",
    page_icon="📝",
    layout="wide"
)

# Verificar autenticación
if not st.session_state.get("authenticated"):
    st.warning("⚠️ Debes iniciar sesión primero")
    st.stop()

db = SupabaseDB()
user_id = st.session_state.user_id

# Título
st.title("📝 Registrar Sesión")
st.markdown("---")

# Tabs
tab1, tab2 = st.tabs(["➕ Nueva Sesión", "📋 Sesiones Recientes"])

# ============================================================================
# TAB 1: NUEVA SESIÓN
# ============================================================================
with tab1:
    st.subheader("Registrar Nueva Sesión")

    # Obtener actividades
    activities = db.get_user_activities(user_id)

    if activities.empty:
        st.warning(
            "⚠️ **No tienes actividades creadas**\n\n"
            "Antes de registrar sesiones, necesitas:\n"
            "1. Ir a **⚡ Actividades**\n"
            "2. Crear al menos una actividad\n"
            "3. Vincularla a tus hábitos"
        )
        st.stop()

    # Verificar que al menos una actividad esté vinculada
    has_linked_activities = False
    for _, activity in activities.iterrows():
        links = db.get_activity_links(activity['id'])
        if not links.empty:
            has_linked_activities = True
            break

    if not has_linked_activities:
        st.warning(
            "⚠️ **Tus actividades no están vinculadas a hábitos**\n\n"
            "Para que las sesiones cuenten hacia tus metas:\n"
            "1. Ve a **⚡ Actividades**\n"
            "2. Pestaña '🔗 Vincular a Hábitos'\n"
            "3. Conecta tus actividades con tus hábitos"
        )

    with st.form("registrar_sesion_form"):
        # Actividad
        activity_names = {row['name']: row['id'] for _, row in activities.iterrows()}

        selected_activity_name = st.selectbox(
            "¿Qué actividad realizaste?",
            list(activity_names.keys()),
            help="Selecciona la actividad que completaste"
        )

        selected_activity_id = activity_names[selected_activity_name]

        # Mostrar a qué hábitos contribuye
        links = db.get_activity_links(selected_activity_id)

        if not links.empty:
            habit_names = []
            for _, link in links.iterrows():
                habit_info = link.get('habits', {})
                habit_name = habit_info.get('name', 'Desconocido') if isinstance(habit_info, dict) else 'Desconocido'
                weight = link.get('weight', 1.0)
                habit_names.append(f"{habit_name} ({weight*100:.0f}%)")

            st.info(
                f"**Esta actividad contribuye a:**\n\n" +
                "\n".join([f"• {name}" for name in habit_names])
            )

        st.markdown("---")

        # Duración y fecha
        col1, col2 = st.columns(2)

        with col1:
            duration = st.number_input(
                "Duración (minutos)",
                min_value=1,
                max_value=480,
                value=60,
                step=5,
                help="¿Cuántos minutos duraste en esta actividad?"
            )

        with col2:
            session_date = st.date_input(
                "Fecha",
                value=date.today(),
                max_value=date.today(),
                help="¿Cuándo realizaste esta actividad?"
            )

        # Hora de inicio (opcional)
        start_time = st.time_input(
            "Hora de inicio (opcional)",
            value=None,
            help="Si quieres registrar a qué hora empezaste"
        )

        st.markdown("---")

        # Mood y Productividad
        st.markdown("### Estado y Productividad")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**¿Cómo te sentías?**")
            mood = st.slider(
                "Mood",
                min_value=1,
                max_value=5,
                value=3,
                format="%d",
                help="1 = Mal | 2 = Regular | 3 = Bien | 4 = Muy bien | 5 = Excelente",
                label_visibility="collapsed"
            )

            mood_labels = {
                1: "😢 Mal",
                2: "😕 Regular",
                3: "😐 Bien",
                4: "😊 Muy bien",
                5: "😄 Excelente"
            }
            st.write(mood_labels[mood])

        with col2:
            st.markdown("**Nivel de productividad**")
            productivity = st.slider(
                "Productividad",
                min_value=1,
                max_value=5,
                value=3,
                format="%d",
                help="1 = Muy bajo | 5 = Muy alto",
                label_visibility="collapsed"
            )

            st.write(get_productivity_bars(productivity))

        # Notas
        notes = st.text_area(
            "Notas (opcional)",
            placeholder="Ej: Aprendí sobre Serverless en AWS. Muy productivo hoy.",
            help="Escribe cualquier observación sobre la sesión"
        )

        st.markdown("---")

        # Resumen antes de enviar
        st.markdown("### Resumen de la Sesión")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Actividad", selected_activity_name)

        with col2:
            st.metric("Duración", format_duration(duration))

        with col3:
            st.metric("Fecha", format_date_spanish(session_date))

        # Botón de envío
        submit = st.form_submit_button(
            "✅ Registrar Sesión",
            use_container_width=True,
            type="primary"
        )

        if submit:
            with st.spinner("Registrando sesión..."):
                # Convertir start_time a string si existe
                start_time_str = start_time.strftime("%H:%M:%S") if start_time else None

                nueva_sesion = db.register_session(
                    activity_id=selected_activity_id,
                    duration_minutes=duration,
                    session_date=session_date,
                    start_time=start_time_str,
                    notes=notes if notes else None,
                    mood=mood,
                    productivity_level=productivity
                )

                if nueva_sesion:
                    st.success(
                        f"✅ **¡Sesión registrada!**\n\n"
                        f"**{duration} minutos** en **{selected_activity_name}**"
                    )

                    # Mostrar distribución
                    if not links.empty:
                        st.info(
                            "📊 **Distribución automática:**\n\n" +
                            "Tu sesión se ha distribuido automáticamente entre tus hábitos vinculados. "
                            "Ve al **📈 Dashboard** para ver tu progreso actualizado."
                        )

                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Error registrando sesión. Intenta de nuevo.")

# ============================================================================
# TAB 2: SESIONES RECIENTES
# ============================================================================
with tab2:
    st.subheader("Sesiones Recientes")

    # Filtros
    col1, col2 = st.columns(2)

    with col1:
        periodo = st.selectbox(
            "Período",
            ["Últimos 7 días", "Últimos 30 días", "Este mes", "Personalizado"]
        )

    # Calcular fechas según período
    end_date = date.today()

    if periodo == "Últimos 7 días":
        start_date = end_date - timedelta(days=7)
    elif periodo == "Últimos 30 días":
        start_date = end_date - timedelta(days=30)
    elif periodo == "Este mes":
        start_date = date(end_date.year, end_date.month, 1)
    else:
        with col2:
            start_date = st.date_input(
                "Desde",
                value=end_date - timedelta(days=30),
                max_value=end_date
            )

    # Obtener sesiones
    sessions = db.get_user_sessions(
        user_id=user_id,
        limit=100,
        start_date=start_date,
        end_date=end_date
    )

    if sessions.empty:
        st.info("📭 No hay sesiones en este período")
    else:
        # Estadísticas del período
        st.markdown("### Estadísticas del Período")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Sesiones", len(sessions))

        with col2:
            total_duration = sessions["duration_minutes"].sum()
            st.metric("Tiempo Total", format_duration(int(total_duration)))

        with col3:
            avg_duration = sessions["duration_minutes"].mean()
            st.metric("Promedio/Sesión", format_duration(int(avg_duration)))

        with col4:
            if "mood" in sessions.columns and sessions["mood"].notna().any():
                avg_mood = sessions["mood"].mean()
                st.metric("Mood Promedio", f"{avg_mood:.1f}/5")

        st.markdown("---")

        # Tabla de sesiones
        st.markdown("### Detalle de Sesiones")

        # Preparar datos para mostrar
        display_sessions = sessions.copy()

        # Procesar columna de actividad
        if "activities" in display_sessions.columns:
            display_sessions["activity_name"] = display_sessions["activities"].apply(
                lambda x: x.get("name", "N/A") if isinstance(x, dict) else "N/A"
            )
        else:
            display_sessions["activity_name"] = "N/A"

        # Formatear duración
        display_sessions["duration_formatted"] = display_sessions["duration_minutes"].apply(
            lambda x: format_duration(int(x))
        )

        # Formatear mood
        if "mood" in display_sessions.columns:
            display_sessions["mood_emoji"] = display_sessions["mood"].apply(
                lambda x: get_mood_emoji(int(x)) if pd.notna(x) else "—"
            )

        # Seleccionar columnas a mostrar
        columns_to_show = []
        rename_map = {}

        if "session_date" in display_sessions.columns:
            columns_to_show.append("session_date")
            rename_map["session_date"] = "Fecha"

        if "activity_name" in display_sessions.columns:
            columns_to_show.append("activity_name")
            rename_map["activity_name"] = "Actividad"

        if "duration_formatted" in display_sessions.columns:
            columns_to_show.append("duration_formatted")
            rename_map["duration_formatted"] = "Duración"

        if "mood_emoji" in display_sessions.columns:
            columns_to_show.append("mood_emoji")
            rename_map["mood_emoji"] = "Mood"

        if "productivity_level" in display_sessions.columns:
            columns_to_show.append("productivity_level")
            rename_map["productivity_level"] = "Prod."

        if "notes" in display_sessions.columns:
            columns_to_show.append("notes")
            rename_map["notes"] = "Notas"

        display_df = display_sessions[columns_to_show].rename(columns=rename_map)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # Exportar datos
        st.markdown("---")

        if st.button("📥 Exportar a CSV"):
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name=f"sesiones_{start_date}_{end_date}.csv",
                mime="text/csv"
            )

# Botón de volver
st.markdown("---")
if st.button("🏠 Volver a Inicio"):
    st.switch_page("main.py")
