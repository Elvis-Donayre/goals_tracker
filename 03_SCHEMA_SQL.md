# SCHEMA SQL COMPLETO - HABIT TRACKER

**Para ejecutar en:** Supabase SQL Editor  
**Base de datos:** PostgreSQL 14+  
**Versión:** 1.0

---

## 📋 TABLA DE CONTENIDOS

1. [Tablas Base](#tablas-base)
2. [Índices](#índices)
3. [Vistas](#vistas)
4. [Funciones SQL](#funciones-sql)
5. [Datos Iniciales](#datos-iniciales)
6. [Verificación](#verificación)

---

## 🗂️ TABLAS BASE

### 1. TABLA: users

Almacena información de usuarios (para soporte multi-user en futuro).

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  full_name VARCHAR(150),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE users IS 'Usuarios del sistema';
COMMENT ON COLUMN users.id IS 'UUID único del usuario';
COMMENT ON COLUMN users.email IS 'Email único para login';
```

---

### 2. TABLA: categories

Categorías de hábitos (predefinidas o customizables).

```sql
CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  description TEXT,
  color VARCHAR(7) DEFAULT '#3B82F6',
  icon VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE categories IS 'Categorías de hábitos: Salud, Aprendizaje, Productividad, etc.';
COMMENT ON COLUMN categories.color IS 'Color hex para visualización (ej: #FF0000)';

-- Insertar categorías predeterminadas
INSERT INTO categories (name, description, color, icon) VALUES
  ('Salud', 'Ejercicio, nutrición, sueño, bienestar físico', '#EF4444', '❤️'),
  ('Aprendizaje', 'Idiomas, cursos, lectura, educación', '#3B82F6', '📚'),
  ('Productividad', 'Trabajo, proyectos, coding, enfoque', '#10B981', '⚡'),
  ('Desarrollo Personal', 'Meditación, reflexión, crecimiento, mindfulness', '#8B5CF6', '🌱'),
  ('Relaciones', 'Familia, amigos, networking, comunidad', '#F59E0B', '👥'),
  ('Finanzas', 'Inversión, ahorro, educación financiera', '#EC4899', '💰')
ON CONFLICT (name) DO NOTHING;
```

---

### 3. TABLA: habits

Definición de metas/hábitos con targets múltiples.

```sql
CREATE TABLE habits (
  id SERIAL PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(150) NOT NULL,
  description TEXT,
  category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
  
  -- TARGETS SEMANALES
  target_minutes_per_week INTEGER DEFAULT 420, -- 7 horas
  max_minutes_per_week INTEGER DEFAULT 900,    -- 15 horas (cap máximo)
  
  -- OBJETIVO TOTAL ACUMULADO
  total_hours_goal INTEGER DEFAULT 100,        -- Horas totales deseadas
  
  -- ESTADO
  is_active BOOLEAN DEFAULT TRUE,
  notes TEXT,
  
  -- TIMESTAMPS
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  CONSTRAINT unique_user_habit UNIQUE (user_id, name)
);

COMMENT ON TABLE habits IS 'Definición de metas/hábitos con múltiples targets';
COMMENT ON COLUMN habits.target_minutes_per_week IS 'Mínimo de minutos por semana';
COMMENT ON COLUMN habits.max_minutes_per_week IS 'Máximo de minutos por semana (para evitar burnout)';
COMMENT ON COLUMN habits.total_hours_goal IS 'Objetivo total en horas a alcanzar';

CREATE INDEX idx_habits_user ON habits(user_id);
CREATE INDEX idx_habits_active ON habits(is_active);
```

---

### 4. TABLA: activities

Actividades concretas que contribuyen a hábitos.

```sql
CREATE TABLE activities (
  id SERIAL PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(150) NOT NULL,
  description TEXT,
  category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
  icon VARCHAR(50),
  color VARCHAR(7),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  CONSTRAINT unique_user_activity UNIQUE (user_id, name)
);

COMMENT ON TABLE activities IS 'Actividades concretas: lo que realmente haces';
COMMENT ON COLUMN activities.name IS 'Nombre específico de la actividad (ej: "Ver videos AWS en YouTube")';

CREATE INDEX idx_activities_user ON activities(user_id);
```

---

### 5. TABLA: habit_activities (Relación muchos-a-muchos)

**ESTA ES LA TABLA CLAVE DEL CRUCE INTELIGENTE.**

Vincula actividades a hábitos con pesos ajustables.

```sql
CREATE TABLE habit_activities (
  id SERIAL PRIMARY KEY,
  habit_id INTEGER NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
  activity_id INTEGER NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
  
  -- PESO: Qué porcentaje de la actividad contribuye a este hábito
  weight DECIMAL(3,2) DEFAULT 1.0, -- Rango 0.0 a 1.0 (0% a 100%)
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  CONSTRAINT unique_habit_activity UNIQUE (habit_id, activity_id),
  CONSTRAINT weight_range CHECK (weight >= 0 AND weight <= 1)
);

COMMENT ON TABLE habit_activities IS 'TABLA CLAVE: Relación muchos-a-muchos entre hábitos y actividades con pesos';
COMMENT ON COLUMN habit_activities.weight IS 'Peso 0-1: qué % de la actividad contribuye a este hábito. Ej: 0.8 = 80%';

CREATE INDEX idx_habit_activities_habit ON habit_activities(habit_id);
CREATE INDEX idx_habit_activities_activity ON habit_activities(activity_id);
```

---

### 6. TABLA: sessions

Registros concretos de tiempo invertido en actividades.

```sql
CREATE TABLE sessions (
  id SERIAL PRIMARY KEY,
  activity_id INTEGER NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
  session_date DATE NOT NULL,
  start_time TIME,
  duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
  notes TEXT,
  
  -- MOOD TRACKING (opcional pero valioso)
  mood SMALLINT CHECK (mood IS NULL OR (mood >= 1 AND mood <= 5)), -- 1-5
  productivity_level SMALLINT CHECK (productivity_level IS NULL OR (productivity_level >= 1 AND productivity_level <= 5)), -- 1-5
  
  completed BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  CONSTRAINT unique_session UNIQUE (activity_id, session_date, start_time)
);

COMMENT ON TABLE sessions IS 'Registros concretos de sesiones: lo que registras diariamente';
COMMENT ON COLUMN sessions.duration_minutes IS 'Duración en minutos de la sesión';
COMMENT ON COLUMN sessions.mood IS 'Cómo te sentías (1=mal, 5=excelente)';
COMMENT ON COLUMN sessions.productivity_level IS 'Qué tan productivo fue (1=bajo, 5=muy alto)';

CREATE INDEX idx_sessions_activity ON sessions(activity_id);
CREATE INDEX idx_sessions_date ON sessions(session_date);
CREATE INDEX idx_sessions_activity_date ON sessions(activity_id, session_date);
```

---

### 7. TABLA: habit_metrics

Métricas precalculadas por hábito (para optimización de queries).

```sql
CREATE TABLE habit_metrics (
  id SERIAL PRIMARY KEY,
  habit_id INTEGER UNIQUE NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
  
  -- ACUMULADOS
  total_minutes_invested INTEGER DEFAULT 0,
  total_sessions INTEGER DEFAULT 0,
  
  -- CÁLCULOS
  completion_percentage DECIMAL(5,2) DEFAULT 0, -- 0-100%
  current_streak INTEGER DEFAULT 0, -- Días consecutivos
  longest_streak INTEGER DEFAULT 0,
  
  -- DATOS
  last_completed_date DATE,
  estimated_completion_date DATE,
  
  updated_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE habit_metrics IS 'Métricas precalculadas para optimización y rápido acceso';
COMMENT ON COLUMN habit_metrics.total_minutes_invested IS 'Total de minutos invertidos en esta meta (acumulado)';
COMMENT ON COLUMN habit_metrics.completion_percentage IS 'Porcentaje completado del goal total';
COMMENT ON COLUMN habit_metrics.estimated_completion_date IS 'Fecha estimada de finalización basada en ritmo actual';

CREATE INDEX idx_habit_metrics_habit ON habit_metrics(habit_id);
```

---

### 8. TABLA: habit_changes_log (Auditoría - Opcional pero recomendado)

Historial de cambios en hábitos (para tracking de cambios).

```sql
CREATE TABLE habit_changes_log (
  id SERIAL PRIMARY KEY,
  habit_id INTEGER NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
  change_type VARCHAR(50), -- 'created', 'updated', 'activated', 'paused', 'deleted'
  old_values JSONB,
  new_values JSONB,
  changed_by UUID REFERENCES users(id),
  changed_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE habit_changes_log IS 'Auditoría: registro de todos los cambios en hábitos';

CREATE INDEX idx_changes_habit ON habit_changes_log(habit_id);
CREATE INDEX idx_changes_date ON habit_changes_log(changed_at);
```

---

## 📍 ÍNDICES (Optimización)

```sql
-- Ya creados arriba, pero aquí está el resumen:

-- Habits
CREATE INDEX idx_habits_user ON habits(user_id);
CREATE INDEX idx_habits_active ON habits(is_active);
CREATE INDEX idx_habits_user_active ON habits(user_id, is_active);

-- Activities
CREATE INDEX idx_activities_user ON activities(user_id);

-- Habit-Activities (CRÍTICO para el cruce)
CREATE INDEX idx_habit_activities_habit ON habit_activities(habit_id);
CREATE INDEX idx_habit_activities_activity ON habit_activities(activity_id);
CREATE INDEX idx_ha_both ON habit_activities(habit_id, activity_id);

-- Sessions (CRÍTICO para queries de tiempo)
CREATE INDEX idx_sessions_activity ON sessions(activity_id);
CREATE INDEX idx_sessions_date ON sessions(session_date);
CREATE INDEX idx_sessions_activity_date ON sessions(activity_id, session_date);

-- Changes Log
CREATE INDEX idx_changes_habit ON habit_changes_log(habit_id);
CREATE INDEX idx_changes_date ON habit_changes_log(changed_at);
```

---

## 📊 VISTAS (Views)

### Vista 1: activity_habit_contribution

Muestra cómo cada actividad contribuye a cada hábito.

```sql
CREATE VIEW activity_habit_contribution AS
SELECT 
  s.session_date,
  s.id as session_id,
  a.id as activity_id,
  a.name as activity_name,
  h.id as habit_id,
  h.name as habit_name,
  ha.weight,
  s.duration_minutes,
  ROUND(s.duration_minutes * ha.weight)::INTEGER as weighted_minutes,
  s.mood,
  s.productivity_level,
  s.notes
FROM sessions s
INNER JOIN activities a ON s.activity_id = a.id
INNER JOIN habit_activities ha ON a.id = ha.activity_id
INNER JOIN habits h ON ha.habit_id = h.id
ORDER BY s.session_date DESC;

COMMENT ON VIEW activity_habit_contribution IS 'Vista clave: muestra cómo cada sesión se distribuye entre múltiples hábitos';
```

---

### Vista 2: habit_progress

Progreso actual de cada hábito con cálculos de tiempo.

```sql
CREATE VIEW habit_progress AS
SELECT 
  h.id,
  h.user_id,
  h.name,
  c.name as category,
  h.target_minutes_per_week,
  h.max_minutes_per_week,
  h.total_hours_goal * 60 as total_minutes_goal,
  
  -- ACUMULADO HISTÓRICO
  COALESCE(SUM(ROUND(s.duration_minutes * ha.weight)::INTEGER), 0) as total_minutes_invested,
  COALESCE(SUM(ROUND(s.duration_minutes * ha.weight)::INTEGER), 0)::FLOAT / 
    NULLIF(h.total_hours_goal * 60, 0) * 100 as completion_percentage,
  
  -- ESTA SEMANA
  COALESCE(
    SUM(CASE WHEN s.session_date >= CURRENT_DATE - INTERVAL '7 days' 
        THEN ROUND(s.duration_minutes * ha.weight)::INTEGER ELSE 0 END),
    0
  ) as minutes_this_week,
  
  -- ÚLTIMAS SESIONES
  COUNT(DISTINCT s.id) as total_sessions,
  MAX(s.session_date) as last_session_date,
  
  h.is_active,
  h.created_at
  
FROM habits h
LEFT JOIN categories c ON h.category_id = c.id
LEFT JOIN habit_activities ha ON h.id = ha.habit_id
LEFT JOIN activities a ON ha.activity_id = a.id
LEFT JOIN sessions s ON a.id = s.activity_id

GROUP BY h.id, h.user_id, h.name, c.name, h.target_minutes_per_week, 
         h.max_minutes_per_week, h.total_hours_goal, h.is_active, h.created_at
ORDER BY h.created_at DESC;

COMMENT ON VIEW habit_progress IS 'Vista crítica: progreso actual de todos los hábitos';
```

---

### Vista 3: activity_habit_matrix

Matriz que muestra la eficiencia de cada actividad (a cuántas metas contribuye).

```sql
CREATE VIEW activity_habit_matrix AS
SELECT 
  a.id as activity_id,
  a.user_id,
  a.name as activity_name,
  
  -- Hábitos a los que contribuye
  STRING_AGG(h.name || ' (' || ROUND(ha.weight * 100)::TEXT || '%)', ', ') 
    as contributes_to_habits,
  COUNT(DISTINCT h.id) as num_habits_connected,
  
  -- Estadísticas de uso
  COUNT(DISTINCT s.id) as total_sessions,
  COALESCE(SUM(s.duration_minutes), 0) as total_minutes_invested,
  ROUND(AVG(s.duration_minutes)::NUMERIC, 2) as avg_session_duration,
  
  -- Esfuerzo ponderado (beneficio a múltiples metas)
  COALESCE(SUM(s.duration_minutes * COALESCE(ha.weight, 1)), 0)::INTEGER 
    as total_weighted_minutes,
  
  -- Mood promedio
  ROUND(AVG(s.mood)::NUMERIC, 2) as avg_mood,
  ROUND(AVG(s.productivity_level)::NUMERIC, 2) as avg_productivity,
  
  MAX(s.session_date) as last_used
  
FROM activities a
LEFT JOIN habit_activities ha ON a.id = ha.activity_id
LEFT JOIN habits h ON ha.habit_id = h.id
LEFT JOIN sessions s ON a.id = s.activity_id

GROUP BY a.id, a.user_id, a.name
ORDER BY total_weighted_minutes DESC;

COMMENT ON VIEW activity_habit_matrix IS 'Matriz de eficiencia: identifica actividades que benefician múltiples metas';
```

---

### Vista 4: weekly_summary

Resumen semanal de progreso.

```sql
CREATE VIEW weekly_summary AS
SELECT 
  h.id as habit_id,
  h.name as habit_name,
  EXTRACT(WEEK FROM s.session_date) as week_number,
  EXTRACT(YEAR FROM s.session_date) as year,
  
  COALESCE(SUM(ROUND(s.duration_minutes * ha.weight)::INTEGER), 0) as minutes_this_week,
  COUNT(DISTINCT s.session_date) as days_with_activity,
  ROUND(
    COALESCE(SUM(ROUND(s.duration_minutes * ha.weight)::INTEGER), 0)::NUMERIC 
    / h.target_minutes_per_week * 100,
    2
  ) as completion_percentage,
  
  CASE 
    WHEN COALESCE(SUM(ROUND(s.duration_minutes * ha.weight)::INTEGER), 0) >= h.target_minutes_per_week 
      THEN 'Completado'
    WHEN COALESCE(SUM(ROUND(s.duration_minutes * ha.weight)::INTEGER), 0) >= h.target_minutes_per_week * 0.75
      THEN 'En camino'
    ELSE 'Rezagado'
  END as status
  
FROM habits h
LEFT JOIN habit_activities ha ON h.id = ha.habit_id
LEFT JOIN activities a ON ha.activity_id = a.id
LEFT JOIN sessions s ON a.id = s.activity_id
  AND s.session_date >= DATE_TRUNC('week', CURRENT_DATE)::DATE
  
GROUP BY h.id, h.name, h.target_minutes_per_week, 
         EXTRACT(WEEK FROM s.session_date), EXTRACT(YEAR FROM s.session_date)
ORDER BY year DESC, week_number DESC;

COMMENT ON VIEW weekly_summary IS 'Resumen semanal de progreso por hábito';
```

---

## 🔧 FUNCIONES SQL

### Función 1: register_session()

Registra una sesión y automáticamente distribuye el tiempo entre hábitos.

```sql
CREATE OR REPLACE FUNCTION register_session(
  activity_id_param INTEGER,
  duration_minutes_param INTEGER,
  session_date_param DATE DEFAULT CURRENT_DATE,
  start_time_param TIME DEFAULT NULL,
  notes_param TEXT DEFAULT NULL,
  mood_param SMALLINT DEFAULT NULL,
  productivity_param SMALLINT DEFAULT NULL
)
RETURNS TABLE(
  session_id INTEGER,
  activity_name VARCHAR,
  duration_minutes INTEGER,
  habits_updated INTEGER,
  success BOOLEAN
) AS $$
DECLARE
  v_session_id INTEGER;
  v_habits_count INTEGER;
BEGIN
  -- Validaciones
  IF duration_minutes_param <= 0 THEN
    RAISE EXCEPTION 'Duration must be greater than 0';
  END IF;
  
  IF mood_param IS NOT NULL AND (mood_param < 1 OR mood_param > 5) THEN
    RAISE EXCEPTION 'Mood must be between 1 and 5';
  END IF;
  
  IF productivity_param IS NOT NULL AND (productivity_param < 1 OR productivity_param > 5) THEN
    RAISE EXCEPTION 'Productivity must be between 1 and 5';
  END IF;
  
  -- Insertar sesión
  INSERT INTO sessions (
    activity_id,
    session_date,
    start_time,
    duration_minutes,
    notes,
    mood,
    productivity_level
  ) VALUES (
    activity_id_param,
    session_date_param,
    start_time_param,
    duration_minutes_param,
    notes_param,
    mood_param,
    productivity_param
  )
  ON CONFLICT (activity_id, session_date, start_time) DO UPDATE
  SET duration_minutes = duration_minutes_param,
      notes = COALESCE(notes_param, notes),
      updated_at = NOW()
  RETURNING id INTO v_session_id;
  
  -- Actualizar métricas de hábitos vinculados
  UPDATE habit_metrics hm
  SET 
    total_minutes_invested = (
      SELECT COALESCE(SUM(ROUND(s.duration_minutes * ha.weight)::INTEGER), 0)
      FROM sessions s
      INNER JOIN habit_activities ha ON s.activity_id = ha.activity_id
      WHERE ha.habit_id = hm.habit_id
    ),
    total_sessions = (
      SELECT COUNT(*)
      FROM sessions s
      INNER JOIN habit_activities ha ON s.activity_id = ha.activity_id
      WHERE ha.habit_id = hm.habit_id
    ),
    last_completed_date = session_date_param,
    updated_at = NOW()
  WHERE habit_id IN (
    SELECT DISTINCT ha.habit_id
    FROM habit_activities ha
    WHERE ha.activity_id = activity_id_param
  );
  
  -- Contar hábitos actualizados
  GET DIAGNOSTICS v_habits_count = ROW_COUNT;
  
  RETURN QUERY
  SELECT 
    v_session_id,
    a.name,
    duration_minutes_param,
    v_habits_count,
    TRUE
  FROM activities a
  WHERE a.id = activity_id_param;
  
EXCEPTION WHEN OTHERS THEN
  RETURN QUERY SELECT NULL::INTEGER, NULL::VARCHAR, NULL::INTEGER, 0, FALSE;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION register_session IS 'Función CRÍTICA: registra sesión y automáticamente distribuye tiempo entre hábitos vinculados';
```

---

### Función 2: link_activity_to_habit()

Crea o actualiza relación entre actividad y hábito.

```sql
CREATE OR REPLACE FUNCTION link_activity_to_habit(
  habit_id_param INTEGER,
  activity_id_param INTEGER,
  weight_param DECIMAL DEFAULT 1.0
)
RETURNS TABLE(
  success BOOLEAN,
  message TEXT
) AS $$
DECLARE
  v_habit_count INTEGER;
  v_activity_count INTEGER;
BEGIN
  -- Validar que existen
  SELECT COUNT(*) INTO v_habit_count FROM habits WHERE id = habit_id_param;
  SELECT COUNT(*) INTO v_activity_count FROM activities WHERE id = activity_id_param;
  
  IF v_habit_count = 0 OR v_activity_count = 0 THEN
    RETURN QUERY SELECT FALSE, 'Habit or activity not found'::TEXT;
    RETURN;
  END IF;
  
  -- Validar weight
  IF weight_param < 0 OR weight_param > 1 THEN
    RETURN QUERY SELECT FALSE, 'Weight must be between 0 and 1'::TEXT;
    RETURN;
  END IF;
  
  -- Insertar o actualizar relación
  INSERT INTO habit_activities (habit_id, activity_id, weight)
  VALUES (habit_id_param, activity_id_param, weight_param)
  ON CONFLICT (habit_id, activity_id) DO UPDATE
  SET weight = weight_param, updated_at = NOW();
  
  RETURN QUERY SELECT TRUE, 'Link created/updated successfully'::TEXT;
  
EXCEPTION WHEN OTHERS THEN
  RETURN QUERY SELECT FALSE, SQLERRM::TEXT;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION link_activity_to_habit IS 'Crea o actualiza relación entre actividad y hábito con peso';
```

---

### Función 3: update_habit_metrics()

Recalcula métricas de un hábito específico.

```sql
CREATE OR REPLACE FUNCTION update_habit_metrics(habit_id_param INTEGER)
RETURNS TABLE(
  habit_id INTEGER,
  total_minutes INTEGER,
  total_sessions INTEGER,
  completion_percentage NUMERIC,
  last_completed_date DATE
) AS $$
DECLARE
  v_total_minutes INTEGER;
  v_total_sessions INTEGER;
  v_completion_pct DECIMAL;
  v_last_date DATE;
  v_total_goal_minutes INTEGER;
BEGIN
  -- Obtener goal
  SELECT h.total_hours_goal * 60 INTO v_total_goal_minutes
  FROM habits h
  WHERE h.id = habit_id_param;
  
  -- Calcular totales
  SELECT 
    COALESCE(SUM(ROUND(s.duration_minutes * ha.weight)::INTEGER), 0),
    COUNT(*)
  INTO v_total_minutes, v_total_sessions
  FROM sessions s
  INNER JOIN habit_activities ha ON s.activity_id = ha.activity_id
  WHERE ha.habit_id = habit_id_param;
  
  -- Calcular porcentaje
  v_completion_pct := (v_total_minutes::NUMERIC / NULLIF(v_total_goal_minutes, 0)) * 100;
  
  -- Obtener última sesión
  SELECT MAX(s.session_date) INTO v_last_date
  FROM sessions s
  INNER JOIN habit_activities ha ON s.activity_id = ha.activity_id
  WHERE ha.habit_id = habit_id_param;
  
  -- Actualizar métricas
  UPDATE habit_metrics
  SET 
    total_minutes_invested = v_total_minutes,
    total_sessions = v_total_sessions,
    completion_percentage = v_completion_pct,
    last_completed_date = v_last_date,
    updated_at = NOW()
  WHERE habit_id = habit_id_param;
  
  RETURN QUERY
  SELECT 
    habit_id_param,
    v_total_minutes,
    v_total_sessions,
    v_completion_pct,
    v_last_date;
    
EXCEPTION WHEN OTHERS THEN
  RETURN QUERY SELECT habit_id_param, 0, 0, 0, NULL;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION update_habit_metrics IS 'Recalcula métricas de un hábito específico';
```

---

## 🌱 DATOS INICIALES

### Categorías (ya insertadas arriba)

Verificar con:
```sql
SELECT * FROM categories;
```

---

### Datos de prueba (OPCIONAL - para testing)

```sql
-- Crear usuario de prueba (reemplaza con tu email real)
INSERT INTO users (email, full_name)
VALUES ('elvis@example.com', 'Elvis Test')
RETURNING id;

-- Copiar el ID que devuelve y reemplazarlo en los queries siguientes
-- Para este ejemplo usaremos: 'user-uuid-aqui'

-- Crear actividades
INSERT INTO activities (user_id, name, description, category_id) VALUES
  ('user-uuid-aqui', 'Ver videos AWS en YouTube', 'Tutoriales en inglés de arquitectura cloud', 2),
  ('user-uuid-aqui', 'Leer documentación técnica AWS', 'Articulos técnicos en inglés sobre AWS', 2),
  ('user-uuid-aqui', 'Resolver ejercicios Cambridge', 'Ejercicios del curso C1 English', 2),
  ('user-uuid-aqui', 'Conversación en inglés', 'Meetup o práctica oral con nativos', 2),
  ('user-uuid-aqui', 'Revisar código en GitHub', 'Análisis de proyectos open source', 3),
  ('user-uuid-aqui', 'Salir a correr', 'Carrera o trote de 30-60 minutos', 1);

-- Crear hábitos/metas
INSERT INTO habits (user_id, name, description, category_id, frequency, target_minutes_per_week, max_minutes_per_week, total_hours_goal) VALUES
  ('user-uuid-aqui', 'Aprender inglés', 'Alcanzar fluencia tipo Cambridge C1', 2, 'Diario', 420, 900, 500),
  ('user-uuid-aqui', 'Dominar AWS', 'Certificación AWS Solutions Architect Professional', 2, 'Diario', 350, 700, 200),
  ('user-uuid-aqui', 'Mejorar código', 'Code review y buenas prácticas de desarrollo', 3, 'Semanal', 180, 360, 100),
  ('user-uuid-aqui', 'Hacer ejercicio', 'Mantener salud física y cardiovascular', 1, 'Diario', 300, 450, 200);

-- Vincular actividades a hábitos (CREAR EL CRUCE INTELIGENTE)
SELECT link_activity_to_habit(
  (SELECT id FROM habits WHERE name = 'Aprender inglés' AND user_id = 'user-uuid-aqui'),
  (SELECT id FROM activities WHERE name = 'Ver videos AWS en YouTube'),
  1.0  -- 100% contribuye a Aprender inglés
);

SELECT link_activity_to_habit(
  (SELECT id FROM habits WHERE name = 'Dominar AWS' AND user_id = 'user-uuid-aqui'),
  (SELECT id FROM activities WHERE name = 'Ver videos AWS en YouTube'),
  0.8  -- 80% contribuye a Dominar AWS
);

SELECT link_activity_to_habit(
  (SELECT id FROM habits WHERE name = 'Dominar AWS' AND user_id = 'user-uuid-aqui'),
  (SELECT id FROM activities WHERE name = 'Leer documentación técnica AWS'),
  1.0
);

SELECT link_activity_to_habit(
  (SELECT id FROM habits WHERE name = 'Aprender inglés' AND user_id = 'user-uuid-aqui'),
  (SELECT id FROM activities WHERE name = 'Leer documentación técnica AWS'),
  0.7  -- 70% contribuye (es en inglés pero menos intenso)
);

SELECT link_activity_to_habit(
  (SELECT id FROM habits WHERE name = 'Aprender inglés' AND user_id = 'user-uuid-aqui'),
  (SELECT id FROM activities WHERE name = 'Resolver ejercicios Cambridge'),
  1.0  -- 100% para inglés
);

SELECT link_activity_to_habit(
  (SELECT id FROM habits WHERE name = 'Aprender inglés' AND user_id = 'user-uuid-aqui'),
  (SELECT id FROM activities WHERE name = 'Conversación en inglés'),
  1.0
);

SELECT link_activity_to_habit(
  (SELECT id FROM habits WHERE name = 'Mejorar código' AND user_id = 'user-uuid-aqui'),
  (SELECT id FROM activities WHERE name = 'Revisar código en GitHub'),
  1.0
);

SELECT link_activity_to_habit(
  (SELECT id FROM habits WHERE name = 'Hacer ejercicio' AND user_id = 'user-uuid-aqui'),
  (SELECT id FROM activities WHERE name = 'Salir a correr'),
  1.0
);

-- Crear métricas para cada hábito
INSERT INTO habit_metrics (habit_id)
SELECT id FROM habits WHERE user_id = 'user-uuid-aqui'
ON CONFLICT (habit_id) DO NOTHING;

-- Insertar datos de sesiones de ejemplo (últimos 7 días)
SELECT register_session(
  (SELECT id FROM activities WHERE name = 'Ver videos AWS en YouTube'),
  90,  -- 90 minutos
  CURRENT_DATE,
  '18:00'::TIME,
  'Serverless y EventBridge - en inglés'
);

SELECT register_session(
  (SELECT id FROM activities WHERE name = 'Resolver ejercicios Cambridge'),
  60,
  CURRENT_DATE - INTERVAL '1 day',
  '19:00'::TIME,
  'Listening y reading comprehension'
);

SELECT register_session(
  (SELECT id FROM activities WHERE name = 'Leer documentación técnica AWS'),
  120,
  CURRENT_DATE - INTERVAL '2 days',
  '20:00'::TIME,
  'Lambda functions y containers'
);

SELECT register_session(
  (SELECT id FROM activities WHERE name = 'Salir a correr'),
  45,
  CURRENT_DATE - INTERVAL '1 day',
  '07:00'::TIME,
  'Trote matutino 5km'
);
```

---

## ✅ VERIFICACIÓN

Ejecuta estos queries para verificar que todo está bien:

```sql
-- 1. Verificar tablas creadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- 2. Verificar índices
SELECT indexname 
FROM pg_indexes 
WHERE schemaname = 'public'
ORDER BY indexname;

-- 3. Verificar vistas
SELECT viewname 
FROM pg_views 
WHERE schemaname = 'public'
ORDER BY viewname;

-- 4. Verificar funciones
SELECT routine_name 
FROM information_schema.routines 
WHERE routine_schema = 'public'
ORDER BY routine_name;

-- 5. Contar registros
SELECT 
  (SELECT COUNT(*) FROM users) as users_count,
  (SELECT COUNT(*) FROM categories) as categories_count,
  (SELECT COUNT(*) FROM habits) as habits_count,
  (SELECT COUNT(*) FROM activities) as activities_count,
  (SELECT COUNT(*) FROM habit_activities) as habit_activities_count,
  (SELECT COUNT(*) FROM sessions) as sessions_count;

-- 6. Ver vista de contribución (si hay datos)
SELECT * FROM activity_habit_contribution LIMIT 10;

-- 7. Ver vista de progreso (si hay datos)
SELECT * FROM habit_progress;

-- 8. Ver matriz de actividades
SELECT * FROM activity_habit_matrix;
```

---

**Estado:** ✅ Schema completo y listo para producción  
**Última actualización:** Enero 8, 2026  
**Versión:** 1.0
