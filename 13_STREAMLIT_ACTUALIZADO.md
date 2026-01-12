# 🐍 CÓDIGO STREAMLIT ACTUALIZADO - HÁBITOS PERSONALIZADOS

**Código Python actualizado para crear hábitos completamente personalizados**

---

## 📝 CAMBIOS EN SupabaseDB

### Método actualizado: create_habit()

```python
def create_habit(
    self,
    user_id: str,
    name: str,
    target_minutes_per_week: int = 420,
    max_minutes_per_week: int = 900,
    total_hours_goal: int = 100,
    description: str = None,
    category_id: int = None
) -> dict:
    """
    NUEVO: Crear hábito PERSONALIZADO del usuario
    
    Args:
        user_id: ID del usuario
        name: Nombre exacto de la meta (usuario lo escribe)
        target_minutes_per_week: Mínimo deseado por semana
        max_minutes_per_week: Máximo para evitar burnout
        total_hours_goal: Objetivo total en horas
        description: Descripción opcional
        category_id: ID de categoría (OPCIONAL - puede ser None)
    
    Returns:
        dict con el hábito creado o None si error
        
    CAMBIO: Ahora permite cualquier nombre + categoría opcional
    """
    
    try:
        # Validar que el nombre no esté vacío
        if not name or not name.strip():
            print("Error: El nombre del hábito no puede estar vacío")
            return None
        
        # Crear el hábito
        response = self.supabase.table('habits').insert({
            'user_id': user_id,
            'name': name.strip(),
            'description': description.strip() if description else None,
            'category_id': category_id,  # Puede ser None
            'target_minutes_per_week': target_minutes_per_week,
            'max_minutes_per_week': max_minutes_per_week,
            'total_hours_goal': total_hours_goal,
            'is_active': True
        }).execute()
        
        if response.data:
            return response.data[0]
        
        return None
    
    except Exception as e:
        print(f"Error creando hábito: {e}")
        return None
```

### Nuevos métodos: Categorías personalizadas

```python
def create_user_category(
    self,
    user_id: str,
    name: str,
    color: str = '#3B82F6'
) -> dict:
    """
    NUEVO: Crear categoría personalizada para el usuario
    
    Args:
        user_id: ID del usuario
        name: Nombre de la categoría
        color: Color hexadecimal (default: azul)
    
    Returns:
        dict con la categoría creada o None
    """
    
    try:
        response = self.supabase.table('user_categories').insert({
            'user_id': user_id,
            'name': name.strip(),
            'color': color
        }).execute()
        
        if response.data:
            return response.data[0]
        
        return None
    
    except Exception as e:
        print(f"Error creando categoría: {e}")
        return None

def get_all_categories_for_user(self, user_id: str) -> list:
    """
    Obtener categorías predefinidas + personalizadas del usuario
    
    Returns:
        Lista con:
        - Categorías predefinidas (system)
        - Categorías del usuario (personal)
    """
    
    try:
        # Obtener categorías predefinidas
        predefined = self.supabase.table('categories').select('*').execute()
        
        # Obtener categorías personalizadas del usuario
        user_cats = self.supabase.table('user_categories').select('*').where(
            'user_id', 'eq', user_id
        ).execute()
        
        # Combinar
        result = []
        
        if predefined.data:
            for cat in predefined.data:
                result.append({
                    'id': cat['id'],
                    'name': cat['name'],
                    'type': 'system',  # Categoría predefinida
                    'color': cat['color']
                })
        
        if user_cats.data:
            for cat in user_cats.data:
                result.append({
                    'id': cat['id'],
                    'name': cat['name'],
                    'type': 'personal',  # Categoría personal
                    'color': cat['color']
                })
        
        return result
    
    except Exception as e:
        print(f"Error obteniendo categorías: {e}")
        return []
```

---

## 💻 INTERFAZ STREAMLIT ACTUALIZADA

### Opción A: main.py - Crear hábito personalizado

