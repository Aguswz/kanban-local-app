# 🚀 Guía de Inicio - Team Manager Desktop

## Instalación y Configuración

### Requisitos del Sistema

**Mínimos:**
- Windows 10+ / macOS 10.14+ / Ubuntu 18.04+
- 4GB RAM
- 2GB espacio en disco
- Conexión a internet (para IA, opcional)

**Recomendados:**
- 8GB RAM
- 4GB espacio en disco
- Procesador multi-core
- SSD para mejor rendimiento

### Instalación

1. **Descargar la aplicación**
   - Visita la página de releases
   - Descarga el instalador para tu plataforma
   - Verifica la firma digital (recomendado)

2. **Instalar**
   - **Windows**: Ejecuta el `.exe` y sigue el asistente
   - **macOS**: Abre el `.dmg` y arrastra a Aplicaciones
   - **Linux**: Ejecuta el `.AppImage` directamente

3. **Primera ejecución**
   - La aplicación se iniciará automáticamente
   - Configuración inicial guiada
   - Creación del primer equipo y proyecto

## Configuración Inicial

### 1. Configuración Básica

Al abrir por primera vez, verás el asistente de configuración:

```
┌─────────────────────────────────────┐
│        Team Manager Desktop        │
│                                     │
│  🎯 Configuración Inicial           │
│                                     │
│  Nombre de la organización:         │
│  [Mi Empresa                    ]   │
│                                     │
│  Tu nombre:                         │
│  [Juan Pérez                    ]   │
│                                     │
│  Tu rol:                            │
│  [▼ Director de Proyectos       ]   │
│                                     │
│  Zona horaria:                      │
│  [▼ America/Mexico_City         ]   │
│                                     │
│           [Continuar]               │
└─────────────────────────────────────┘
```

### 2. Configuración del Director IA

El Director IA puede funcionar en tres modos:

**Modo Simulación (Gratuito)**
- Análisis basado en reglas heurísticas
- Funciona completamente offline
- Ideal para pruebas y uso básico

**Modo OpenAI (Recomendado)**
- Análisis avanzado con GPT-4
- Requiere API key de OpenAI
- Mejor calidad de insights

**Modo Anthropic**
- Análisis detallado con Claude
- Requiere API key de Anthropic
- Excelente para análisis contextual

```
┌─────────────────────────────────────┐
│     Configuración Director IA       │
│                                     │
│  Proveedor de IA:                   │
│  ○ Simulación (Gratuito)            │
│  ● OpenAI (Recomendado)             │
│  ○ Anthropic                        │
│                                     │
│  API Key de OpenAI:                 │
│  [sk-...                        ]   │
│                                     │
│  ✓ Conexión verificada              │
│                                     │
│           [Guardar]                 │
└─────────────────────────────────────┘
```

### 3. Crear Primer Equipo

```
┌─────────────────────────────────────┐
│        Crear Primer Equipo          │
│                                     │
│  Nombre del equipo:                 │
│  [Desarrollo Frontend           ]   │
│                                     │
│  Descripción:                       │
│  [Equipo encargado del desarrollo   │
│   de interfaces de usuario      ]   │
│                                     │
│  Color del equipo:                  │
│  [🔵] [🟢] [🟡] [🔴] [🟣]           │
│                                     │
│  Límites WIP:                       │
│  En progreso: [3] Revisión: [2]     │
│                                     │
│           [Crear Equipo]            │
└─────────────────────────────────────┘
```

## Conceptos Fundamentales

### Jerarquía Organizacional

```
Organización
├── Equipos (1-20)
│   ├── Miembros (1-15 por equipo)
│   └── Proyectos (múltiples)
└── Proyectos
    ├── Tarjetas/Tareas
    └── Dependencias
```

### Flujo de Trabajo

1. **Crear Equipos** → Definir capacidades y roles
2. **Crear Proyectos** → Asignar a equipos
3. **Gestionar Trabajo** → Tableros Kanban por equipo
4. **Monitorear** → Dashboard global y análisis IA
5. **Optimizar** → Seguir recomendaciones del Director IA

### Roles y Permisos

**Admin**
- Configuración global
- Gestión de todos los equipos
- Acceso completo al Director IA

**Manager**
- Gestión de equipos asignados
- Creación de proyectos
- Análisis de carga de trabajo

**Member**
- Gestión de sus tareas
- Vista de su equipo
- Reportes básicos

## Uso Diario

### Dashboard Principal

El dashboard es tu centro de control:

```
┌─────────────────────────────────────────────────────────────┐
│  🏠 Dashboard Ejecutivo                    🧠 Director IA   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 Métricas Clave                                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │ 5 Equipos│ │12 Proyec│ │  85%    │ │ 2 Riesgos│           │
│  │ Activos  │ │ Activos │ │Utiliza. │ │Críticos  │           │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘           │
│                                                             │
│  🚨 Alertas Críticas                                        │
│  ⚠️ Equipo Frontend sobrecargado (120% utilización)         │
│  🔴 Proyecto Alpha bloqueado por dependencia externa        │
│                                                             │
│  📈 Estado de Equipos        🧠 Insights del Director IA    │
│  [Gráfico de carga]          💡 Redistribuir trabajo del    │
│                                  equipo Frontend            │
│                               ⚡ Resolver bloqueo crítico   │
│                                  en Proyecto Alpha          │
└─────────────────────────────────────────────────────────────┘
```

