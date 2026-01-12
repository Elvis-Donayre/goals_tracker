"""
=============================================================================
GESTIÓN DE ACTIVIDADES Y VINCULACIÓN
=============================================================================
"""

import streamlit as st
import time
from utils.database import SupabaseDB
from utils.helpers import format_duration

st.set_page_config(
    page_title="Actividades - Habit Tracker",
    page_icon="⚡",
    layout="wide"
)

# Verificar autenticación
if not st.session_state.get("authenticated"):
    st.warning("⚠️ Debes iniciar sesión primero")
    st.stop()

db = SupabaseDB()
user_id = st.session_state.user_id

# Título
st.title("⚡ Gestión de Actividades")
st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs([
    "➕ Crear Actividad",
    "🔗 Vincular a Hábitos",
    "📋 Mis Actividades"
])

# ============================================================================
# TAB 1: CREAR ACTIVIDAD
# ============================================================================
with tab1:
    st.subheader("Nueva Actividad")

    with st.form("crear_actividad"):
        # Nombre
        nombre_actividad = st.text_input(
            "Nombre de la actividad",
            placeholder="Ej: Ver videos AWS en YouTube",
            help="Describe específicamente qué harás"
        )

        # Categoría (opcional)
        usar_categoria = st.checkbox("Asignar categoría (opcional)")

        category_id = None
        if usar_categoria:
            categorias = db.get_all_categories_for_user(user_id)

            if categorias:
                cat_options = {f"{c['name']}": c['id'] for c in categorias}
                cat_selected = st.selectbox("Categoría", list(cat_options.keys()))
                category_id = cat_options[cat_selected]

        # Descripción
        descripcion = st.text_area(
            "Descripción (opcional)",
            placeholder="Ej: Tutoriales en inglés de arquitectura cloud"
        )

        # Botón
        submit = st.form_submit_button(
            "✅ Crear Actividad",
            use_container_width=True,
            type="primary"
        )

        if submit:
            if not nombre_actividad or not nombre_actividad.strip():
                st.error("❌ Debes ingresar un nombre para la actividad")
            else:
                nueva_actividad = db.create_activity(
                    user_id=user_id,
                    name=nombre_actividad,
                    category_id=category_id,
                    description=descripcion if descripcion else None
                )

                if nueva_actividad:
                    st.success(f"✅ Actividad '{nombre_actividad}' creada!")
                    st.info(
                        "💡 **Próximo paso:** Ve a la pestaña '🔗 Vincular a Hábitos' "
                        "para conectar esta actividad con tus metas"
                    )
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Error creando actividad")

