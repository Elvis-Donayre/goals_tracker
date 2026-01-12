# Diagramas del Proyecto: Habit Tracker

## 1. DIAGRAMA DE ARQUITECTURA GENERAL

```mermaid
graph TB
    subgraph "Frontend"
        ST["Streamlit App<br/>(Local o Cloud)"]
    end
    
    subgraph "Backend Cloud"
        SB["Supabase"]
        subgraph "Supabase Components"
            AUTH["Auth<br/>(Autenticación)"]
            API["REST API<br/>(Auto-generada)"]
            DB["PostgreSQL<br/>(Base de datos)"]
        end
    end
    
    subgraph "User Machine"
        BS["Browser<br/>(Streamlit UI)"]
    end
    
    ST -->|HTTP Requests| API
    API -->|SQL Queries| DB
    BS -->|Visualiza| ST
    
    style ST fill:#ff6b6b
    style SB fill:#3ecf8e
    style DB fill:#4facfe
    style API fill:#43e97b
```

---

## 2. DIAGRAMA DE FLUJO DE DATOS

```mermaid
graph LR
    subgraph "User Actions"
        UA1["Crear Hábito"]
        UA2["Registrar Completación"]
        UA3["Ver Dashboard"]
    end
    
    subgraph "Streamlit Logic"
        SL1["Validar datos"]
        SL2["Llamar función SQL"]
        SL3["Query a vistas"]
    end
    
    subgraph "Supabase Processing"
        SP1["Insertar en tabla"]
        SP2["Ejecutar función PL/pgSQL"]
        SP3["Actualizar métricas"]
        SP4["Ejecutar queries"]
    end
    
    subgraph "Database"
        DB1["habits"]
        DB2["completions"]
        DB3["habit_metrics"]
        DB4["habits_summary VIEW"]
    end
    
    UA1 --> SL1
    UA2 --> SL2
    UA3 --> SL3
    
    SL1 --> SP1
    SL2 --> SP2
    SL3 --> SP4
    
    SP1 --> DB1
    SP2 --> DB2
    SP3 --> DB3
    SP4 --> DB4
    
    style UA1 fill:#ffe66d
    style UA2 fill:#ffe66d
    style UA3 fill:#ffe66d
    style SP2 fill:#a8edea
    style SP3 fill:#a8edea
```

---

## 3. DIAGRAMA DE ENTIDAD-RELACIÓN (ER)

```mermaid
erDiagram
    USERS ||--o{ HABITS : "has"
    CATEGORIES ||--o{ HABITS : "categorizes"
    HABITS ||--o{ COMPLETIONS : "tracked_by"
    HABITS ||--o{ HABIT_METRICS : "has_one"
    HABITS ||--o{ HABIT_CHANGES_LOG : "logs"
    
    USERS {
        uuid id PK
        string email UK
        timestamp created_at
        timestamp updated_at
    }
    
    CATEGORIES {
        int id PK
        string name UK
        text description
        string color
        timestamp created_at
    }
    
    HABITS {
        int id PK
        uuid user_id FK
        string name
        text description
        int category_id FK
        string frequency
        int target_per_week
        int target_per_month
        boolean is_active
        text notes
        timestamp created_at
        timestamp updated_at
    }
    
    COMPLETIONS {
        int id PK
        int habit_id FK
        date completed_date
        timestamp completed_at
        text notes
        int streak_count
        timestamp created_at
    }
    
    HABIT_METRICS {
        int id PK
        int habit_id FK UK
        int current_streak
        int longest_streak
        int total_completions
        decimal completion_rate
        date last_completed_date
        timestamp updated_at
    }
    
    HABIT_CHANGES_LOG {
        int id PK
        int habit_id FK
        string change_type
        jsonb old_values
        jsonb new_values
        timestamp changed_at
    }
```

---

## 4. DIAGRAMA DE ESTRUCTURA DE CARPETAS

