"""
=============================================================================
GESTIÓN DE HÁBITOS - CREAR, EDITAR, ELIMINAR
=============================================================================
"""

import streamlit as st
import time
from datetime import datetime, timedelta
from utils.database import SupabaseDB
from utils.helpers import (
    calculate_weeks_to_goal,
    format_duration,
    categorize_completion
)

st.set_page_config(
    page_title="Mis Hábitos - Habit Tracker",
    page_icon="🎯",
    layout="wide"
)

# Verificar autenticación
if not st.session_state.get("authenticated"):
    st.warning("⚠️ Debes iniciar sesión primero")
    st.stop()

db = SupabaseDB()
user_id = st.session_state.user_id

# Título
st.title("🎯 Mis Hábitos")
st.markdown("---")

# Tabs
tab1, tab2 = st.tabs(["➕ Crear Hábito", "📋 Mis Hábitos"])

# ============================================================================
# TAB 1: CREAR HÁBITO
# ============================================================================
with tab1:
    st.subheader("Crear Nueva Meta Personalizada")

    # Opción de creación
    opcion_creacion = st.radio(
        "¿Cómo quieres crear tu meta?",
        ["✍️ Escribir mi propia meta", "💡 Ver sugerencias por categoría"],
        index=0
    )

    if opcion_creacion == "✍️ Escribir mi propia meta":
        # ────────────────────────────────────────────────────────────
        # OPCIÓN: COMPLETAMENTE PERSONALIZADO
        # ────────────────────────────────────────────────────────────

        st.write("**Crea exactamente la meta que necesitas**")

        with st.form("crear_habito_personalizado"):

            # Nombre de la meta
            nombre_meta = st.text_input(
                label="¿Cuál es tu meta?",
                placeholder="Ej: Aprender italiano, Escribir una novela, Meditar 30 min diarios",
                max_chars=255,
                help="Escribe exactamente lo que quieres lograr"
            )

            # Descripción (opcional)
            descripcion = st.text_area(
                label="Descripción (opcional)",
                placeholder="Ej: Quiero hablar italiano para viajar a Roma. Meta: Conversaciones fluidas",
                max_chars=1000,
                help="Da contexto sobre por qué esta meta es importante para ti"
            )

            st.markdown("---")

            # Categoría (OPCIONAL)
            st.write("**Asignar a una categoría (opcional)**")

            usar_categoria = st.checkbox(
                "Quiero categorizar esta meta",
                value=False,
                help="Las categorías ayudan a organizar tu progreso"
            )

            category_id = None

            if usar_categoria:
                col1, col2 = st.columns([3, 1])

                with col1:
                    # Obtener todas las categorías
                    todas_categorias = db.get_all_categories_for_user(user_id)

                    if todas_categorias:
                        # Agrupar por tipo
                        cat_names = []
                        cat_map = {}

                        # Categorías predefinidas primero
                        predefined = [c for c in todas_categorias if c['type'] == 'system']
                        personal = [c for c in todas_categorias if c['type'] == 'personal']

                        for cat in predefined:
                            cat_names.append(f"📌 {cat['name']}")
                            cat_map[f"📌 {cat['name']}"] = cat['id']

                        for cat in personal:
                            cat_names.append(f"⭐ {cat['name']}")
                            cat_map[f"⭐ {cat['name']}"] = cat['id']

                        categoria_selected = st.selectbox(
                            "Elige categoría",
                            options=cat_names,
                            help="📌 = Sugeridas  |  ⭐ = Tus categorías"
                        )

                        category_id = cat_map[categoria_selected]

            st.markdown("---")

            # TARGETS
            st.write("**Configura tus objetivos**")

            col1, col2, col3 = st.columns(3)

            with col1:
                target_weekly = st.number_input(
                    label="Target semanal (minutos)",
                    min_value=30,
                    max_value=10000,
                    value=420,
                    step=30,
                    help="¿Cuántos minutos mínimo por semana? (Ej: 420 = 7 horas)"
                )

            with col2:
                max_weekly = st.number_input(
                    label="Máximo semanal (minutos)",
                    min_value=60,
                    max_value=10000,
                    value=900,
                    step=30,
                    help="¿Cuál es el máximo para no sufrir burnout? (Ej: 900 = 15 horas)"
                )

            with col3:
                total_goal = st.number_input(
                    label="Objetivo total (horas)",
                    min_value=10,
                    max_value=10000,
                    value=100,
                    step=10,
                    help="¿Cuántas horas totales quieres invertir? (Ej: 100 horas)"
                )

            # Estimación
            if target_weekly > 0:
                semanas_requeridas, fecha_estimada = calculate_weeks_to_goal(
                    0, total_goal, target_weekly
                )

                st.info(
                    f"📈 Con **{format_duration(target_weekly)}/semana**, completarás {total_goal}h en "
                    f"~**{semanas_requeridas} semanas** (**{fecha_estimada}**)"
                )

            st.markdown("---")

            # BOTÓN ENVÍO
            submit = st.form_submit_button(
                label="✅ Crear Meta",
                width='stretch',
                type="primary"
            )

            if submit:
                if nombre_meta and nombre_meta.strip():
                    # Validar que máximo sea mayor que target
                    if max_weekly < target_weekly:
                        st.error("❌ El máximo semanal debe ser mayor o igual al target semanal")
                    else:
                        with st.spinner("Creando hábito..."):
                            nuevo_habito = db.create_habit(
                                user_id=user_id,
                                name=nombre_meta,
                                description=descripcion if descripcion else None,
                                category_id=category_id,
                                target_minutes_per_week=target_weekly,
                                max_minutes_per_week=max_weekly,
                                total_hours_goal=total_goal
                            )

                            if nuevo_habito:
                                st.success(
                                    f"✅ ¡Meta '{nombre_meta}' creada!\n\n"
                                    f"Ahora puedes:\n"
                                    f"1. Crear actividades que te ayuden\n"
                                    f"2. Vincularlas con pesos\n"
                                    f"3. Empezar a registrar tu progreso"
                                )
                                st.balloons()
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("❌ Error creando la meta. Intenta de nuevo.")
                else:
                    st.error("❌ Debes ingresar un nombre para tu meta")

    else:
        # ────────────────────────────────────────────────────────────
        # OPCIÓN: SUGERENCIAS POR CATEGORÍA
        # ────────────────────────────────────────────────────────────

        st.write("**Inspiración: Sugerencias por categoría**")
        st.info(
            "Puedes usar estas ideas como inspiración, o escribir lo que quieras en la opción anterior"
        )

        sugerencias = {
            "🎓 Aprendizaje": [
                "Aprender nuevo idioma",
                "Dominar una tecnología (AWS, Python, React)",
                "Leer X libros este año",
                "Completar un curso online",
                "Estudiar para certificación",
                "Mejorar habilidades de escritura"
            ],
            "❤️ Salud": [
                "Hacer ejercicio 4 veces por semana",
                "Meditar diariamente",
                "Mejorar alimentación",
                "Dormir 8 horas por noche",
                "Yoga o estiramientos",
                "Correr X km por semana"
            ],
            "⚡ Productividad": [
                "Escribir en blog/newsletter",
                "Trabajar en proyecto personal",
                "Networking (contactar personas)",
                "Leer documentación técnica",
                "Code review y contributing",
                "Automatizar tareas repetitivas"
            ],
            "🌱 Desarrollo Personal": [
                "Lectura de crecimiento personal",
                "Journaling (escribir diarios)",
                "Prácticas de mindfulness",
                "Aprender nuevas habilidades",
                "Reflexión y autoanálisis",
                "Mentoring a otros"
            ],
            "👥 Relaciones": [
                "Pasar tiempo con familia",
                "Networking profesional",
                "Reuniones con amigos",
                "Comunicación efectiva",
                "Voluntariado",
                "Mentoría"
            ],
            "💰 Finanzas": [
                "Aprender sobre inversiones",
                "Ahorrar X dinero mensual",
                "Estudiar mercados/trading",
                "Planificación financiera",
                "Presupuesto personal",
                "Educación sobre criptomonedas"
            ]
        }

        # Selector de categoría
        categoria_sugerencia = st.selectbox(
            "Elige una categoría",
            list(sugerencias.keys())
        )

        # Mostrar sugerencias
        st.write(f"**Sugerencias para {categoria_sugerencia}:**")

        for sugerencia in sugerencias[categoria_sugerencia]:
            st.write(f"• {sugerencia}")

        st.info("💡 Usa estas sugerencias como inspiración y créalas en la opción 'Escribir mi propia meta'")

