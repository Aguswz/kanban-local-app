const { contextBridge, ipcRenderer } = require('electron')

// Exponer APIs seguras al renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  // Información de la aplicación
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  
  // Diálogos
  showMessageBox: (options) => ipcRenderer.invoke('show-message-box', options),
  showErrorBox: (title, content) => ipcRenderer.invoke('show-error-box', title, content),
  
  // Eventos del menú
  onMenuAction: (callback) => {
    ipcRenderer.on('menu-action', (event, action, data) => {
      callback(action, data)
    })
  },
  
  // Remover listeners
  removeAllListeners: (channel) => {
    ipcRenderer.removeAllListeners(channel)
  },
  
  // Información del sistema
  platform: process.platform,
  
  // Constantes útiles
  isDev: process.env.NODE_ENV === 'development'
})

// Prevenir que el renderer acceda a Node.js directamente
delete window.require
delete window.exports
delete window.module