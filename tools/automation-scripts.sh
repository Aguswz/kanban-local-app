#!/bin/bash
# 🤖 Scripts de Automatización para Sistema Kanban
# Conjunto de scripts para automatizar tareas comunes del flujo Kanban

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BOARD_FILE="$PROJECT_ROOT/kanban/board.md"
METRICS_DIR="$PROJECT_ROOT/metrics"

# Funciones de utilidad
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Función: Backup diario del tablero
daily_backup() {
    log_info "Iniciando backup diario..."
    
    BACKUP_DIR="$PROJECT_ROOT/backups"
    mkdir -p "$BACKUP_DIR"
    
    DATE=$(date +%Y-%m-%d)
    BACKUP_FILE="$BACKUP_DIR/kanban-backup-$DATE.tar.gz"
    
    # Crear backup comprimido
    tar -czf "$BACKUP_FILE" \
        -C "$PROJECT_ROOT" \
        kanban/ \
        stories/ \
        tasks/ \
        epics/ \
        metrics/ \
        --exclude="*.tmp" \
        --exclude="*.log" 2>/dev/null || true
    
    if [ -f "$BACKUP_FILE" ]; then
        log_success "Backup creado: $BACKUP_FILE"
        
        # Limpiar backups antiguos (mantener últimos 30 días)
        find "$BACKUP_DIR" -name "kanban-backup-*.tar.gz" -mtime +30 -delete 2>/dev/null || true
        log_info "Backups antiguos limpiados"
    else
        log_error "Error creando backup"
        return 1
    fi
}

