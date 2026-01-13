const { app, BrowserWindow, Menu, ipcMain, dialog } = require('electron')
const path = require('path')
const { spawn } = require('child_process')
const isDev = process.env.NODE_ENV === 'development'

let mainWindow
let backendProcess

// Configuración de la ventana principal
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, '../assets/icon.png'),
    titleBarStyle: 'default',
    show: false // No mostrar hasta que esté listo
  })

  // Cargar la aplicación
  if (isDev) {
    mainWindow.loadURL('http://localhost:3000')
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(path.join(__dirname, '../frontend/dist/index.html'))
  }

  // Mostrar cuando esté listo
  mainWindow.once('ready-to-show', () => {
    mainWindow.show()
    
    // Centrar la ventana
    mainWindow.center()
  })

  // Manejar cierre de ventana
  mainWindow.on('closed', () => {
    mainWindow = null
  })

  // Prevenir navegación externa
  mainWindow.webContents.on('will-navigate', (event, navigationUrl) => {
    const parsedUrl = new URL(navigationUrl)
    
    if (parsedUrl.origin !== 'http://localhost:3000' && parsedUrl.origin !== 'file://') {
      event.preventDefault()
    }
  })
}

// Iniciar backend Python
function startBackend() {
  if (isDev) {
    // En desarrollo, el backend se inicia por separado
    return
  }

  const backendPath = path.join(process.resourcesPath, 'backend', 'main.exe')
  
  backendProcess = spawn(backendPath, [], {
    stdio: 'pipe',
    cwd: path.dirname(backendPath)
  })

  backendProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`)
  })

  backendProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`)
  })

  backendProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`)
  })
}

// Detener backend
function stopBackend() {
  if (backendProcess) {
    backendProcess.kill()
    backendProcess = null
  }
}

// Configurar menú de aplicación
function createMenu() {
  const template = [
    {
      label: 'Archivo',
      submenu: [
        {
          label: 'Nuevo Proyecto',
          accelerator: 'CmdOrCtrl+N',
          click: () => {
            mainWindow.webContents.send('menu-action', 'new-project')
          }
        },
        {
          label: 'Importar Datos',
          click: async () => {
            const result = await dialog.showOpenDialog(mainWindow, {
              properties: ['openFile'],
              filters: [
                { name: 'JSON Files', extensions: ['json'] },
                { name: 'All Files', extensions: ['*'] }
              ]
            })
            
            if (!result.canceled) {
              mainWindow.webContents.send('menu-action', 'import-data', result.filePaths[0])
            }
          }
        },
        {
          label: 'Exportar Datos',
          click: async () => {
            const result = await dialog.showSaveDialog(mainWindow, {
              filters: [
                { name: 'JSON Files', extensions: ['json'] }
              ]
            })
            
            if (!result.canceled) {
              mainWindow.webContents.send('menu-action', 'export-data', result.filePath)
            }
          }
        },
        { type: 'separator' },
        {
          label: 'Configuración',
          accelerator: 'CmdOrCtrl+,',
          click: () => {
            mainWindow.webContents.send('menu-action', 'settings')
          }
        },
        { type: 'separator' },
        {
          label: 'Salir',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => {
            app.quit()
          }
        }
      ]
    },
    {
      label: 'Editar',
      submenu: [
        { role: 'undo', label: 'Deshacer' },
        { role: 'redo', label: 'Rehacer' },
        { type: 'separator' },
        { role: 'cut', label: 'Cortar' },
        { role: 'copy', label: 'Copiar' },
        { role: 'paste', label: 'Pegar' },
        { role: 'selectall', label: 'Seleccionar Todo' }
      ]
    },
    {
      label: 'Vista',
      submenu: [
        {
          label: 'Dashboard',
          accelerator: 'CmdOrCtrl+1',
          click: () => {
            mainWindow.webContents.send('menu-action', 'view-dashboard')
          }
        },
        {
          label: 'Equipos',
          accelerator: 'CmdOrCtrl+2',
          click: () => {
            mainWindow.webContents.send('menu-action', 'view-teams')
          }
        },
        {
          label: 'Proyectos',
          accelerator: 'CmdOrCtrl+3',
          click: () => {
            mainWindow.webContents.send('menu-action', 'view-projects')
          }
        },
        {
          label: 'Carga de Trabajo',
          accelerator: 'CmdOrCtrl+4',
          click: () => {
            mainWindow.webContents.send('menu-action', 'view-workload')
          }
        },
        { type: 'separator' },
        { role: 'reload', label: 'Recargar' },
        { role: 'forceReload', label: 'Forzar Recarga' },
        { role: 'toggleDevTools', label: 'Herramientas de Desarrollo' },
        { type: 'separator' },
        { role: 'resetZoom', label: 'Zoom Normal' },
        { role: 'zoomIn', label: 'Acercar' },
        { role: 'zoomOut', label: 'Alejar' },
        { type: 'separator' },
        { role: 'togglefullscreen', label: 'Pantalla Completa' }
      ]
    },
    {
      label: 'IA',
      submenu: [
        {
          label: 'Abrir Asistente IA',
          accelerator: 'CmdOrCtrl+I',
          click: () => {
            mainWindow.webContents.send('menu-action', 'open-ai-assistant')
          }
        },
        {
          label: 'Análisis Global',
          accelerator: 'CmdOrCtrl+Shift+A',
          click: () => {
            mainWindow.webContents.send('menu-action', 'ai-global-analysis')
          }
        },
        {
          label: 'Detectar Riesgos',
          click: () => {
            mainWindow.webContents.send('menu-action', 'ai-detect-risks')
          }
        },
        {
          label: 'Optimizar Flujo',
          click: () => {
            mainWindow.webContents.send('menu-action', 'ai-optimize-flow')
          }
        }
      ]
    },
    {
      label: 'Ayuda',
      submenu: [
        {
          label: 'Guía de Uso',
          click: () => {
            mainWindow.webContents.send('menu-action', 'help-guide')
          }
        },
        {
          label: 'Atajos de Teclado',
          click: () => {
            mainWindow.webContents.send('menu-action', 'help-shortcuts')
          }
        },
        { type: 'separator' },
        {
          label: 'Acerca de Team Manager',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'Acerca de Team Manager',
              message: 'Team Manager Desktop v1.0.0',
              detail: 'Aplicación profesional de gestión de equipos con IA integrada.\n\nDesarrollado para optimizar el flujo de trabajo y la coordinación entre equipos.'
            })
          }
        }
      ]
    }
  ]

  // Ajustes específicos para macOS
  if (process.platform === 'darwin') {
    template.unshift({
      label: app.getName(),
      submenu: [
        { role: 'about', label: 'Acerca de Team Manager' },
        { type: 'separator' },
        { role: 'services', label: 'Servicios' },
        { type: 'separator' },
        { role: 'hide', label: 'Ocultar Team Manager' },
        { role: 'hideothers', label: 'Ocultar Otros' },
        { role: 'unhide', label: 'Mostrar Todo' },
        { type: 'separator' },
        { role: 'quit', label: 'Salir de Team Manager' }
      ]
    })
  }

  const menu = Menu.buildFromTemplate(template)
  Menu.setApplicationMenu(menu)
}

// Eventos de la aplicación
app.whenReady().then(() => {
  createWindow()
  createMenu()
  startBackend()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  stopBackend()
  
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('before-quit', () => {
  stopBackend()
})

// IPC handlers
ipcMain.handle('get-app-version', () => {
  return app.getVersion()
})

ipcMain.handle('show-message-box', async (event, options) => {
  const result = await dialog.showMessageBox(mainWindow, options)
  return result
})

ipcMain.handle('show-error-box', (event, title, content) => {
  dialog.showErrorBox(title, content)
})

// Manejo de errores no capturadas
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error)
  dialog.showErrorBox('Error Crítico', `Se produjo un error inesperado:\n\n${error.message}`)
})

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason)
})