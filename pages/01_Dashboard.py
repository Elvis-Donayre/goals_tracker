"""
=============================================================================
DASHBOARD - VISUALIZACIÓN DE PROGRESO
=============================================================================
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import pandas as pd
from utils.database import SupabaseDB
from utils.helpers import (
    format_duration,
    categorize_completion,
    calculate_weekly_compliance,
    get_color_for_category
)

st.set_page_config(
    page_title="Dashboard - Habit Tracker",
    page_icon="📈",
    layout="wide"
)

# Verificar autenticación
if not st.session_state.get("authenticated"):
    st.warning("⚠️ Debes iniciar sesión primero")
    st.stop()

db = SupabaseDB()
user_id = st.session_state.user_id

# Título
st.title("📈 Dashboard de Progreso")
st.markdown("---")

# Obtener datos
progress = db.get_habit_progress(user_id)
weekly_summary = db.get_weekly_summary(user_id)
activities_matrix = db.get_habit_activities_matrix(user_id)

# Verificar si hay datos
if progress.empty:
    st.info(
        "📊 **No hay datos para mostrar aún**\n\n"
        "Para empezar:\n"
        "1. Crea hábitos en **🎯 Mis Hábitos**\n"
        "2. Crea actividades en **⚡ Actividades**\n"
        "3. Registra sesiones en **📝 Registrar Sesión**"
    )
    st.stop()

# Tabs del dashboard
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Progreso General",
    "📅 Resumen Semanal",
    "⚡ Actividades",
    "📈 Detalles"
])

# ============================================================================
# TAB 1: PROGRESO GENERAL
# ============================================================================
with tab1:
    st.subheader("Progreso por Hábito")

    # Métricas principales
    col1, col2, col3 = st.columns(3)

    with col1:
        total_habits = len(progress)
        st.metric("Total Hábitos Activos", total_habits)

    with col2:
        if not progress.empty and "total_minutes_invested" in progress.columns:
            total_time = progress["total_minutes_invested"].sum()
            time_display = format_duration(int(total_time)) if pd.notna(total_time) and total_time > 0 else "0m"
            st.metric("Tiempo Total Invertido", time_display)

    with col3:
        if not progress.empty and "completion_percentage" in progress.columns:
            avg_completion = progress["completion_percentage"].mean()
            st.metric("Progreso Promedio", f"{avg_completion:.1f}%")

    st.markdown("---")

    # Gráfico de barras de completación
    st.subheader("Porcentaje de Completación")

    if not progress.empty and "completion_percentage" in progress.columns:
        # Preparar datos
        chart_data = progress.copy()
        chart_data = chart_data.sort_values("completion_percentage", ascending=True)

        # Asignar colores según completación
        def get_bar_color(pct):
            if pct >= 75:
                return "#10B981"
            elif pct >= 50:
                return "#3B82F6"
            elif pct >= 25:
                return "#F59E0B"
            else:
                return "#EF4444"

        chart_data["color"] = chart_data["completion_percentage"].apply(get_bar_color)

        # Crear gráfico
        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=chart_data["name"],
            x=chart_data["completion_percentage"],
            orientation="h",
            marker=dict(
                color=chart_data["color"],
                line=dict(color="white", width=1)
            ),
            text=chart_data["completion_percentage"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>" +
                "Completado: %{x:.1f}%<br>" +
                "<extra></extra>"
            )
        ))

        fig.update_layout(
            title="Progreso hacia Objetivos",
            xaxis_title="Porcentaje Completado (%)",
            yaxis_title="",
            height=max(400, len(chart_data) * 60),
            showlegend=False,
            xaxis=dict(range=[0, 105]),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, width='stretch')

    st.markdown("---")

    # Tabla de detalles
    st.subheader("Detalles de Hábitos")

    if not progress.empty:
        display_df = progress[[
            "name",
            "total_minutes_invested",
            "total_hours_goal",
            "completion_percentage"
        ]].copy()

        display_df["total_minutes_invested"] = display_df["total_minutes_invested"].apply(
            lambda x: format_duration(int(x)) if pd.notna(x) and x > 0 else "0m"
        )
        display_df["total_hours_goal"] = display_df["total_hours_goal"].apply(
            lambda x: f"{x}h"
        )
        display_df["completion_percentage"] = display_df["completion_percentage"].apply(
            lambda x: f"{x:.1f}%"
        )

        display_df.columns = ["Hábito", "Tiempo Invertido", "Objetivo", "Completado"]

        st.dataframe(display_df, width='stretch', hide_index=True)

# ============================================================================
# TAB 2: RESUMEN SEMANAL
# ============================================================================
with tab2:
    st.subheader("Cumplimiento Semanal")

    if weekly_summary.empty:
        st.info("No hay datos de esta semana aún.")
    else:
        # Mostrar cada hábito
        for idx, row in weekly_summary.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"### {row['name']}")

                    # Calcular cumplimiento
                    compliance = calculate_weekly_compliance(
                        row.get("minutes_this_week", 0),
                        row["target_minutes_per_week"]
                    )

                    # Barra de progreso
                    progress_pct = min(100, compliance["percentage"])
                    st.progress(progress_pct / 100)

                    # Métricas
                    col_a, col_b, col_c = st.columns(3)

                    with col_a:
                        mins_week = row.get("minutes_this_week", 0)
                        week_display = format_duration(int(mins_week)) if pd.notna(mins_week) and mins_week > 0 else "0m"
                        st.metric("Esta semana", week_display)

                    with col_b:
                        st.metric(
                            "Target",
                            format_duration(row["target_minutes_per_week"])
                        )

                    with col_c:
                        st.metric(
                            "Cumplimiento",
                            f"{compliance['percentage']}%"
                        )

                with col2:
                    st.markdown(
                        f"""
                        <div style='
                            background: {compliance['color']};
                            color: white;
                            padding: 1rem;
                            border-radius: 10px;
                            text-align: center;
                            margin-top: 2rem;
                        '>
                            <h3 style='margin: 0;'>{compliance['status']}</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown("---")