```mermaid
graph TD
    A["habit-tracker/"] --> B["main.py"]
    A --> C["requirements.txt"]
    A --> D[".env"]
    A --> E[".gitignore"]
    A --> F["pages/"]
    A --> G["utils/"]
    A --> H[".streamlit/"]
    
    F --> F1["01_Dashboard.py"]
    F --> F2["02_Agregar_Habito.py"]
    F --> F3["03_Registrar_Progreso.py"]
    
    G --> G1["database.py"]
    G --> G2["helpers.py"]
    G --> G3["__init__.py"]
    
    H --> H1["config.toml"]
    H --> H2["secrets.toml"]
    
    style A fill:#f9ca24
    style B fill:#6c5ce7
    style F fill:#a29bfe
    style G fill:#a29bfe
    style H fill:#a29bfe
```

---

## 5. FLUJO DE REGISTRO DE COMPLETACIÓN (Detallado)

```mermaid
sequenceDiagram
    participant User as Usuario
    participant ST as Streamlit
    participant DB as Supabase API
    participant SQL as PostgreSQL
    
    User->>ST: Hace clic "Marcar completado"
    ST->>DB: register_completion(habit_id)
    DB->>SQL: RPC: register_completion()
    
    activate SQL
    SQL->>SQL: Insertar en COMPLETIONS
    SQL->>SQL: Calcular calculate_current_streak()
    SQL->>SQL: Actualizar HABIT_METRICS
    SQL-->>DB: ✓ Éxito
    deactivate SQL
    
    DB-->>ST: Response exitosa
    ST->>ST: Refrescar dashboard
    ST-->>User: ✅ "Hábito completado"
    User->>ST: Ve actualizado en tabla
    
    style User fill:#ffe66d
    style ST fill:#ff6b6b
    style DB fill:#43e97b
    style SQL fill:#4facfe
```

---

## 6. DIAGRAMA DE ESTADÍSTICAS Y VISTAS

```mermaid
graph TB
    subgraph "Raw Data"
        C["COMPLETIONS<br/>(Registros crudos)"]
        H["HABITS<br/>(Definiciones)"]
        M["HABIT_METRICS<br/>(Precalculadas)"]
    end
    
    subgraph "Agregaciones SQL"
        Q1["Racha actual<br/>(PL/pgSQL)"]
        Q2["Racha más larga<br/>(Window functions)"]
        Q3["Tasa completación<br/>(Agregaciones)"]
        Q4["Tendencias últimos 30d<br/>(Time-based)"]
    end
    
    subgraph "Vistas Supabase"
        V["habits_summary VIEW"]
    end
    
    subgraph "Visualizaciones Streamlit"
        D1["📊 Dashboard Principal"]
        D2["📈 Gráfico de Rachas"]
        D3["📉 Tendencias"]
        D4["🎯 Resumen Categorías"]
    end
    
    C --> Q1
    C --> Q2
    C --> Q3
    C --> Q4
    H --> V
    M --> V
    
    Q1 --> D2
    Q2 --> D2
    Q3 --> D1
    Q4 --> D3
    V --> D1
    V --> D4
    
    style C fill:#dfe6e9
    style M fill:#dfe6e9
    style V fill:#74b9ff
    style D1 fill:#55efc4
    style D2 fill:#55efc4
    style D3 fill:#55efc4
    style D4 fill:#55efc4
```

---

## 7. CICLO DE VIDA DE UN HÁBITO

```mermaid
stateDiagram-v2
    [*] --> Creado: Usuario crea hábito
    
    Creado --> Activo: is_active = true
    
    Activo --> Pausado: Usuario pausa
    Pausado --> Activo: Usuario reactiva
    
    Activo --> Completado: Objetivo alcanzado
    Pausado --> Completado: Usuario marca como completado
    
    Completado --> [*]
    
    note right of Activo
        Registra completaciones
        Calcula métricas
        Actualiza racha
    end note
    
    note right of Pausado
        No acepta registros
        Mantiene datos históricos
    end note
```

---

## 8. MATRIZ DE PERMISOS Y SEGURIDAD