```python
# ============================================================================
# TAB: CREAR MI PROPIA META PERSONALIZADA
# ============================================================================

st.subheader("Crear tu Meta Personalizada")

# Opción de creación
opcion_creacion = st.radio(
    "¿Cómo quieres crear tu meta?",
    ["Escribir mi propia meta", "Ver sugerencias por categoría"],
    index=0
)

if opcion_creacion == "Escribir mi propia meta":
    
    # ────────────────────────────────────────────────────────────
    # OPCIÓN A: COMPLETAMENTE PERSONALIZADO
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
                # Obtener todas las categorías (predefinidas + personalizadas)
                todas_categorias = db.get_all_categories_for_user(user_id)
                
                if todas_categorias:
                    # Agrupar por tipo
                    cat_names = []
                    cat_map = {}  # Mapear nombre → id
                    
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
            
            with col2:
                if st.button("➕ Nueva", help="Crear una categoría personalizada"):
                    st.session_state.mostrar_crear_categoria = True
        
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
        
        # ✓ Estimación
        if target_weekly > 0:
            semanas_requeridas = (total_goal * 60) / target_weekly
            meses_aproximados = semanas_requeridas / 4.3
            fecha_estimada = (datetime.now() + timedelta(weeks=semanas_requeridas)).strftime("%B %Y")
            
            st.info(
                f"📈 Con **{target_weekly} min/semana**, completarás {total_goal}h en "
                f"~**{int(semanas_requeridas)} semanas** (**{fecha_estimada}**)"
            )
        
        st.markdown("---")
        
        # BOTÓN ENVÍO
        if st.form_submit_button(
            label="✅ Crear Meta",
            use_container_width=True,
            type="primary"
        ):
            if nombre_meta and nombre_meta.strip():
                # Crear el hábito
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
                    st.session_state.crear_habito_ok = True
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Error creando la meta. Intenta de nuevo.")
            else:
                st.error("❌ Debes ingresar un nombre para tu meta")

else:
    
    # ────────────────────────────────────────────────────────────
    # OPCIÓN B: SUGERENCIAS POR CATEGORÍA
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
    
    for i, sugerencia in enumerate(sugerencias[categoria_sugerencia]):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.write(f"• {sugerencia}")
        
        with col2:
            if st.button(
                label="Usar",
                key=f"btn_usar_sugerencia_{i}",
                help="Pre-llenar el formulario con esta sugerencia"
            ):
                st.session_state.nombre_meta_sugerencia = sugerencia
                st.info(f"✅ Usa esta en la opción 'Escribir mi propia meta'")

# ============================================================================
# CREAR CATEGORÍA PERSONALIZADA
# ============================================================================

if usar_categoria and st.session_state.get("mostrar_crear_categoria"):
    st.markdown("---")
    
    with st.expander("➕ Crear nueva categoría personalizada"):
        with st.form("crear_categoria_form"):
            nombre_cat = st.text_input(
                "Nombre de la categoría",
                placeholder="Ej: Mis Negocios, Aprendizaje XYZ",
                max_chars=100
            )
            
            color_cat = st.color_picker(
                "Color de la categoría",
                value="#3B82F6"
            )
            
            if st.form_submit_button("✅ Crear Categoría"):
                if nombre_cat:
                    new_cat = db.create_user_category(
                        user_id=user_id,
                        name=nombre_cat,
                        color=color_cat
                    )
                    
                    if new_cat:
                        st.success(f"✅ Categoría '{nombre_cat}' creada")
                        st.session_state.mostrar_crear_categoria = False
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Error creando categoría")
                else:
                    st.error("Ingresa un nombre")

# ============================================================================
# MOSTRAR HÁBITOS CREADOS
# ============================================================================

st.markdown("---")
st.subheader("Tus Metas Creadas")

habits = db.get_all_habits(user_id)

if len(habits) == 0:
    st.info("📝 Aún no has creado ninguna meta. ¡Crea la primera arriba!")
else:
    for idx, habit in habits.iterrows():
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"### 🎯 {habit['name']}")
                
                if habit.get('description'):
                    st.write(f"*{habit['description']}*")
                
                # Detalles
                metric_cols = st.columns(4)
                with metric_cols[0]:
                    st.metric(
                        "Target/semana",
                        f"{habit['target_minutes_per_week']}m"
                    )
                with metric_cols[1]:
                    st.metric(
                        "Máx/semana",
                        f"{habit['max_minutes_per_week']}m"
                    )
                with metric_cols[2]:
                    st.metric(
                        "Objetivo total",
                        f"{habit['total_hours_goal']}h"
                    )
                with metric_cols[3]:
                    st.metric(
                        "Status",
                        "✅ Activo" if habit.get('is_active') else "⏸ Pausado"
                    )
            
            with col2:
                if st.button(
                    "Editar",
                    key=f"edit_{habit['id']}"
                ):
                    st.info("Función de editar próximamente")
            
            st.markdown("---")
```

---

## 🔑 CAMBIOS CLAVE

### 1. Sin metas predefinidas

**Antes:**
```python
metas_predefinidas = ["Aprender inglés", "Dominar AWS"]
meta = st.selectbox("Elige meta", metas_predefinidas)
```

**Ahora:**
```python
nombre = st.text_input("¿Cuál es tu meta?", placeholder="Escribe lo que quieras")
```

### 2. Categorías opcionales

**Antes:**
```python
category_id = st.selectbox("Categoría", categorias)  # Obligatoria
```

**Ahora:**
```python
usar_categoria = st.checkbox("Quiero categorizar")
if usar_categoria:
    category_id = st.selectbox("Categoría", categorias)
else:
    category_id = None
```

### 3. Sugerencias como inspiración

```python
# No fuerzan, solo sugieren
sugerencias = {
    "Aprendizaje": ["Aprender italiano", "Estudiar Python"],
    "Salud": ["Meditar", "Ejercicio"]
}

# Usuario puede:
# - Usar una sugerencia
# - Escribir la suya propia
# - Ignorar y crear algo único
```

---

## ✨ RESULTADO

```
Usuario abre → Escribe EXACTAMENTE lo que quiere
            → Es su meta, 100% personalizada
            → Categoría opcional
            → Control completo

✅ Máxima flexibilidad
✅ Máximo engagement
✅ Cada usuario diferente
```

---

**Status:** Código actualizado  
**Versión:** 2.0 (Hábitos personalizados)  
**Próximo:** Desplegar y probar