# ============================================================================
# TAB 3: ACTIVIDADES
# ============================================================================
with tab3:
    st.subheader("Análisis de Actividades")

    if activities_matrix.empty:
        st.info("No hay actividades registradas aún.")
    else:
        # Top actividades por tiempo
        st.markdown("### Top Actividades por Tiempo Invertido")

        top_activities = activities_matrix.sort_values(
            "total_minutes", ascending=False
        ).head(10)

        if not top_activities.empty:
            fig = px.bar(
                top_activities,
                x="total_minutes",
                y="activity_name",
                orientation="h",
                labels={
                    "total_minutes": "Minutos Totales",
                    "activity_name": "Actividad"
                },
                color="number_of_habits",
                color_continuous_scale="Blues"
            )

            fig.update_layout(
                height=max(400, len(top_activities) * 50),
                showlegend=True
            )

            st.plotly_chart(fig, width='stretch')

        st.markdown("---")

        # Actividades multi-hábito
        st.markdown("### Actividades que Benefician Múltiples Hábitos")

        multi_habit_activities = activities_matrix[
            activities_matrix["number_of_habits"] > 1
        ].sort_values("number_of_habits", ascending=False)

        if not multi_habit_activities.empty:
            for idx, activity in multi_habit_activities.iterrows():
                st.success(
                    f"**{activity['activity_name']}**\n\n"
                    f"Beneficia **{activity['number_of_habits']} hábitos**: "
                    f"{activity.get('benefited_habits', 'N/A')}"
                )
        else:
            st.info(
                "💡 **Tip:** Crea actividades que beneficien múltiples hábitos "
                "para maximizar tu eficiencia."
            )

# ============================================================================
# TAB 4: DETALLES
# ============================================================================
with tab4:
    st.subheader("Detalles por Hábito")

    # Selector de hábito
    habit_names = progress["name"].tolist()
    selected_habit = st.selectbox("Selecciona un hábito", habit_names)

    if selected_habit:
        habit_data = progress[progress["name"] == selected_habit].iloc[0]

        # Información del hábito
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            mins_invested = habit_data["total_minutes_invested"]
            invested_display = format_duration(int(mins_invested)) if pd.notna(mins_invested) and mins_invested > 0 else "0m"
            st.metric("Tiempo Invertido", invested_display)

        with col2:
            st.metric(
                "Objetivo",
                f"{habit_data['total_hours_goal']}h"
            )

        with col3:
            st.metric(
                "Completado",
                f"{habit_data['completion_percentage']:.1f}%"
            )

        with col4:
            completion_info = categorize_completion(habit_data["completion_percentage"])
            st.metric(
                "Status",
                completion_info["status"]
            )

        st.markdown("---")

        # Targets semanales
        st.markdown("### Targets Semanales")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Mínimo Semanal",
                format_duration(habit_data["target_minutes_per_week"])
            )

        with col2:
            st.metric(
                "Máximo Semanal",
                format_duration(habit_data["max_minutes_per_week"])
            )

        # Progreso visual
        st.markdown("### Visualización de Progreso")

        total_goal_minutes = habit_data["total_hours_goal"] * 60
        invested = habit_data["total_minutes_invested"]
        remaining = max(0, total_goal_minutes - invested)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=["Progreso"],
            y=[invested],
            name="Tiempo Invertido",
            marker_color="#10B981"
        ))

        fig.add_trace(go.Bar(
            x=["Progreso"],
            y=[remaining],
            name="Tiempo Restante",
            marker_color="#E5E7EB"
        ))

        fig.update_layout(
            barmode="stack",
            title=f"Progreso hacia {habit_data['total_hours_goal']} horas",
            yaxis_title="Minutos",
            height=400,
            showlegend=True
        )

        st.plotly_chart(fig, width='stretch')

# Botón de volver
st.markdown("---")
if st.button("🏠 Volver a Inicio"):
    st.switch_page("main.py")
