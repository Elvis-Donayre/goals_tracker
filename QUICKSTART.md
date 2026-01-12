# ⚡ Quick Start - Habit Tracker

**Tiempo estimado**: 15 minutos

## 🚀 Configuración Rápida

### 1. Instalar dependencias (2 min)

```bash
pip install -r requirements.txt
```

### 2. Configurar Supabase (5 min)

1. Ir a [supabase.com](https://supabase.com) → Login
2. **New Project** → `habit-tracker`
3. **SQL Editor** → Copiar SQL de `12_SQL_ACTUALIZADO.md`
4. **Run** → ✅ Success
5. **Settings → API** → Copiar:
   - Project URL
   - anon public key

### 3. Configurar .env (1 min)

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Editar `.env`:
```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=eyJhbGc...tu_clave_anon
```

### 4. Ejecutar (1 min)

```bash
streamlit run main.py
```

Se abrirá en: `http://localhost:8501`

## 📝 Primer Uso

### Registrarte (1 min)

1. Pestaña **"📝 Registrarse"**
2. Email + Contraseña
3. **Crear Cuenta**
4. Verificar email
5. **Iniciar Sesión**

### Crear tu primer hábito (2 min)

1. **🎯 Mis Hábitos** → **➕ Crear Hábito**
2. Nombre: "Aprender Python"
3. Target: 420 min/semana
4. Objetivo: 100 horas
5. **Crear Meta**

### Crear actividad (1 min)

1. **⚡ Actividades** → **➕ Crear Actividad**
2. Nombre: "Ver tutoriales Python"
3. **Crear Actividad**

### Vincular (1 min)

1. **⚡ Actividades** → **🔗 Vincular a Hábitos**
2. Seleccionar actividad
3. ✅ Marcar hábito "Aprender Python"
4. Peso: 1.0
5. **Guardar Vínculos**

### Registrar sesión (1 min)

1. **📝 Registrar Sesión**
2. Actividad: "Ver tutoriales Python"
3. Duración: 60 minutos
4. **Registrar Sesión**

### Ver progreso

1. **📈 Dashboard** → ¡Ver tus datos! 📊

## ✅ Listo

Ahora tienes:
- ✅ Sistema funcionando
- ✅ Primera meta creada
- ✅ Primera actividad vinculada
- ✅ Primera sesión registrada
- ✅ Progreso visible en Dashboard

## 📚 Más Información

- **Documentación completa**: `README.md`
- **Guía detallada**: `SETUP_GUIDE.md`
- **SQL a ejecutar**: `12_SQL_ACTUALIZADO.md`

## 🐛 Problemas

### No se conecta a Supabase
→ Verifica `.env` tiene las credenciales correctas

### Tablas no existen
→ Ejecuta TODO el SQL en Supabase

### Error al registrar
→ Verifica tu email (confirmación)

## 💡 Tips

1. **Metas personalizadas**: Crea exactamente lo que necesites
2. **Pesos flexibles**: Ajusta cuánto contribuye cada actividad
3. **Registro diario**: Sé consistente para ver progreso real
4. **Analiza datos**: Usa Dashboard para insights

---

**¿Listo? ¡Empieza a trackear tus hábitos!** 🎯
