"""
=============================================================================
FUNCIONES AUXILIARES - HABIT TRACKER
=============================================================================
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Tuple
import pandas as pd


def calculate_weeks_to_goal(
    current_minutes: int,
    goal_hours: int,
    minutes_per_week: int
) -> Tuple[int, str]:
    """
    Calcular semanas necesarias para completar objetivo

    Args:
        current_minutes: Minutos ya invertidos
        goal_hours: Objetivo total en horas
        minutes_per_week: Ritmo semanal

    Returns:
        Tupla (semanas_restantes, fecha_estimada)
    """
    total_goal_minutes = goal_hours * 60
    remaining_minutes = total_goal_minutes - current_minutes

    if minutes_per_week <= 0:
        return 0, "N/A"

    weeks_remaining = max(0, remaining_minutes / minutes_per_week)
    estimated_date = date.today() + timedelta(weeks=weeks_remaining)

    return int(weeks_remaining), estimated_date.strftime("%B %Y")


def calculate_completion_percentage(
    current_minutes: int,
    goal_hours: int
) -> float:
    """
    Calcular porcentaje de completación

    Args:
        current_minutes: Minutos invertidos
        goal_hours: Objetivo en horas

    Returns:
        Porcentaje (0-100)
    """
    if goal_hours <= 0:
        return 0.0

    total_goal_minutes = goal_hours * 60
    percentage = (current_minutes / total_goal_minutes) * 100

    return min(100.0, max(0.0, percentage))


def format_duration(minutes: int) -> str:
    """
    Formatear minutos en texto legible

    Args:
        minutes: Minutos totales

    Returns:
        String formateado (ej: "2h 30m", "45m")
    """
    if minutes < 60:
        return f"{minutes}m"

    hours = minutes // 60
    mins = minutes % 60

    if mins == 0:
        return f"{hours}h"

    return f"{hours}h {mins}m"


def get_week_boundaries(reference_date: date = None) -> Tuple[date, date]:
    """
    Obtener inicio y fin de la semana actual

    Args:
        reference_date: Fecha de referencia (default: hoy)

    Returns:
        Tupla (start_date, end_date)
    """
    if reference_date is None:
        reference_date = date.today()

    # Lunes como inicio de semana
    start = reference_date - timedelta(days=reference_date.weekday())
    end = start + timedelta(days=6)

    return start, end


def categorize_completion(percentage: float) -> Dict[str, Any]:
    """
    Categorizar nivel de completación

    Args:
        percentage: Porcentaje de completación

    Returns:
        Diccionario con status, color y mensaje
    """
    if percentage >= 100:
        return {
            "status": "Completado",
            "color": "#10B981",  # Verde
            "icon": "✅",
            "message": "¡Objetivo alcanzado!"
        }
    elif percentage >= 75:
        return {
            "status": "Excelente progreso",
            "color": "#3B82F6",  # Azul
            "icon": "🔥",
            "message": "Casi llegas a la meta"
        }
    elif percentage >= 50:
        return {
            "status": "Buen ritmo",
            "color": "#F59E0B",  # Amarillo
            "icon": "⚡",
            "message": "Vas por buen camino"
        }
    elif percentage >= 25:
        return {
            "status": "En progreso",
            "color": "#EF4444",  # Naranja
            "icon": "📈",
            "message": "Continúa así"
        }
    else:
        return {
            "status": "Recién comenzando",
            "color": "#6B7280",  # Gris
            "icon": "🚀",
            "message": "¡Empieza tu viaje!"
        }


def calculate_weekly_compliance(
    minutes_this_week: int,
    target_minutes_per_week: int
) -> Dict[str, Any]:
    """
    Calcular cumplimiento semanal

    Args:
        minutes_this_week: Minutos de esta semana
        target_minutes_per_week: Target semanal

    Returns:
        Diccionario con porcentaje, status y color
    """
    if target_minutes_per_week <= 0:
        return {
            "percentage": 0,
            "status": "Sin target",
            "color": "#6B7280"
        }

    percentage = (minutes_this_week / target_minutes_per_week) * 100

    if percentage >= 100:
        status = "✅ Completado"
        color = "#10B981"
    elif percentage >= 75:
        status = "⚡ Casi ahí"
        color = "#3B82F6"
    elif percentage >= 50:
        status = "📊 En camino"
        color = "#F59E0B"
    else:
        status = "⚠️ Rezagado"
        color = "#EF4444"

    return {
        "percentage": round(percentage, 1),
        "status": status,
        "color": color
    }


def validate_email(email: str) -> bool:
    """
    Validar formato de email

    Args:
        email: Email a validar

    Returns:
        True si es válido
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validar fortaleza de contraseña

    Args:
        password: Contraseña a validar

    Returns:
        Tupla (es_valida, mensaje_error)
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"

    if not any(c.isupper() for c in password):
        return False, "Debe incluir al menos una mayúscula"

    if not any(c.islower() for c in password):
        return False, "Debe incluir al menos una minúscula"

    if not any(c.isdigit() for c in password):
        return False, "Debe incluir al menos un número"

    return True, ""