```mermaid
graph TB
    subgraph "Row Level Security (RLS)"
        RLS1["HABITS: Solo usuario propietario"]
        RLS2["COMPLETIONS: Solo usuario propietario"]
        RLS3["CATEGORIES: Público (lectura)"]
    end
    
    subgraph "API Keys"
        KEY1["ANON KEY (Frontend)<br/>Acceso limitado + RLS"]
        KEY2["SERVICE KEY (Backend)<br/>⚠️ NUNCA en Streamlit"]
    end
    
    subgraph "Datos Expuestos en Frontend"
        EXP1["✓ Tu nombre de usuario"]
        EXP2["✓ Tus hábitos"]
        EXP3["✓ Tus completaciones"]
        EXP4["✗ Emails de otros usuarios"]
    end
    
    RLS1 --> KEY1
    RLS2 --> KEY1
    RLS3 --> KEY1
    
    KEY1 --> EXP1
    KEY1 --> EXP2
    KEY1 --> EXP3
    
    style KEY1 fill:#55efc4
    style KEY2 fill:#ff7675
    style RLS1 fill:#dfe6e9
    style RLS2 fill:#dfe6e9
    style RLS3 fill:#dfe6e9
```

---

## 9. COMPONENTES DE STREAMLIT

```mermaid
graph TB
    subgraph "Aplicación Principal"
        MAIN["main.py<br/>(Landing page)"]
    end
    
    subgraph "Páginas"
        P1["01_Dashboard.py<br/>(Métricas generales)"]
        P2["02_Agregar_Habito.py<br/>(CRUD hábitos)"]
        P3["03_Registrar_Progreso.py<br/>(Registrar completación)"]
    end
    
    subgraph "Utilidades"
        U1["database.py<br/>(Conexión Supabase)"]
        U2["helpers.py<br/>(Funciones auxiliares)"]
    end
    
    subgraph "Componentes Reutilizables"
        C1["Métrica cards"]
        C2["Gráficos Plotly"]
        C3["Tablas interactivas"]
        C4["Formularios"]
    end
    
    MAIN --> P1
    MAIN --> P2
    MAIN --> P3
    
    P1 --> U1
    P2 --> U1
    P3 --> U1
    
    P1 --> C1
    P1 --> C2
    P1 --> C3
    
    P2 --> C4
    P3 --> C4
    
    U1 --> U2
    
    style MAIN fill:#ff6b6b
    style P1 fill:#ff7675
    style P2 fill:#ff7675
    style P3 fill:#ff7675
    style U1 fill:#0984e3
    style U2 fill:#0984e3
```

---

## 10. FLUJO COMPLETO: DE USUARIO A DATOS

```mermaid
graph LR
    A["👤 Usuario<br/>en navegador"] 
    B["🌐 Interfaz<br/>Streamlit"]
    C["📤 HTTP Request<br/>JSON"]
    D["☁️ Supabase<br/>API REST"]
    E["🔐 Validación<br/>RLS + Auth"]
    F["💾 PostgreSQL<br/>Transacción"]
    G["📊 Tabla<br/>Actualizada"]
    H["📥 JSON<br/>Response"]
    I["🎨 Dashboard<br/>Refrescado"]
    
    A -->|Ingresa datos| B
    B -->|Crea payload| C
    C -->|POST/INSERT| D
    D -->|Verifica permisos| E
    E -->|Query SQL| F
    F -->|Commit| G
    G -->|Serializa| H
    H -->|Renderiza| I
    I -->|Visualiza| A
    
    style A fill:#ffe66d
    style B fill:#ff6b6b
    style C fill:#fab1a0
    style D fill:#43e97b
    style E fill:#74b9ff
    style F fill:#4facfe
    style G fill:#a29bfe
    style H fill:#fab1a0
    style I fill:#55efc4
```

---

## RESUMEN VISUAL: Stack Técnico

```
┌─────────────────────────────────────────────┐
│          HABIT TRACKER STACK                │
├─────────────────────────────────────────────┤
│                                             │
│  🖥️  FRONTEND (Streamlit)                   │
│  ├─ Python 3.9+                            │
│  ├─ Streamlit 1.28+                        │
│  └─ Plotly (gráficos)                      │
│                                             │
│  ☁️  BACKEND (Supabase)                     │
│  ├─ PostgreSQL 14+                         │
│  ├─ PostgREST (REST API)                   │
│  ├─ PL/pgSQL (funciones)                   │
│  └─ Row Level Security                     │
│                                             │
│  🔒 AUTENTICACIÓN                           │
│  └─ Supabase Auth (JWT)                    │
│                                             │
│  📦 HOSTING                                 │
│  ├─ Supabase Cloud (BD)                    │
│  └─ Streamlit Cloud (App)                  │
│                                             │
└─────────────────────────────────────────────┘
```
