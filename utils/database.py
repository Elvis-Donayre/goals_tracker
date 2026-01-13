"""
=============================================================================
CLASE SUPABASEDB - HABIT TRACKER
=============================================================================
Maneja todas las operaciones con la base de datos Supabase
"""

import os
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class SupabaseDB:
    """
    Clase para manejar todas las operaciones con Supabase
    """

    def __init__(self):
        """Inicializar conexión con Supabase"""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise ValueError(
                "Faltan credenciales de Supabase. "
                "Asegúrate de tener un archivo .env con SUPABASE_URL y SUPABASE_KEY"
            )

        self.supabase: Client = create_client(self.url, self.key)

    # =========================================================================
    # AUTENTICACIÓN
    # =========================================================================

    def sign_up(self, email: str, password: str, full_name: str = None) -> Dict[str, Any]:
        """
        Registrar nuevo usuario

        Args:
            email: Email del usuario
            password: Contraseña
            full_name: Nombre completo (opcional)

        Returns:
            Diccionario con datos del usuario o error
        """
        try:
            # Registrar en Supabase Auth
            auth_response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if auth_response.user:
                # Insertar en tabla users
                user_data = {
                    "id": auth_response.user.id,
                    "email": email,
                    "full_name": full_name
                }

                self.supabase.table("users").insert(user_data).execute()

                return {
                    "success": True,
                    "user": auth_response.user,
                    "message": "Usuario registrado exitosamente"
                }

            return {"success": False, "message": "Error al registrar usuario"}

        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}

    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """
        Iniciar sesión

        Args:
            email: Email del usuario
            password: Contraseña

        Returns:
            Diccionario con datos del usuario o error
        """
        try:
            auth_response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if auth_response.user:
                return {
                    "success": True,
                    "user": auth_response.user,
                    "session": auth_response.session
                }

            return {"success": False, "message": "Credenciales inválidas"}

        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}

    def sign_out(self) -> Dict[str, Any]:
        """Cerrar sesión"""
        try:
            self.supabase.auth.sign_out()
            return {"success": True, "message": "Sesión cerrada"}
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Obtener usuario actual"""
        try:
            user = self.supabase.auth.get_user()
            return user.user if user else None
        except:
            return None

    # =========================================================================
    # CATEGORÍAS
    # =========================================================================

    def get_categories(self) -> pd.DataFrame:
        """Obtener todas las categorías predefinidas"""
        try:
            response = self.supabase.table("categories").select("*").execute()
            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Error obteniendo categorías: {e}")
            return pd.DataFrame()

    def create_user_category(
        self,
        user_id: str,
        name: str,
        color: str = "#3B82F6"
    ) -> Optional[Dict[str, Any]]:
        """
        Crear categoría personalizada del usuario

        Args:
            user_id: ID del usuario
            name: Nombre de la categoría
            color: Color en formato hex

        Returns:
            Diccionario con la categoría creada o None
        """
        try:
            response = self.supabase.table("user_categories").insert({
                "user_id": user_id,
                "name": name.strip(),
                "color": color
            }).execute()

            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creando categoría: {e}")
            return None

    def get_all_categories_for_user(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Obtener categorías predefinidas + personalizadas del usuario

        Returns:
            Lista con categorías tipo 'system' y 'personal'
        """
        try:
            result = []

            # Categorías predefinidas
            predefined = self.supabase.table("categories").select("*").execute()
            if predefined.data:
                for cat in predefined.data:
                    result.append({
                        "id": cat["id"],
                        "name": cat["name"],
                        "type": "system",
                        "color": cat.get("color", "#3B82F6")
                    })

            # Categorías del usuario
            user_cats = self.supabase.table("user_categories").select("*").eq(
                "user_id", user_id
            ).execute()

            if user_cats.data:
                for cat in user_cats.data:
                    result.append({
                        "id": cat["id"],
                        "name": cat["name"],
                        "type": "personal",
                        "color": cat.get("color", "#3B82F6")
                    })

            return result
        except Exception as e:
            print(f"Error obteniendo categorías: {e}")
            return []

    # =========================================================================
    # HÁBITOS/METAS
    # =========================================================================

    def create_habit(
        self,
        user_id: str,
        name: str,
        target_minutes_per_week: int = 420,
        max_minutes_per_week: int = 900,
        total_hours_goal: int = 100,
        description: str = None,
        category_id: int = None
    ) -> Optional[Dict[str, Any]]:
        """
        Crear nuevo hábito/meta personalizada

        Args:
            user_id: ID del usuario
            name: Nombre de la meta (texto libre)
            target_minutes_per_week: Target mínimo semanal
            max_minutes_per_week: Máximo semanal para evitar burnout
            total_hours_goal: Objetivo total en horas
            description: Descripción opcional
            category_id: ID de categoría (opcional)

        Returns:
            Diccionario con el hábito creado o None
        """
        try:
            if not name or not name.strip():
                print("Error: El nombre del hábito no puede estar vacío")
                return None

            habit_data = {
                "user_id": user_id,
                "name": name.strip(),
                "description": description.strip() if description else None,
                "category_id": category_id,
                "target_minutes_per_week": target_minutes_per_week,
                "max_minutes_per_week": max_minutes_per_week,
                "total_hours_goal": total_hours_goal,
                "is_active": True
            }

            response = self.supabase.table("habits").insert(habit_data).execute()

            if response.data:
                # Crear entrada en habit_metrics
                habit_id = response.data[0]["id"]
                self.supabase.table("habit_metrics").insert({
                    "habit_id": habit_id,
                    "total_minutes_invested": 0,
                    "total_sessions": 0,
                    "current_streak": 0,
                    "longest_streak": 0,
                    "completion_percentage": 0.0
                }).execute()

                return response.data[0]

            return None
        except Exception as e:
            print(f"Error creando hábito: {e}")
            return None

    def get_user_habits(self, user_id: str, active_only: bool = True) -> pd.DataFrame:
        """
        Obtener hábitos del usuario

        Args:
            user_id: ID del usuario
            active_only: Si True, solo retorna hábitos activos

        Returns:
            DataFrame con los hábitos
        """
        try:
            query = self.supabase.table("habits").select("*").eq("user_id", user_id)

            if active_only:
                query = query.eq("is_active", True)

            response = query.order("created_at", desc=True).execute()

            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Error obteniendo hábitos: {e}")
            return pd.DataFrame()

    def update_habit(self, habit_id: str, updates: Dict[str, Any]) -> bool:
        """
        Actualizar un hábito

        Args:
            habit_id: ID del hábito
            updates: Diccionario con campos a actualizar

        Returns:
            True si se actualizó correctamente
        """
        try:
            updates["updated_at"] = datetime.now().isoformat()
            response = self.supabase.table("habits").update(updates).eq("id", habit_id).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error actualizando hábito: {e}")
            return False

    def delete_habit(self, habit_id: str) -> bool:
        """
        Eliminar un hábito (soft delete - marca como inactivo)

        Args:
            habit_id: ID del hábito

        Returns:
            True si se eliminó correctamente
        """
        try:
            return self.update_habit(habit_id, {"is_active": False})
        except Exception as e:
            print(f"Error eliminando hábito: {e}")
            return False

    def get_habit_progress(self, user_id: str) -> pd.DataFrame:
        """
        Obtener progreso de todos los hábitos del usuario usando la vista

        Args:
            user_id: ID del usuario

        Returns:
            DataFrame con progreso detallado
        """
        try:
            response = self.supabase.table("habit_progress").select("*").eq(
                "user_id", user_id
            ).execute()

            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Error obteniendo progreso: {e}")
            return pd.DataFrame()

    # =========================================================================
    # ACTIVIDADES
    # =========================================================================

    def create_activity(
        self,
        user_id: str,
        name: str,
        category_id: int = None,
        description: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        Crear nueva actividad

        Args:
            user_id: ID del usuario
            name: Nombre de la actividad
            category_id: ID de categoría (opcional)
            description: Descripción opcional

        Returns:
            Diccionario con la actividad creada o None
        """
        try:
            if not name or not name.strip():
                print("Error: El nombre de la actividad no puede estar vacío")
                return None

            activity_data = {
                "user_id": user_id,
                "name": name.strip(),
                "category_id": category_id,
                "description": description.strip() if description else None
            }

            response = self.supabase.table("activities").insert(activity_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creando actividad: {e}")
            return None

    def get_user_activities(self, user_id: str) -> pd.DataFrame:
        """Obtener actividades del usuario"""
        try:
            response = self.supabase.table("activities").select("*").eq(
                "user_id", user_id
            ).order("created_at", desc=True).execute()

            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Error obteniendo actividades: {e}")
            return pd.DataFrame()

    def update_activity(self, activity_id: str, updates: Dict[str, Any]) -> bool:
        """Actualizar actividad"""
        try:
            updates["updated_at"] = datetime.now().isoformat()
            response = self.supabase.table("activities").update(updates).eq(
                "id", activity_id
            ).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error actualizando actividad: {e}")
            return False

    def delete_activity(self, activity_id: str) -> bool:
        """Eliminar actividad"""
        try:
            response = self.supabase.table("activities").delete().eq(
                "id", activity_id
            ).execute()
            return True
        except Exception as e:
            print(f"Error eliminando actividad: {e}")
            return False

    # =========================================================================
    # VINCULACIÓN HÁBITOS-ACTIVIDADES (EL CRUCE INTELIGENTE)
    # =========================================================================

    def link_activity_to_habit(
        self,
        habit_id: str,
        activity_id: str,
        weight: float = 1.0
    ) -> bool:
        """
        Vincular actividad a hábito con peso

        Args:
            habit_id: ID del hábito
            activity_id: ID de la actividad
            weight: Peso de contribución (0.0 a 1.0)

        Returns:
            True si se vinculó correctamente
        """
        try:
            if weight < 0 or weight > 1:
                print("Error: El peso debe estar entre 0 y 1")
                return False

            # Verificar si ya existe la relación
            existing = self.supabase.table("habit_activities").select("*").eq(
                "habit_id", habit_id
            ).eq("activity_id", activity_id).execute()

            if existing.data:
                # Actualizar peso existente
                response = self.supabase.table("habit_activities").update({
                    "weight": weight,
                    "updated_at": datetime.now().isoformat()
                }).eq("habit_id", habit_id).eq("activity_id", activity_id).execute()
            else:
                # Crear nueva vinculación
                response = self.supabase.table("habit_activities").insert({
                    "habit_id": habit_id,
                    "activity_id": activity_id,
                    "weight": weight
                }).execute()

            return bool(response.data)
        except Exception as e:
            print(f"Error vinculando actividad a hábito: {e}")
            return False

    def unlink_activity_from_habit(self, habit_id: str, activity_id: str) -> bool:
        """Desvincular actividad de hábito"""
        try:
            response = self.supabase.table("habit_activities").delete().eq(
                "habit_id", habit_id
            ).eq("activity_id", activity_id).execute()
            return True
        except Exception as e:
            print(f"Error desvinculando: {e}")
            return False

    def get_activity_links(self, activity_id: str) -> pd.DataFrame:
        """
        Obtener todos los hábitos vinculados a una actividad

        Args:
            activity_id: ID de la actividad

        Returns:
            DataFrame con habit_id, habit_name, weight
        """
        try:
            response = self.supabase.table("habit_activities").select(
                "*, habits(id, name)"
            ).eq("activity_id", activity_id).execute()

            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Error obteniendo vínculos: {e}")
            return pd.DataFrame()

    def get_habit_activities_matrix(self, user_id: str) -> pd.DataFrame:
        """Obtener matriz de actividades por hábito usando la vista"""
        try:
            response = self.supabase.table("activity_habit_matrix").select("*").eq(
                "user_id", user_id
            ).execute()

            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Error obteniendo matriz: {e}")
            return pd.DataFrame()

    # =========================================================================
    # SESIONES (REGISTRO DE TIEMPO)
    # =========================================================================

    def register_session(
        self,
        activity_id: str,
        duration_minutes: int,
        session_date: date = None,
        start_time: str = None,
        notes: str = None,
        mood: int = None,
        productivity_level: int = None
    ) -> Optional[Dict[str, Any]]:
        """
        Registrar sesión de actividad
        AUTOMÁTICAMENTE distribuye el tiempo entre hábitos vinculados

        Args:
            activity_id: ID de la actividad
            duration_minutes: Duración en minutos
            session_date: Fecha de la sesión (default: hoy)
            start_time: Hora de inicio (opcional)
            notes: Notas (opcional)
            mood: Estado de ánimo 1-5 (opcional)
            productivity_level: Productividad 1-5 (opcional)

        Returns:
            Diccionario con la sesión creada o None
        """
        try:
            if duration_minutes <= 0:
                print("Error: La duración debe ser mayor a 0")
                return None

            if mood and (mood < 1 or mood > 5):
                print("Error: Mood debe estar entre 1 y 5")
                return None

            if productivity_level and (productivity_level < 1 or productivity_level > 5):
                print("Error: Productivity debe estar entre 1 y 5")
                return None

            session_data = {
                "activity_id": activity_id,
                "duration_minutes": duration_minutes,
                "session_date": (session_date or date.today()).isoformat(),
                "start_time": start_time,
                "notes": notes,
                "mood": mood,
                "productivity_level": productivity_level
            }

            response = self.supabase.table("sessions").insert(session_data).execute()

            if response.data:
                # El trigger register_session() en Supabase automáticamente
                # actualiza las métricas de los hábitos vinculados
                return response.data[0]

            return None
        except Exception as e:
            print(f"Error registrando sesión: {e}")
            return None

    def get_user_sessions(
        self,
        user_id: str,
        limit: int = 100,
        start_date: date = None,
        end_date: date = None
    ) -> pd.DataFrame:
        """
        Obtener sesiones del usuario

        Args:
            user_id: ID del usuario
            limit: Número máximo de sesiones a retornar
            start_date: Fecha de inicio (opcional)
            end_date: Fecha de fin (opcional)

        Returns:
            DataFrame con las sesiones
        """
        try:
            query = self.supabase.table("sessions").select(
                "*, activities!inner(user_id, name)"
            ).eq("activities.user_id", user_id)

            if start_date:
                query = query.gte("session_date", start_date.isoformat())

            if end_date:
                query = query.lte("session_date", end_date.isoformat())

            response = query.order("session_date", desc=True).limit(limit).execute()

            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Error obteniendo sesiones: {e}")
            return pd.DataFrame()

    def get_activity_contribution(self, user_id: str) -> pd.DataFrame:
        """
        Obtener contribución de actividades a hábitos usando la vista
        Muestra cómo se distribuye cada sesión entre múltiples hábitos

        Args:
            user_id: ID del usuario

        Returns:
            DataFrame con contribuciones detalladas
        """
        try:
            # Necesitamos filtrar por user_id a través de activities
            response = self.supabase.table("activity_habit_contribution").select(
                "*, activities!inner(user_id)"
            ).eq("activities.user_id", user_id).execute()

            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Error obteniendo contribuciones: {e}")
            return pd.DataFrame()

    # =========================================================================
    # MÉTRICAS Y ESTADÍSTICAS
    # =========================================================================

    def get_weekly_summary(self, user_id: str) -> pd.DataFrame:
        """Obtener resumen semanal de progreso usando la vista"""
        try:
            response = self.supabase.table("weekly_summary").select("*").eq(
                "user_id", user_id
            ).execute()

            return pd.DataFrame(response.data) if response.data else pd.DataFrame()
        except Exception as e:
            print(f"Error obteniendo resumen semanal: {e}")
            return pd.DataFrame()

    def get_habit_metrics(self, habit_id: str) -> Optional[Dict[str, Any]]:
        """Obtener métricas de un hábito específico"""
        try:
            response = self.supabase.table("habit_metrics").select("*").eq(
                "habit_id", habit_id
            ).execute()

            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error obteniendo métricas: {e}")
            return None

    def update_habit_metrics(self, habit_id: str) -> bool:
        """
        Forzar actualización de métricas de un hábito
        (Normalmente se actualizan automáticamente vía trigger)
        """
        try:
            # Llamar a la función SQL update_habit_metrics
            response = self.supabase.rpc("update_habit_metrics", {
                "p_habit_id": habit_id
            }).execute()
            return True
        except Exception as e:
            print(f"Error actualizando métricas: {e}")
            return False
