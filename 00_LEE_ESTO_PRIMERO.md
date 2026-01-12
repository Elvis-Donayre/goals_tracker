# 🎯 GUÍA DEFINITIVA - QUÉ ARCHIVO USAR EN CADA PASO

**Un documento único para no confundirse. Sigue esto y ya.**

---

## ⚡ SI TIENES 5 MINUTOS

```
Abre:  08_SUPABASE_RAPIDO.md

Sigue los 6 pasos.

Copia SQL de:  12_SQL_ACTUALIZADO.md

Ejecuta en Supabase.

FIN. Base de datos lista.
```

---

## ⏱️ SI TIENES 30 MINUTOS

```
1. LEE (15 min):
   01_RESUMEN_EJECUTIVO.md
   
   ¿Qué es el proyecto? Aquí lo sabes.

2. VE (10 min):
   05_MOCKUP_VISUAL.md
   
   ¿Cómo se ve? Aquí lo ves.

3. ENTIENDE CAMBIO (5 min):
   14_RESUMEN_CAMBIOS.md
   
   ¿Por qué metas personalizadas? Aquí entiendes.

FIN. Entiendes el proyecto completamente.
```

---

## 📋 LA RUTA PASO A PASO

### PASO 1: ENTENDER (1 hora)

**Lee EN ESTE ORDEN:**

1. `01_RESUMEN_EJECUTIVO.md` (15 min)
   → Qué es Habit Tracker
   
2. `05_MOCKUP_VISUAL.md` (15 min)
   → Cómo se ve
   
3. `06_AUTENTICACION_STREAMLIT.md` (15 min)
   → Cómo se loguean usuarios
   
4. `14_RESUMEN_CAMBIOS.md` (10 min)
   → Por qué metas personalizadas

**OTROS (opcional):**
- `00_INDICE_MAESTRO.md` - Si quieres roadmap general
- `habit_tracker_architecture.md` - Si quieres diagramas

**NO LEAS:**
- ❌ `03_SCHEMA_SQL.md` (es el viejo)
- ❌ `04_GUIA_STREAMLIT.md` (es el viejo)
- ❌ `09_RESUMEN_FINAL.md` (es navegación vieja)
- ❌ `10_COMPLETADO.md` (es resumen viejo)
- ❌ `11_CAMBIO_METAS_PERSONALIZADAS.md` (análisis largo)

---

### PASO 2: CREAR SUPABASE (20-30 minutos)

**Abre:**
`08_SUPABASE_RAPIDO.md`

**Sigue los 6 pasos:**

1. Ir a supabase.com
2. Crear cuenta
3. Crear proyecto "habit-tracker"
4. Abrir SQL Editor
5. Copiar SQL de `12_SQL_ACTUALIZADO.md`
6. Ejecutar [▶ Run]

**Resultado:** Base de datos lista

**SI NECESITAS DETALLES:**
Abre: `07_CREAR_TABLAS_SUPABASE.md` (muy detallado)

**SI ALGO FALLA:**
Lee sección "Solucionar problemas" en `07_CREAR_TABLAS_SUPABASE.md`

---

### PASO 3: COPIAR CREDENCIALES (5 minutos)

**En Supabase:**
- Settings → API
- Copiar: Project URL
- Copiar: anon public key

**Crear en tu compu:**
```
archivo: .env

SUPABASE_URL = "https://..."
SUPABASE_KEY = "eyJ..."
```

---

### PASO 4: CREAR PROYECTO STREAMLIT (3-4 horas)

**Abre:**
`13_STREAMLIT_ACTUALIZADO.md`

**Sigue:**
- Copiar clase SupabaseDB
- Copiar main.py
- Copiar páginas Streamlit
- Adaptar a tu setup

**SOLO de aquí:**
- ✅ Métodos de SupabaseDB
- ✅ main.py con login
- ✅ Formulario crear hábitos
- ✅ Página registrar sesión

**NO de aquí:**
- ❌ `04_GUIA_STREAMLIT.md` (es versión vieja)

---

### PASO 5: AGREGAR GRÁFICOS (1-2 horas)

**Abre:**
`05_MOCKUP_VISUAL.md`

**Lee section "Analytics Avanzado"**

**Usa código de:**
`04_GUIA_STREAMLIT.md` (sí este, para gráficos Plotly)

---

### PASO 6: DEPLOY (1 hora)

**Push a GitHub:**
```
git add .
git commit -m "Habit Tracker"
git push
```

