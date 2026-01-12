# ⚡ SUPABASE EN 5 MINUTOS - VERSIÓN RÁPIDA

**Si tienes prisa, aquí está el resumen visual super simple**

---

## 🎯 LOS 6 PASOS

### 1️⃣ CREAR CUENTA

```
Ir a: https://supabase.com

[Get Started]
  ↓
Ingresar email
  ↓
Confirmar en email recibido
  ↓
✅ Logueado
```

### 2️⃣ CREAR PROYECTO

```
[+ Create new project]
  ↓
Project Name: habit-tracker
Plan: Free (gratuito)
  ↓
[Create project]
  ↓
⏳ Esperando 1-2 minutos
  ↓
✅ Proyecto listo
```

### 3️⃣ ABRIR SQL EDITOR

```
Dashboard del proyecto
  ↓
Left sidebar → [SQL Editor]
  ↓
Verás área vacía para escribir SQL
```

### 4️⃣ COPIAR Y EJECUTAR TODO EL SQL

**De dónde copiar:**

Archivo que ya tienes: `03_SCHEMA_SQL.md`

**Qué copiar:**

Desde esta línea:
```sql
CREATE TABLE users (
```

Hasta la última línea que tenga `;`

**Dónde pegarlo:**

En el área de texto del SQL Editor de Supabase

**Cómo ejecutar:**

Presiona: [▶ Run] (botón arriba a la derecha)

**Resultado que verás:**

```
✅ Success!
Query completed successfully
```

### 5️⃣ VERIFICAR TABLAS

```
Left sidebar → [Table Editor]
  ↓
Verás lista de tablas:
  ├─ users
  ├─ categories (con datos)
  ├─ habits
  ├─ activities
  ├─ habit_activities
  ├─ sessions
  ├─ habit_metrics
  └─ habit_changes_log
  ↓
✅ Todas creadas correctamente
```

### 6️⃣ COPIAR CREDENCIALES

```
Top derecha: [⚙️ Settings]
  ↓
Left sidebar → [API]
  ↓
Verás dos campos importantes:

1. Project URL:
   https://xxxxxxxx.supabase.co
   [Copy]

2. anon public key:
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   [Copy]

  ↓
Crear archivo .env local:

SUPABASE_URL = "https://xxxxxxxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

  ↓
✅ Listo para conectar desde Streamlit
```

---

## 📹 VERSIÓN "PASO A PASO CON CLICKS"

Si quieres ver exactamente dónde hacer click:

### En Supabase (Primera vez)

```
1. Abrir navegador
2. Ir a: https://supabase.com
3. Botón grande "Get Started" → CLICK
4. Ingresar email y contraseña
5. Click en [Create account]
6. Esperar email de verificación
7. Click en enlace de confirmación
8. LISTO: Estás logueado en dashboard
```

### Crear proyecto

```
1. Dashboard → [+ Create new project]
2. Nombre: "habit-tracker"
3. Plan: "Free" (gratuito)
4. Click [Create project]
5. ⏳ ESPERAR 1-2 MINUTOS
6. ✅ Proyecto creado
```

### Crear tablas (LO MÁS IMPORTANTE)

```
1. Dashboard → Left sidebar → [SQL Editor]
2. En el editor que aparece, click para poner cursor
3. Seleccionar todo en el editor (si hay algo):
   - Ctrl+A (o Cmd+A en Mac)
   - Delete
4. COPIAR DESDE 03_SCHEMA_SQL.md:
   - Abre ese archivo en tu compu
   - Selecciona TODO el SQL (desde CREATE TABLE users...)
   - Ctrl+C para copiar
5. PEGAR en el editor Supabase:
   - Click en el editor
   - Ctrl+V para pegar
6. Ver que aparece TODO el SQL:
   - CREATE TABLE users (
   - CREATE TABLE categories (
   - ... etc
7. EJECUTAR:
   - Click botón [▶ Run] (arriba a la derecha)
   - Esperar respuesta
8. ✅ Verás: "Success! Query completed successfully"
```