# ============================================================================
# TAB 2: VINCULAR A HÁBITOS (EL CRUCE INTELIGENTE)
# ============================================================================
with tab2:
    st.subheader("Vincular Actividades a Hábitos")

    st.info(
        "**El Cruce Inteligente:**\n\n"
        "Conecta cada actividad con uno o más hábitos usando **pesos** (0.0 a 1.0)\n\n"
        "- **1.0 (100%)**: La actividad contribuye completamente a este hábito\n"
        "- **0.5 (50%)**: Contribuye parcialmente\n\n"
        "**Ejemplo:** 'Ver videos AWS' → 100% a 'Aprender inglés' + 80% a 'Dominar AWS'"
    )

    # Obtener actividades y hábitos
    activities = db.get_user_activities(user_id)
    habits = db.get_user_habits(user_id)

    if activities.empty:
        st.warning("⚠️ No tienes actividades creadas. Ve a la pestaña '➕ Crear Actividad'")
    elif habits.empty:
        st.warning("⚠️ No tienes hábitos creados. Ve a '🎯 Mis Hábitos'")
    else:
        # Selector de actividad
        activity_names = {row['name']: row['id'] for _, row in activities.iterrows()}
        selected_activity_name = st.selectbox(
            "Selecciona una actividad",
            list(activity_names.keys())
        )

        selected_activity_id = activity_names[selected_activity_name]

        st.markdown("---")

        # Obtener vínculos existentes
        existing_links = db.get_activity_links(selected_activity_id)
        existing_habit_ids = []

        if not existing_links.empty:
            existing_habit_ids = [
                link.get('habit_id') or link.get('habits', {}).get('id')
                for _, link in existing_links.iterrows()
            ]

        st.markdown("### ¿A cuáles hábitos contribuye esta actividad?")

        # Formulario de vinculación
        with st.form("vincular_form"):
            links_to_create = []

            for _, habit in habits.iterrows():
                st.markdown(f"**{habit['name']}**")

                col1, col2 = st.columns([1, 2])

                with col1:
                    is_linked = habit['id'] in existing_habit_ids

                    vincular = st.checkbox(
                        "Vincular",
                        value=is_linked,
                        key=f"link_{habit['id']}"
                    )

                with col2:
                    if vincular:
                        # Obtener peso actual si existe
                        current_weight = 1.0

                        if not existing_links.empty:
                            link_row = existing_links[
                                (existing_links['habit_id'] == habit['id']) |
                                (existing_links.get('habits', {}).get('id') == habit['id'])
                            ]

                            if not link_row.empty:
                                current_weight = link_row.iloc[0].get('weight', 1.0)

                        weight = st.slider(
                            "Peso de contribución",
                            min_value=0.0,
                            max_value=1.0,
                            value=float(current_weight),
                            step=0.1,
                            format="%.1f",
                            key=f"weight_{habit['id']}",
                            help=f"1.0 = 100% contribuye | 0.5 = 50% contribuye"
                        )

                        links_to_create.append({
                            "habit_id": habit['id'],
                            "weight": weight,
                            "habit_name": habit['name']
                        })

                st.markdown("---")

            # Botón guardar
            submit = st.form_submit_button(
                "💾 Guardar Vínculos",
                use_container_width=True,
                type="primary"
            )

            if submit:
                with st.spinner("Guardando vínculos..."):
                    # Eliminar vínculos viejos que ya no están
                    for habit_id in existing_habit_ids:
                        if habit_id not in [l['habit_id'] for l in links_to_create]:
                            db.unlink_activity_from_habit(habit_id, selected_activity_id)

                    # Crear/actualizar nuevos vínculos
                    for link in links_to_create:
                        db.link_activity_to_habit(
                            habit_id=link['habit_id'],
                            activity_id=selected_activity_id,
                            weight=link['weight']
                        )

                    st.success("✅ Vínculos guardados!")

                    # Mostrar resultado
                    if links_to_create:
                        st.info(
                            f"**'{selected_activity_name}' ahora contribuye a:**\n\n" +
                            "\n".join([
                                f"- {link['habit_name']}: {link['weight']*100:.0f}%"
                                for link in links_to_create
                            ])
                        )

                    time.sleep(2)
                    st.rerun()

# ============================================================================
# TAB 3: MIS ACTIVIDADES
# ============================================================================
with tab3:
    st.subheader("Tus Actividades")

    activities = db.get_user_activities(user_id)

    if activities.empty:
        st.info("📝 No tienes actividades creadas. ¡Crea la primera en la pestaña '➕ Crear Actividad'!")
    else:
        # Obtener matriz de actividades
        matrix = db.get_habit_activities_matrix(user_id)

        for _, activity in activities.iterrows():
            with st.expander(f"⚡ {activity['name']}", expanded=False):
                col1, col2 = st.columns([3, 1])

                with col1:
                    # Descripción
                    if activity.get("description"):
                        st.write(f"*{activity['description']}*")

                    # Obtener estadísticas de la matriz
                    if not matrix.empty:
                        activity_stats = matrix[matrix['id'] == activity['id']]

                        if not activity_stats.empty:
                            stats = activity_stats.iloc[0]

                            metric_cols = st.columns(3)

                            with metric_cols[0]:
                                st.metric(
                                    "Hábitos vinculados",
                                    stats.get("number_of_habits", 0)
                                )

                            with metric_cols[1]:
                                st.metric(
                                    "Sesiones totales",
                                    stats.get("total_sessions", 0)
                                )

                            with metric_cols[2]:
                                total_min = stats.get("total_minutes", 0)
                                st.metric(
                                    "Tiempo total",
                                    format_duration(int(total_min)) if total_min else "0m"
                                )

                            # Mostrar hábitos beneficiados
                            if stats.get("benefited_habits"):
                                st.success(
                                    f"**Beneficia:** {stats['benefited_habits']}"
                                )

                with col2:
                    st.markdown("**Acciones:**")

                    # Editar
                    if st.button(
                        "✏️ Editar",
                        key=f"edit_act_{activity['id']}",
                        use_container_width=True
                    ):
                        st.session_state[f"editing_act_{activity['id']}"] = True

                    # Eliminar
                    if st.button(
                        "🗑️ Eliminar",
                        key=f"delete_act_{activity['id']}",
                        use_container_width=True
                    ):
                        if st.session_state.get(f"confirm_delete_act_{activity['id']}", False):
                            if db.delete_activity(activity['id']):
                                st.success("✅ Actividad eliminada")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.session_state[f"confirm_delete_act_{activity['id']}"] = True

# Botón de volver
st.markdown("---")
if st.button("🏠 Volver a Inicio"):
    st.switch_page("main.py")