# ============================================================================
# TAB 2: MIS HÁBITOS
# ============================================================================
with tab2:
    st.subheader("Tus Metas Creadas")

    # Obtener hábitos
    habits = db.get_user_habits(user_id, active_only=False)

    if habits.empty:
        st.info("📝 Aún no has creado ninguna meta. ¡Crea la primera en la pestaña '➕ Crear Hábito'!")
    else:
        # Filtros
        col1, col2 = st.columns([2, 1])

        with col1:
            filtro_status = st.radio(
                "Filtrar por:",
                ["Todos", "Solo Activos", "Solo Inactivos"],
                horizontal=True
            )

        # Aplicar filtro
        if filtro_status == "Solo Activos":
            habits_filtrados = habits[habits["is_active"] == True]
        elif filtro_status == "Solo Inactivos":
            habits_filtrados = habits[habits["is_active"] == False]
        else:
            habits_filtrados = habits

        st.markdown("---")

        # Mostrar cada hábito
        for idx, habit in habits_filtrados.iterrows():
            with st.expander(
                f"{'🎯' if habit['is_active'] else '⏸️'} {habit['name']}",
                expanded=False
            ):
                col1, col2 = st.columns([3, 1])

                with col1:
                    # Descripción
                    if habit.get("description"):
                        st.write(f"*{habit['description']}*")

                    # Métricas
                    metric_cols = st.columns(4)

                    with metric_cols[0]:
                        st.metric(
                            "Target/semana",
                            format_duration(habit["target_minutes_per_week"])
                        )

                    with metric_cols[1]:
                        st.metric(
                            "Máx/semana",
                            format_duration(habit["max_minutes_per_week"])
                        )

                    with metric_cols[2]:
                        st.metric(
                            "Objetivo total",
                            f"{habit['total_hours_goal']}h"
                        )

                    with metric_cols[3]:
                        status_text = "✅ Activo" if habit["is_active"] else "⏸ Pausado"
                        st.metric("Status", status_text)

                    # Obtener progreso
                    metrics = db.get_habit_metrics(habit["id"])

                    if metrics:
                        st.markdown("---")
                        st.markdown("**Progreso Actual:**")

                        prog_cols = st.columns(3)

                        with prog_cols[0]:
                            st.metric(
                                "Tiempo Invertido",
                                format_duration(metrics.get("total_minutes_invested", 0))
                            )

                        with prog_cols[1]:
                            st.metric(
                                "Sesiones Totales",
                                metrics.get("total_sessions", 0)
                            )

                        with prog_cols[2]:
                            completion = metrics.get("completion_percentage", 0)
                            st.metric(
                                "Completado",
                                f"{completion:.1f}%"
                            )

                        # Barra de progreso
                        st.progress(min(100, completion) / 100)

                with col2:
                    st.markdown("**Acciones:**")

                    # Editar
                    if st.button(
                        "✏️ Editar",
                        key=f"edit_{habit['id']}",
                        width='stretch'
                    ):
                        st.session_state[f"editing_{habit['id']}"] = True

                    # Pausar/Activar
                    if habit["is_active"]:
                        if st.button(
                            "⏸️ Pausar",
                            key=f"pause_{habit['id']}",
                            width='stretch'
                        ):
                            if db.update_habit(habit["id"], {"is_active": False}):
                                st.success("✅ Hábito pausado")
                                time.sleep(1)
                                st.rerun()
                    else:
                        if st.button(
                            "▶️ Activar",
                            key=f"activate_{habit['id']}",
                            width='stretch'
                        ):
                            if db.update_habit(habit["id"], {"is_active": True}):
                                st.success("✅ Hábito activado")
                                time.sleep(1)
                                st.rerun()

                    # Eliminar
                    if st.button(
                        "🗑️ Eliminar",
                        key=f"delete_{habit['id']}",
                        width='stretch',
                        type="secondary"
                    ):
                        st.session_state[f"confirm_delete_{habit['id']}"] = True

                # Confirmación de eliminación
                if st.session_state.get(f"confirm_delete_{habit['id']}", False):
                    st.warning("⚠️ ¿Estás seguro de eliminar este hábito?")

                    col_a, col_b = st.columns(2)

                    with col_a:
                        if st.button(
                            "✅ Sí, eliminar",
                            key=f"confirm_yes_{habit['id']}"
                        ):
                            if db.delete_habit(habit["id"]):
                                st.success("✅ Hábito eliminado")
                                st.session_state[f"confirm_delete_{habit['id']}"] = False
                                time.sleep(1)
                                st.rerun()

                    with col_b:
                        if st.button(
                            "❌ Cancelar",
                            key=f"confirm_no_{habit['id']}"
                        ):
                            st.session_state[f"confirm_delete_{habit['id']}"] = False
                            st.rerun()

                # Formulario de edición
                if st.session_state.get(f"editing_{habit['id']}", False):
                    st.markdown("---")
                    st.markdown("**Editar Hábito:**")

                    with st.form(f"edit_form_{habit['id']}"):
                        new_name = st.text_input("Nombre", value=habit["name"])
                        new_desc = st.text_area("Descripción", value=habit.get("description", ""))

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            new_target = st.number_input(
                                "Target semanal (min)",
                                value=habit["target_minutes_per_week"],
                                min_value=30
                            )

                        with col2:
                            new_max = st.number_input(
                                "Máximo semanal (min)",
                                value=habit["max_minutes_per_week"],
                                min_value=60
                            )

                        with col3:
                            new_goal = st.number_input(
                                "Objetivo total (h)",
                                value=habit["total_hours_goal"],
                                min_value=10
                            )

                        col_save, col_cancel = st.columns(2)

                        with col_save:
                            submit_edit = st.form_submit_button(
                                "💾 Guardar Cambios",
                                width='stretch'
                            )

                        if submit_edit:
                            updates = {
                                "name": new_name,
                                "description": new_desc,
                                "target_minutes_per_week": new_target,
                                "max_minutes_per_week": new_max,
                                "total_hours_goal": new_goal
                            }

                            if db.update_habit(habit["id"], updates):
                                st.success("✅ Hábito actualizado")
                                st.session_state[f"editing_{habit['id']}"] = False
                                time.sleep(1)
                                st.rerun()

                    if st.button(
                        "❌ Cancelar Edición",
                        key=f"cancel_edit_{habit['id']}"
                    ):
                        st.session_state[f"editing_{habit['id']}"] = False
                        st.rerun()

# Botón de volver
st.markdown("---")
if st.button("🏠 Volver a Inicio"):
    st.switch_page("main.py")