**En Streamlit Cloud:**
1. Conectar GitHub
2. Seleccionar repo
3. Configurar secrets (.env)
4. Deploy

**FIN. Tu app está LIVE 🚀**

---

## 📂 ARCHIVOS ÚTILES POR SITUACIÓN

### Situación: "Necesito crear la BD"

```
→ 08_SUPABASE_RAPIDO.md (6 pasos rápidos)
→ 12_SQL_ACTUALIZADO.md (el SQL a ejecutar)

Si necesitas detalles:
→ 07_CREAR_TABLAS_SUPABASE.md
```

### Situación: "Necesito entender el proyecto"

```
→ 01_RESUMEN_EJECUTIVO.md
→ 05_MOCKUP_VISUAL.md
→ 06_AUTENTICACION_STREAMLIT.md
→ 14_RESUMEN_CAMBIOS.md
```

### Situación: "Necesito el código"

```
→ 13_STREAMLIT_ACTUALIZADO.md (NUEVO - metas personalizadas)

Para gráficos:
→ 04_GUIA_STREAMLIT.md (sección de plotly)
```

### Situación: "Algo no funciona"

```
Si es Supabase:
→ 07_CREAR_TABLAS_SUPABASE.md (sección problemas)

Si es Streamlit:
→ 13_STREAMLIT_ACTUALIZADO.md (lee comentarios)

Si es login:
→ 06_AUTENTICACION_STREAMLIT.md
```

### Situación: "¿Qué cambió con metas personalizadas?"

```
→ 14_RESUMEN_CAMBIOS.md (resumen ejecutivo)
→ 11_CAMBIO_METAS_PERSONALIZADAS.md (análisis completo)
```

### Situación: "Quiero ver diagramas"

```
→ habit_tracker_architecture.md (10 diagramas)
→ 05_MOCKUP_VISUAL.md (mockups)
```

---

## ❌ ARCHIVOS QUE NO NECESITAS

| Archivo | Por qué |
|---------|---------|
| `03_SCHEMA_SQL.md` | Viejo (usa `12_SQL_ACTUALIZADO.md`) |
| `04_GUIA_STREAMLIT.md` | Viejo (usa `13_STREAMLIT_ACTUALIZADO.md`) |
| `09_RESUMEN_FINAL.md` | Navegación vieja |
| `10_COMPLETADO.md` | Resumen viejo |
| `11_CAMBIO_METAS_PERSONALIZADAS.md` | Demasiado largo (lee `14_RESUMEN_CAMBIOS.md`) |

---

## ✅ ARCHIVOS QUE SÍ NECESITAS

| Archivo | Cuándo |
|---------|--------|
| `08_SUPABASE_RAPIDO.md` | Crear BD (PRIMERO) |
| `12_SQL_ACTUALIZADO.md` | SQL a ejecutar (CON 08) |
| `13_STREAMLIT_ACTUALIZADO.md` | Código Streamlit (SEGUNDO) |
| `01_RESUMEN_EJECUTIVO.md` | Entender proyecto (OPCIONAL pero recomendado) |
| `05_MOCKUP_VISUAL.md` | Ver diseño (OPCIONAL) |
| `06_AUTENTICACION_STREAMLIT.md` | Entender login (OPCIONAL) |
| `07_CREAR_TABLAS_SUPABASE.md` | Si necesitas detalles |
| `14_RESUMEN_CAMBIOS.md` | Entender cambios |

---

## 🎯 ESCENARIOS

### Escenario 1: "Quiero empezar AHORA mismo"

```
1. Abre: 08_SUPABASE_RAPIDO.md
2. Ir a supabase.com
3. Crear proyecto
4. Copiar SQL de: 12_SQL_ACTUALIZADO.md
5. Ejecutar
6. ✅ BD lista
```

**Tiempo: 20 minutos**

---

### Escenario 2: "Quiero entender primero"

```
1. Lee: 01_RESUMEN_EJECUTIVO.md (15 min)
2. Ve: 05_MOCKUP_VISUAL.md (10 min)
3. Lee: 14_RESUMEN_CAMBIOS.md (5 min)
4. Ahora: Escenario 1
```

**Tiempo: 30 minutos lectura + 20 Supabase**

---

### Escenario 3: "Quiero hacerlo bien y completo"

