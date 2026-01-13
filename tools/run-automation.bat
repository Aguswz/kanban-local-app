@echo off
REM 🤖 Script de Automatización Kanban para Windows
REM Wrapper para ejecutar scripts de automatización en Windows

setlocal enabledelayedexpansion

REM Configuración
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set BOARD_FILE=%PROJECT_ROOT%\kanban\board.md

REM Colores para output (limitado en Windows)
set GREEN=[92m
set RED=[91m
set YELLOW=[93m
set BLUE=[94m
set NC=[0m

REM Función para mostrar ayuda
if "%1"=="" goto :help
if "%1"=="help" goto :help

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ Python no está instalado o no está en PATH%NC%
    exit /b 1
)

REM Ejecutar comando solicitado
if "%1"=="status" goto :status
if "%1"=="health_check" goto :health_check
if "%1"=="update_metrics" goto :update_metrics
if "%1"=="daily_backup" goto :daily_backup
if "%1"=="cleanup" goto :cleanup
if "%1"=="sync_github" goto :sync_github

echo %RED%❌ Comando desconocido: %1%NC%
goto :help

:status
echo %BLUE%📊 Estado del Sistema Kanban%NC%
echo ================================
echo 📁 Directorio: %PROJECT_ROOT%
echo 📅 Fecha: %date% %time%
echo.

REM Verificar archivos principales
if exist "%BOARD_FILE%" (
    echo ✅ Tablero principal: Encontrado
) else (
    echo ❌ Tablero principal: No encontrado
)

REM Verificar herramientas Python
if exist "%SCRIPT_DIR%kanban-cli.py" (
    echo ✅ Kanban CLI: Disponible
) else (
    echo ❌ Kanban CLI: No encontrado
)

if exist "%SCRIPT_DIR%metrics-collector.py" (
    echo ✅ Metrics Collector: Disponible
) else (
    echo ❌ Metrics Collector: No encontrado
)

goto :end

:health_check
echo %BLUE%🔍 Verificando salud del sistema...%NC%

REM Verificar estructura de directorios
for %%d in (kanban templates tools docs metrics) do (
    if not exist "%PROJECT_ROOT%\%%d" (
        echo %YELLOW%⚠️ Creando directorio faltante: %%d%NC%
        mkdir "%PROJECT_ROOT%\%%d"
    )
)

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ Python no disponible%NC%
    exit /b 1
) else (
    echo %GREEN%✅ Python disponible%NC%
)

echo %GREEN%✅ Verificación de salud completada%NC%
goto :end

:update_metrics
echo %BLUE%📊 Actualizando métricas...%NC%

if exist "%SCRIPT_DIR%metrics-collector.py" (
    python "%SCRIPT_DIR%metrics-collector.py" snapshot
    python "%SCRIPT_DIR%metrics-collector.py" metrics
    echo %GREEN%✅ Métricas actualizadas%NC%
) else (
    echo %RED%❌ Script de métricas no encontrado%NC%
    exit /b 1
)
goto :end

:daily_backup
echo %BLUE%💾 Creando backup diario...%NC%

set BACKUP_DIR=%PROJECT_ROOT%\backups
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

set DATE=%date:~-4,4%-%date:~-10,2%-%date:~-7,2%
set BACKUP_FILE=%BACKUP_DIR%\kanban-backup-%DATE%.zip

REM Crear backup usando PowerShell (más confiable en Windows)
powershell -Command "Compress-Archive -Path '%PROJECT_ROOT%\kanban', '%PROJECT_ROOT%\stories', '%PROJECT_ROOT%\tasks', '%PROJECT_ROOT%\metrics' -DestinationPath '%BACKUP_FILE%' -Force"

if exist "%BACKUP_FILE%" (
    echo %GREEN%✅ Backup creado: %BACKUP_FILE%%NC%
) else (
    echo %RED%❌ Error creando backup%NC%
    exit /b 1
)
goto :end

:cleanup
echo %BLUE%🧹 Limpiando archivos temporales...%NC%

REM Limpiar archivos temporales
del /q /s "%PROJECT_ROOT%\*.tmp" >nul 2>&1
del /q /s "%PROJECT_ROOT%\*.log" >nul 2>&1

echo %GREEN%✅ Limpieza completada%NC%
goto :end

:sync_github
echo %BLUE%🔗 Sincronizando con GitHub...%NC%

if exist "%SCRIPT_DIR%github-integration.py" (
    python "%SCRIPT_DIR%github-integration.py" test
    if errorlevel 1 (
        echo %RED%❌ Error de conexión con GitHub%NC%
        exit /b 1
    )
    python "%SCRIPT_DIR%github-integration.py" sync
    echo %GREEN%✅ Sincronización completada%NC%
) else (
    echo %YELLOW%⚠️ Integración con GitHub no configurada%NC%
)
goto :end

:help
echo 🤖 Scripts de Automatización Kanban - Windows
echo.
echo Comandos disponibles:
echo   status            - Mostrar estado del sistema
echo   health_check      - Verificar salud del sistema
echo   update_metrics    - Actualizar métricas
echo   daily_backup      - Crear backup diario
echo   cleanup           - Limpiar archivos temporales
echo   sync_github       - Sincronizar con GitHub
echo.
echo Ejemplo de uso:
echo   run-automation.bat status
echo   run-automation.bat health_check
echo.
echo Para automatización, usar Programador de tareas de Windows
goto :end

:end
endlocal