Si hay error, verás rojo. Pero si pegaste correctamente, funciona.

### Verificar tablas

```
1. Left sidebar → [Table Editor]
2. En la lista que aparece, verás:
   - users
   - categories (haz click aquí, deberías ver 6 filas)
   - habits
   - activities
   - etc.
3. ✅ Si ves todas las tablas, FUNCIONÓ
```

### Obtener credenciales

```
1. Arriba del dashboard, click en [⚙️ Settings]
2. Left sidebar → [API]
3. Verás dos campos principales:

   "Project URL"
   - Botón [Copy] → COPIA este valor

   "anon public key"  
   - Botón [Copy] → COPIA este valor

4. En tu compu, crea archivo .env:
   SUPABASE_URL = [pega lo del Project URL]
   SUPABASE_KEY = [pega lo del anon public key]

5. ✅ LISTO para usar en Python
```

---

## 📋 CHECKLIST MÁS SIMPLE

- [ ] Ir a supabase.com
- [ ] Crear cuenta (email + password)
- [ ] Confirmar en email
- [ ] Crear proyecto "habit-tracker"
- [ ] Ir a SQL Editor
- [ ] Copiar TODO el SQL de 03_SCHEMA_SQL.md
- [ ] Pegar en editor Supabase
- [ ] Click [▶ Run]
- [ ] Ver ✅ Success
- [ ] Ir a Table Editor
- [ ] Verificar 8 tablas existen
- [ ] Ir a Settings → API
- [ ] Copiar Project URL
- [ ] Copiar anon public key
- [ ] Guardar en .env local
- [ ] ✅ DONE!

---

## 🎯 CUÁNTO TARDA

- Crear cuenta: 2 minutos
- Crear proyecto: 3 minutos
- Crear tablas (SQL): 2 minutos
- Total: **~7 minutos**

---

## ❓ PREGUNTAS FRECUENTES

**P: ¿Qué si me sale error al ejecutar el SQL?**
A: Mira la sección "SOLUCIONAR PROBLEMAS" en 07_CREAR_TABLAS_SUPABASE.md

**P: ¿El plan Free es suficiente?**
A: ✅ SÍ, completamente. Supabase free te da:
- 500MB BD
- 2 GB bajada/mes
- Perfecto para desarrollo y pequeño uso

**P: ¿Dónde guardo el .env?**
A: En la raíz de tu proyecto Streamlit local:
```
habit-tracker/
├── main.py
├── .env ← AQUÍ
├── requirements.txt
├── pages/
└── utils/
```

**P: ¿Puedo ver las tablas después sin ir a Supabase?**
A: SÍ, desde Streamlit. Hacemos consultas SQL desde Python.

**P: ¿Necesito hacer más SQL después?**
A: NO. Todo está en 03_SCHEMA_SQL.md. Lo ejecutas una sola vez.

---

## 🎬 RESUMIDO EN GIF (Imaginario)

```
1. supabase.com → Get Started → Email → Confirm
   [Sign up screen] ↓
   
2. Create project → "habit-tracker" → Free
   [Project creation] ↓
   
3. SQL Editor → Paste SQL → Run
   [SQL code screen] → [▶ Run] → ✅ Success ↓
   
4. Table Editor → Ver 8 tablas
   [Table list screen] ↓
   
5. Settings → API → Copy credentials
   [Credentials screen] ↓
   
6. Create .env file en tu compu
   [File saved] ↓
   
✅ LISTO PARA STREAMLIT
```

---

## 🚀 SIGUIENTE PASO

Una vez hayas hecho todo esto, tienes:

✅ Base de datos en Supabase
✅ Tablas creadas
✅ Datos de prueba insertados (categorías)
✅ Credenciales guardadas

**Próximo:** Conectar desde Streamlit (ver documento 04_GUIA_STREAMLIT.md)

---

**Status:** ✅ Listo para implementar  
**Dificultad:** ⭐ Muy fácil (solo copiar/pegar)  
**Tiempo:** ⏱️ 5-10 minutos