```
DÍA 1: ENTENDER
├─ 01_RESUMEN_EJECUTIVO.md
├─ 05_MOCKUP_VISUAL.md
├─ 06_AUTENTICACION_STREAMLIT.md
└─ 14_RESUMEN_CAMBIOS.md
Tiempo: 1-2 horas

DÍA 2: CREAR BD
├─ 08_SUPABASE_RAPIDO.md
├─ 12_SQL_ACTUALIZADO.md (SQL)
└─ 07_CREAR_TABLAS_SUPABASE.md (si necesitas detalles)
Tiempo: 30 minutos

DÍA 3-4: STREAMLIT
├─ 13_STREAMLIT_ACTUALIZADO.md (copiar código)
├─ Crear proyecto local
├─ Adaptar a tu setup
└─ Probar
Tiempo: 3-4 horas

DÍA 5: GRÁFICOS Y PULIR
├─ 05_MOCKUP_VISUAL.md (referencia)
├─ 04_GUIA_STREAMLIT.md (gráficos Plotly)
└─ Pruebas
Tiempo: 1-2 horas

TOTAL: 4-5 días
```

---

## 🚀 LA RUTA RECOMENDADA

**Sigue ESTO y no te confundas:**

```
┌─────────────────────────────────────────────────┐
│ PASO 1: LEER (30 minutos)                       │
├─────────────────────────────────────────────────┤
│ 01_RESUMEN_EJECUTIVO.md                         │
│ 05_MOCKUP_VISUAL.md                             │
│ 14_RESUMEN_CAMBIOS.md                           │
└─────────────────────────────────────────────────┘
           ↓ (Ahora entiendes qué es)
┌─────────────────────────────────────────────────┐
│ PASO 2: CREAR BD (20 minutos)                   │
├─────────────────────────────────────────────────┤
│ 08_SUPABASE_RAPIDO.md                           │
│ 12_SQL_ACTUALIZADO.md (el SQL)                  │
└─────────────────────────────────────────────────┘
           ↓ (Ahora tienes BD)
┌─────────────────────────────────────────────────┐
│ PASO 3: STREAMLIT (3-4 horas)                   │
├─────────────────────────────────────────────────┤
│ 13_STREAMLIT_ACTUALIZADO.md                     │
│ Copiar código                                    │
│ Adaptar a tu setup                              │
└─────────────────────────────────────────────────┘
           ↓ (Ahora tienes app)
┌─────────────────────────────────────────────────┐
│ PASO 4: DEPLOY (1 hora)                         │
├─────────────────────────────────────────────────┤
│ Push a GitHub                                    │
│ Streamlit Cloud                                  │
└─────────────────────────────────────────────────┘
           ↓
      ✅ APP LISTA
```

---

## 📞 PREGUNTAS RÁPIDAS

| Pregunta | Respuesta |
|----------|----------|
| ¿Por dónde empiezo? | `08_SUPABASE_RAPIDO.md` |
| ¿Qué es esto? | `01_RESUMEN_EJECUTIVO.md` |
| ¿Cómo se ve? | `05_MOCKUP_VISUAL.md` |
| ¿Cuál SQL uso? | `12_SQL_ACTUALIZADO.md` |
| ¿Cuál código uso? | `13_STREAMLIT_ACTUALIZADO.md` |
| ¿Cómo se loguea? | `06_AUTENTICACION_STREAMLIT.md` |
| ¿Qué cambió? | `14_RESUMEN_CAMBIOS.md` |
| ¿Algo falla? | `07_CREAR_TABLAS_SUPABASE.md` |
| ¿Diagramas? | `habit_tracker_architecture.md` |

---

## ✨ RESUMEN: LOS 5 ARCHIVOS QUE REALMENTE NECESITAS

```
1. 01_RESUMEN_EJECUTIVO.md
   → Entender proyecto
   
2. 08_SUPABASE_RAPIDO.md
   → Crear BD en 5 pasos
   
3. 12_SQL_ACTUALIZADO.md
   → El SQL a ejecutar
   
4. 13_STREAMLIT_ACTUALIZADO.md
   → El código a copiar
   
5. 14_RESUMEN_CAMBIOS.md
   → Entender cambios

TODO LO DEMÁS: Extras/Referencia
```

---

## 🎯 PUNTO FINAL

**Lee esto (esta página) y OLVIDA el resto.**

Abre los archivos en este orden:
1. `01_RESUMEN_EJECUTIVO.md`
2. `08_SUPABASE_RAPIDO.md` + `12_SQL_ACTUALIZADO.md`
3. `13_STREAMLIT_ACTUALIZADO.md`
4. Deploy

**Ya.**

---

**Status:** ✅ Guía definitiva única  
**Versión:** 2.0 (Metas personalizadas)  
**Próximo:** Elige tu escenario arriba y comienza