### Gestión de Equipos

**Vista de Equipo Individual:**
- Tablero Kanban del equipo
- Carga de trabajo por miembro
- Métricas de rendimiento
- Alertas específicas del equipo

**Acciones Comunes:**
- Crear/editar tarjetas
- Mover tarjetas entre columnas
- Asignar trabajo a miembros
- Configurar límites WIP

### Director IA

El Director IA es tu asistente principal:

**Análisis Automático:**
- Ejecuta análisis cada 30 minutos
- Detecta problemas proactivamente
- Genera recomendaciones específicas

**Interacción Manual:**
- Pregunta en lenguaje natural
- Solicita análisis específicos
- Pide recomendaciones de optimización

**Ejemplos de Prompts:**
```
"¿Qué equipos están sobrecargados?"
"Analiza los riesgos del Proyecto Alpha"
"¿Cómo puedo optimizar el flujo de trabajo?"
"Detecta cuellos de botella en la organización"
```

## Atajos de Teclado

### Navegación Global
- `Ctrl/Cmd + 1` → Dashboard
- `Ctrl/Cmd + 2` → Equipos
- `Ctrl/Cmd + 3` → Proyectos
- `Ctrl/Cmd + 4` → Carga de Trabajo

### Director IA
- `Ctrl/Cmd + I` → Abrir Director IA
- `Ctrl/Cmd + Shift + A` → Análisis Global
- `Ctrl/Cmd + Shift + R` → Detectar Riesgos

### Acciones Rápidas
- `Ctrl/Cmd + N` → Nuevo Proyecto
- `Ctrl/Cmd + T` → Nueva Tarea
- `Ctrl/Cmd + ,` → Configuración

## Mejores Prácticas

### 1. Configuración de Equipos

**Tamaño Óptimo:**
- 3-8 miembros por equipo
- Roles claramente definidos
- Capacidades realistas (6-8h/día)

**Límites WIP:**
- En progreso: 1-2 por persona
- Revisión: 30-50% del WIP total
- Ajustar según métricas reales

### 2. Gestión de Proyectos

**Planificación:**
- Definir dependencias claramente
- Estimaciones realistas
- Fechas de entrega flexibles

**Seguimiento:**
- Revisar progreso semanalmente
- Actualizar estimaciones regularmente
- Resolver bloqueos inmediatamente

### 3. Uso del Director IA

**Frecuencia:**
- Revisar insights diariamente
- Análisis global semanal
- Seguir recomendaciones prioritarias

**Configuración:**
- API key de IA configurada
- Contexto organizacional completo
- Feedback regular al sistema

### 4. Optimización Continua

**Métricas Clave:**
- Tiempo de ciclo por equipo
- Utilización promedio
- Número de bloqueos
- Satisfacción del equipo

**Acciones Regulares:**
- Retrospectivas mensuales
- Ajuste de procesos
- Capacitación continua
- Mejora de herramientas

## Solución de Problemas

### Problemas Comunes

**La aplicación no inicia:**
1. Verificar requisitos del sistema
2. Ejecutar como administrador
3. Revisar logs en `%APPDATA%/team-manager/logs`

**Director IA no responde:**
1. Verificar conexión a internet
2. Validar API key
3. Cambiar a modo simulación temporalmente

**Rendimiento lento:**
1. Cerrar aplicaciones innecesarias
2. Verificar espacio en disco
3. Reiniciar la aplicación

**Datos no se guardan:**
1. Verificar permisos de escritura
2. Revisar espacio en disco
3. Comprobar integridad de la base de datos

### Logs y Diagnóstico

**Ubicación de logs:**
- Windows: `%APPDATA%/team-manager/logs/`
- macOS: `~/Library/Application Support/team-manager/logs/`
- Linux: `~/.config/team-manager/logs/`

**Información útil:**
- `app.log` → Log principal de la aplicación
- `ai.log` → Logs del Director IA
- `database.log` → Logs de base de datos
- `error.log` → Errores críticos

## Soporte

### Recursos de Ayuda

**Documentación:**
- Guía de usuario completa
- Tutoriales en video
- FAQ actualizada

**Comunidad:**
- Foro de usuarios
- Canal de Discord
- Repositorio GitHub

**Soporte Técnico:**
- Email: support@teammanager.com
- Tickets de soporte
- Chat en vivo (horario comercial)

### Reportar Problemas

Al reportar un problema, incluye:
1. Versión de la aplicación
2. Sistema operativo
3. Pasos para reproducir
4. Logs relevantes
5. Capturas de pantalla

¡Estás listo para optimizar la gestión de tus equipos con Team Manager Desktop! 🚀