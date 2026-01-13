# 🧠 Team Manager Desktop - Aplicación de Gestión de Equipos con IA

## Descripción
Aplicación de escritorio multiplataforma para gestión profesional de múltiples equipos y proyectos, con asistente IA integrado que actúa como director de operaciones ágil.

## Características Principales

### 🎯 Gestión Multi-Equipo
- Control centralizado de múltiples equipos y proyectos
- Vista global del estado del trabajo en tiempo real
- Coordinación automática entre equipos
- Gestión de dependencias inter-proyecto

### ⏱️ Control de Tiempos y Carga
- Estimación vs tiempo real por persona y equipo
- Detección automática de sobrecarga
- Planificación realista basada en capacidad
- Alertas proactivas de riesgos

### 🧠 IA como Director de Operaciones
- Análisis contextual de todos los equipos
- Detección temprana de cuellos de botella
- Sugerencias de redistribución de trabajo
- Optimización continua del flujo

### 🖥️ Aplicación Nativa
- Instalación local (Windows/macOS/Linux)
- Funciona completamente offline
- Datos bajo control del usuario
- Interfaz profesional optimizada para uso diario

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    ELECTRON APP                             │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React + TypeScript + Tailwind)                  │
│  ├── Dashboard Global                                       │
│  ├── Vista por Equipos                                      │
│  ├── Vista por Proyectos                                    │
│  ├── Kanban Boards                                          │
│  ├── Control de Carga                                       │
│  └── Panel de IA                                            │
├─────────────────────────────────────────────────────────────┤
│  Backend Embebido (Python + FastAPI)                       │
│  ├── Motor Multi-Kanban                                     │
│  ├── Reglas Agile/Scrum                                     │
│  ├── Gestión de Equipos                                     │
│  ├── Control de Tiempos                                     │
│  ├── Coordinación Inter-Proyecto                            │
│  └── Agente IA Director                                     │
├─────────────────────────────────────────────────────────────┤
│  Persistencia (SQLite + JSON)                              │
│  ├── Base de Datos Relacional                               │
│  ├── Configuraciones JSON                                   │
│  ├── Backup Automático                                      │
│  └── Versionado de Datos                                    │
└─────────────────────────────────────────────────────────────┘
```

## Instalación y Uso

### Requisitos
- Windows 10+, macOS 10.14+, o Linux (Ubuntu 18.04+)
- 4GB RAM mínimo, 8GB recomendado
- 2GB espacio en disco

### Instalación
1. Descargar el instalador para tu plataforma
2. Ejecutar instalador (firmado digitalmente)
3. Configuración inicial guiada
4. ¡Listo para usar!

## Desarrollo

### Estructura del Proyecto
```
team-manager-desktop/
├── electron/                 # Configuración Electron
├── frontend/                 # React + TypeScript
├── backend/                  # Python + FastAPI
├── database/                 # Esquemas y migraciones
├── ai/                       # Agente IA y prompts
├── build/                    # Scripts de construcción
└── dist/                     # Aplicaciones compiladas
```

### Comandos de Desarrollo
```bash
npm run dev          # Desarrollo con hot reload
npm run build        # Construcción para producción
npm run package      # Crear instaladores
npm run test         # Ejecutar tests
```

## Licencia
Propietaria - Uso interno de la organización