# 📊 Habit Tracker - Sistema Inteligente de Tracking de Hábitos

Un sistema completo de tracking de hábitos con **cruces múltiples** que permite que una actividad contribuya a varios hábitos simultáneamente.

## ✨ Características Principales

- 🎯 **Metas Completamente Personalizadas**: Crea exactamente las metas que necesitas, sin restricciones
- ⚡ **Cruce Inteligente**: Una actividad puede beneficiar múltiples hábitos con pesos ajustables
- 📈 **Dashboard Avanzado**: Visualizaciones con Plotly para analizar tu progreso
- 🔐 **Autenticación Completa**: Sistema de login/registro con Supabase Auth
- 📊 **Métricas Automáticas**: Cálculos automáticos de progreso, porcentajes y proyecciones
- 📝 **Registro Diario**: Interfaz intuitiva para registrar sesiones con mood y productividad
- 🎨 **Interfaz Moderna**: UI pulida con Streamlit

## 🏗️ Arquitectura

```
┌─────────────────────────────────────┐
│      FRONTEND: Streamlit            │
│  ├─ Login/Registro                  │
│  ├─ Dashboard con gráficos          │
│  ├─ CRUD de Hábitos                 │
│  ├─ CRUD de Actividades             │
│  └─ Registro de Sesiones            │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│    DATABASE: Supabase (PostgreSQL)  │
│  ├─ Autenticación (Supabase Auth)   │
│  ├─ 8 Tablas principales            │
│  ├─ 4 Vistas SQL precalculadas      │
│  └─ Triggers automáticos            │
└─────────────────────────────────────┘
```

## 🚀 Instalación Rápida

1. Clona el repositorio
2. Instala dependencias: `pip install -r requirements.txt`
3. Configura `.env` con tus credenciales de Supabase
4. Ejecuta: `streamlit run main.py`

Ver el README completo para instrucciones detalladas de configuración.