# Función: Verificar salud del sistema
health_check() {
    log_info "Verificando salud del sistema Kanban..."
    
    local issues=0
    
    # Verificar archivos esenciales
    if [ ! -f "$BOARD_FILE" ]; then
        log_error "Tablero principal no encontrado: $BOARD_FILE"
        ((issues++))
    fi
    
    # Verificar estructura de directorios
    for dir in "kanban" "templates" "tools" "docs" "metrics"; do
        if [ ! -d "$PROJECT_ROOT/$dir" ]; then
            log_warning "Directorio faltante: $dir"
            mkdir -p "$PROJECT_ROOT/$dir"
            log_success "Directorio creado: $dir"
        fi
    done
    
    # Verificar herramientas Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 no está instalado"
        ((issues++))
    else
        log_success "Python3 disponible"
    fi
    
    # Verificar permisos de scripts
    for script in "$SCRIPT_DIR"/*.py; do
        if [ -f "$script" ] && [ ! -x "$script" ]; then
            log_warning "Script sin permisos de ejecución: $(basename "$script")"
            chmod +x "$script"
            log_success "Permisos corregidos: $(basename "$script")"
        fi
    done
    
    # Verificar WIP limits en el tablero
    if [ -f "$BOARD_FILE" ]; then
        local wip_violations=$(grep -c "WIP: [5-9]/[1-4]" "$BOARD_FILE" 2>/dev/null || echo "0")
        if [ "$wip_violations" -gt 0 ]; then
            log_warning "Posibles violaciones de WIP limits detectadas"
        fi
    fi
    
    if [ $issues -eq 0 ]; then
        log_success "Sistema Kanban saludable ✨"
        return 0
    else
        log_error "Se encontraron $issues problemas"
        return 1
    fi
}

# Función: Actualizar métricas automáticamente
update_metrics() {
    log_info "Actualizando métricas..."
    
    if [ -f "$SCRIPT_DIR/metrics-collector.py" ]; then
        python3 "$SCRIPT_DIR/metrics-collector.py" snapshot
        python3 "$SCRIPT_DIR/metrics-collector.py" metrics
        log_success "Métricas actualizadas"
    else
        log_error "Script de métricas no encontrado"
        return 1
    fi
}

# Función: Generar reporte semanal
weekly_report() {
    log_info "Generando reporte semanal..."
    
    local week_start=$(date -d "last monday" +%Y-%m-%d)
    local week_end=$(date -d "next sunday" +%Y-%m-%d)
    
    if [ -f "$SCRIPT_DIR/metrics-collector.py" ]; then
        python3 "$SCRIPT_DIR/metrics-collector.py" report
        log_success "Reporte semanal generado para semana $week_start - $week_end"
    else
        log_error "Script de métricas no encontrado"
        return 1
    fi
    
    # Enviar notificación si está configurado
    if [ -n "$SLACK_WEBHOOK" ]; then
        send_slack_notification "📊 Reporte semanal Kanban generado para $week_start - $week_end"
    fi
}

# Función: Limpiar archivos temporales
cleanup() {
    log_info "Limpiando archivos temporales..."
    
    # Limpiar archivos temporales
    find "$PROJECT_ROOT" -name "*.tmp" -delete 2>/dev/null || true
    find "$PROJECT_ROOT" -name "*.log" -mtime +7 -delete 2>/dev/null || true
    find "$PROJECT_ROOT" -name ".DS_Store" -delete 2>/dev/null || true
    
    # Limpiar métricas antiguas (mantener últimos 90 días)
    if [ -d "$METRICS_DIR" ]; then
        find "$METRICS_DIR" -name "report-*.md" -mtime +90 -delete 2>/dev/null || true
    fi
    
    log_success "Limpieza completada"
}

# Función: Verificar bloqueos críticos
check_blocked_items() {
    log_info "Verificando items bloqueados..."
    
    if [ ! -f "$BOARD_FILE" ]; then
        log_error "Tablero no encontrado"
        return 1
    fi
    
    # Contar items en sección BLOQUEADO
    local blocked_count=$(awk '/## 🚫 BLOQUEADO/,/## / {if(/^- \[ \]/) count++} END {print count+0}' "$BOARD_FILE")
    
    if [ "$blocked_count" -gt 0 ]; then
        log_warning "Se encontraron $blocked_count items bloqueados"
        
        # Extraer items bloqueados
        awk '/## 🚫 BLOQUEADO/,/## / {if(/^- \[ \]/) print "  " $0}' "$BOARD_FILE"
        
        # Enviar alerta si está configurado
        if [ -n "$SLACK_WEBHOOK" ] && [ "$blocked_count" -gt 2 ]; then
            send_slack_notification "🚨 ALERTA: $blocked_count items bloqueados en el tablero Kanban"
        fi
        
        return 1
    else
        log_success "No hay items bloqueados"
        return 0
    fi
}

# Función: Enviar notificación a Slack
send_slack_notification() {
    local message="$1"
    
    if [ -z "$SLACK_WEBHOOK" ]; then
        log_warning "SLACK_WEBHOOK no configurado, saltando notificación"
        return 0
    fi
    
    local payload=$(cat <<EOF
{
    "text": "$message",
    "username": "Kanban Bot",
    "icon_emoji": ":kanban:"
}
EOF
)
    
    if curl -s -X POST -H 'Content-type: application/json' \
        --data "$payload" \
        "$SLACK_WEBHOOK" > /dev/null; then
        log_success "Notificación enviada a Slack"
    else
        log_error "Error enviando notificación a Slack"
    fi
}

# Función: Sincronizar con GitHub
sync_github() {
    log_info "Sincronizando con GitHub..."
    
    if [ -f "$SCRIPT_DIR/github-integration.py" ]; then
        if python3 "$SCRIPT_DIR/github-integration.py" test; then
            python3 "$SCRIPT_DIR/github-integration.py" sync
            log_success "Sincronización con GitHub completada"
        else
            log_error "Error de conexión con GitHub"
            return 1
        fi
    else
        log_warning "Integración con GitHub no configurada"
        return 0
    fi
}

# Función: Configurar cron jobs automáticamente
setup_cron() {
    log_info "Configurando tareas automáticas (cron)..."
    
    local cron_file="/tmp/kanban_cron"
    
    # Crear archivo de cron temporal
    cat > "$cron_file" << EOF
# Kanban System Automation
# Backup diario a las 23:00
0 23 * * * cd "$PROJECT_ROOT" && bash "$SCRIPT_DIR/automation-scripts.sh" daily_backup

# Health check cada 4 horas durante horario laboral
0 9,13,17 * * 1-5 cd "$PROJECT_ROOT" && bash "$SCRIPT_DIR/automation-scripts.sh" health_check

# Actualizar métricas cada 2 horas durante horario laboral
0 9,11,13,15,17 * * 1-5 cd "$PROJECT_ROOT" && bash "$SCRIPT_DIR/automation-scripts.sh" update_metrics

# Verificar bloqueos cada hora durante horario laboral
0 9-17 * * 1-5 cd "$PROJECT_ROOT" && bash "$SCRIPT_DIR/automation-scripts.sh" check_blocked_items

# Reporte semanal los lunes a las 9:00
0 9 * * 1 cd "$PROJECT_ROOT" && bash "$SCRIPT_DIR/automation-scripts.sh" weekly_report

# Limpieza semanal los domingos a las 22:00
0 22 * * 0 cd "$PROJECT_ROOT" && bash "$SCRIPT_DIR/automation-scripts.sh" cleanup

# Sincronización con GitHub cada 6 horas
0 6,12,18 * * * cd "$PROJECT_ROOT" && bash "$SCRIPT_DIR/automation-scripts.sh" sync_github
EOF
    
    # Instalar cron jobs
    if crontab "$cron_file"; then
        log_success "Tareas automáticas configuradas"
        rm "$cron_file"
    else
        log_error "Error configurando cron jobs"
        rm "$cron_file"
        return 1
    fi
    
    log_info "Para ver las tareas configuradas: crontab -l"
    log_info "Para editar manualmente: crontab -e"
}

# Función: Mostrar estado del sistema
status() {
    log_info "Estado del Sistema Kanban"
    echo "================================"
    
    # Información básica
    echo "📁 Directorio: $PROJECT_ROOT"
    echo "📅 Fecha: $(date)"
    echo ""
    
    # Estado del tablero
    if [ -f "$BOARD_FILE" ]; then
        local total_items=$(grep -c "^- \[ \]" "$BOARD_FILE" 2>/dev/null || echo "0")
        local blocked_items=$(awk '/## 🚫 BLOQUEADO/,/## / {if(/^- \[ \]/) count++} END {print count+0}' "$BOARD_FILE")
        
        echo "📊 Items en tablero: $total_items"
        echo "🚫 Items bloqueados: $blocked_items"
    else
        echo "⚠️  Tablero no encontrado"
    fi
    
    # Estado de herramientas
    echo ""
    echo "🛠️  Herramientas:"
    
    if command -v python3 &> /dev/null; then
        echo "  ✅ Python3: $(python3 --version)"
    else
        echo "  ❌ Python3: No instalado"
    fi
    
    if [ -f "$SCRIPT_DIR/kanban-cli.py" ]; then
        echo "  ✅ Kanban CLI: Disponible"
    else
        echo "  ❌ Kanban CLI: No encontrado"
    fi
    
    if [ -f "$SCRIPT_DIR/metrics-collector.py" ]; then
        echo "  ✅ Metrics Collector: Disponible"
    else
        echo "  ❌ Metrics Collector: No encontrado"
    fi
    
    # Estado de integraciones
    echo ""
    echo "🔗 Integraciones:"
    
    if [ -f "$SCRIPT_DIR/github-config.json" ]; then
        echo "  ✅ GitHub: Configurado"
    else
        echo "  ⚪ GitHub: No configurado"
    fi
    
    if [ -n "$SLACK_WEBHOOK" ]; then
        echo "  ✅ Slack: Configurado"
    else
        echo "  ⚪ Slack: No configurado"
    fi
}

# Función principal
main() {
    case "${1:-help}" in
        "daily_backup")
            daily_backup
            ;;
        "health_check")
            health_check
            ;;
        "update_metrics")
            update_metrics
            ;;
        "weekly_report")
            weekly_report
            ;;
        "cleanup")
            cleanup
            ;;
        "check_blocked_items")
            check_blocked_items
            ;;
        "sync_github")
            sync_github
            ;;
        "setup_cron")
            setup_cron
            ;;
        "status")
            status
            ;;
        "help"|*)
            echo "🤖 Scripts de Automatización Kanban"
            echo ""
            echo "Comandos disponibles:"
            echo "  daily_backup      - Crear backup diario del sistema"
            echo "  health_check      - Verificar salud del sistema"
            echo "  update_metrics    - Actualizar métricas"
            echo "  weekly_report     - Generar reporte semanal"
            echo "  cleanup           - Limpiar archivos temporales"
            echo "  check_blocked_items - Verificar items bloqueados"
            echo "  sync_github       - Sincronizar con GitHub"
            echo "  setup_cron        - Configurar tareas automáticas"
            echo "  status            - Mostrar estado del sistema"
            echo ""
            echo "Variables de entorno opcionales:"
            echo "  SLACK_WEBHOOK     - URL del webhook de Slack para notificaciones"
            echo ""
            echo "Ejemplo de uso:"
            echo "  bash automation-scripts.sh health_check"
            echo "  SLACK_WEBHOOK='https://hooks.slack.com/...' bash automation-scripts.sh weekly_report"
            ;;
    esac
}

# Ejecutar función principal con argumentos
main "$@"