def get_color_for_category(category_name: str) -> str:
    """
    Obtener color para categoría

    Args:
        category_name: Nombre de la categoría

    Returns:
        Color en formato hex
    """
    colors = {
        "Salud": "#EF4444",
        "Aprendizaje": "#3B82F6",
        "Productividad": "#10B981",
        "Desarrollo Personal": "#8B5CF6",
        "Relaciones": "#F59E0B",
        "Finanzas": "#EC4899"
    }

    return colors.get(category_name, "#6B7280")


def format_date_spanish(date_obj: date) -> str:
    """
    Formatear fecha en español

    Args:
        date_obj: Objeto de fecha

    Returns:
        Fecha formateada (ej: "9 de enero de 2026")
    """
    months = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }

    return f"{date_obj.day} de {months[date_obj.month]} de {date_obj.year}"


def get_mood_emoji(mood: int) -> str:
    """
    Obtener emoji para mood

    Args:
        mood: Valor de mood (1-5)

    Returns:
        Emoji correspondiente
    """
    emojis = {
        1: "😢",
        2: "😕",
        3: "😐",
        4: "😊",
        5: "😄"
    }

    return emojis.get(mood, "😐")


def get_productivity_bars(productivity: int) -> str:
    """
    Obtener barras de productividad

    Args:
        productivity: Nivel de productividad (1-5)

    Returns:
        String con barras
    """
    return "▮" * productivity + "▯" * (5 - productivity)


def aggregate_sessions_by_period(
    sessions_df: pd.DataFrame,
    period: str = "week"
) -> pd.DataFrame:
    """
    Agregar sesiones por período

    Args:
        sessions_df: DataFrame de sesiones
        period: 'day', 'week', 'month', 'year'

    Returns:
        DataFrame agregado
    """
    if sessions_df.empty:
        return pd.DataFrame()

    sessions_df["session_date"] = pd.to_datetime(sessions_df["session_date"])

    if period == "day":
        return sessions_df.groupby(
            sessions_df["session_date"].dt.date
        )["duration_minutes"].sum().reset_index()

    elif period == "week":
        return sessions_df.groupby(
            sessions_df["session_date"].dt.to_period("W")
        )["duration_minutes"].sum().reset_index()

    elif period == "month":
        return sessions_df.groupby(
            sessions_df["session_date"].dt.to_period("M")
        )["duration_minutes"].sum().reset_index()

    elif period == "year":
        return sessions_df.groupby(
            sessions_df["session_date"].dt.year
        )["duration_minutes"].sum().reset_index()

    return sessions_df


def calculate_streak(sessions_df: pd.DataFrame) -> int:
    """
    Calcular racha actual de días consecutivos

    Args:
        sessions_df: DataFrame de sesiones

    Returns:
        Número de días consecutivos
    """
    if sessions_df.empty:
        return 0

    sessions_df["session_date"] = pd.to_datetime(sessions_df["session_date"])
    unique_dates = sorted(sessions_df["session_date"].dt.date.unique(), reverse=True)

    if not unique_dates:
        return 0

    streak = 0
    expected_date = date.today()

    for session_date in unique_dates:
        if session_date == expected_date or session_date == expected_date - timedelta(days=1):
            streak += 1
            expected_date = session_date - timedelta(days=1)
        else:
            break

    return streak
