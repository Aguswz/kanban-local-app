import { useEffect, useCallback } from 'react'

// Tipos para la API de Electron
interface ElectronAPI {
  getAppVersion: () => Promise<string>
  showMessageBox: (options: any) => Promise<any>
  showErrorBox: (title: string, content: string) => Promise<void>
  onMenuAction: (callback: (action: string, data?: any) => void) => void
  removeAllListeners: (channel: string) => void
  platform: string
  isDev: boolean
}

// Declarar la API global de Electron
declare global {
  interface Window {
    electronAPI?: ElectronAPI
  }
}

export const useElectronAPI = () => {
  const isElectron = typeof window !== 'undefined' && window.electronAPI

  const getAppVersion = useCallback(async (): Promise<string> => {
    if (isElectron) {
      return await window.electronAPI!.getAppVersion()
    }
    return '1.0.0-web'
  }, [isElectron])

  const showMessageBox = useCallback(async (options: {
    type?: 'none' | 'info' | 'error' | 'question' | 'warning'
    title?: string
    message: string
    detail?: string
    buttons?: string[]
    defaultId?: number
    cancelId?: number
  }) => {
    if (isElectron) {
      return await window.electronAPI!.showMessageBox(options)
    } else {
      // Fallback para web
      const result = window.confirm(`${options.title || 'Confirmación'}\n\n${options.message}${options.detail ? '\n\n' + options.detail : ''}`)
      return { response: result ? 0 : 1 }
    }
  }, [isElectron])

  const showErrorBox = useCallback(async (title: string, content: string) => {
    if (isElectron) {
      await window.electronAPI!.showErrorBox(title, content)
    } else {
      // Fallback para web
      alert(`${title}\n\n${content}`)
    }
  }, [isElectron])

  const onMenuAction = useCallback((callback: (action: string, data?: any) => void) => {
    if (isElectron) {
      window.electronAPI!.onMenuAction(callback)
    }
  }, [isElectron])

  const removeAllListeners = useCallback((channel: string) => {
    if (isElectron) {
      window.electronAPI!.removeAllListeners(channel)
    }
  }, [isElectron])

  const getPlatform = useCallback((): string => {
    if (isElectron) {
      return window.electronAPI!.platform
    }
    return 'web'
  }, [isElectron])

  const isDev = useCallback((): boolean => {
    if (isElectron) {
      return window.electronAPI!.isDev
    }
    return process.env.NODE_ENV === 'development'
  }, [isElectron])

  // Cleanup al desmontar
  useEffect(() => {
    return () => {
      if (isElectron) {
        removeAllListeners('menu-action')
      }
    }
  }, [isElectron, removeAllListeners])

  return {
    isElectron,
    getAppVersion,
    showMessageBox,
    showErrorBox,
    onMenuAction,
    removeAllListeners,
    platform: getPlatform(),
    isDev: isDev(),
  }
}

// Hook para mostrar confirmaciones
export const useConfirmDialog = () => {
  const { showMessageBox } = useElectronAPI()

  const confirm = useCallback(async (
    message: string,
    title: string = 'Confirmación',
    detail?: string
  ): Promise<boolean> => {
    const result = await showMessageBox({
      type: 'question',
      title,
      message,
      detail,
      buttons: ['Cancelar', 'Confirmar'],
      defaultId: 1,
      cancelId: 0,
    })
    
    return result.response === 1
  }, [showMessageBox])

  const confirmDanger = useCallback(async (
    message: string,
    title: string = 'Acción Peligrosa',
    detail?: string
  ): Promise<boolean> => {
    const result = await showMessageBox({
      type: 'warning',
      title,
      message,
      detail,
      buttons: ['Cancelar', 'Continuar'],
      defaultId: 0,
      cancelId: 0,
    })
    
    return result.response === 1
  }, [showMessageBox])

  return {
    confirm,
    confirmDanger,
  }
}

// Hook para manejo de errores
export const useErrorHandler = () => {
  const { showErrorBox } = useElectronAPI()

  const handleError = useCallback((error: Error | string, title: string = 'Error') => {
    const message = typeof error === 'string' ? error : error.message
    console.error('Error:', error)
    showErrorBox(title, message)
  }, [showErrorBox])

  const handleAsyncError = useCallback(async (
    asyncFn: () => Promise<any>,
    errorTitle: string = 'Error'
  ) => {
    try {
      return await asyncFn()
    } catch (error) {
      handleError(error as Error, errorTitle)
      throw error
    }
  }, [handleError])

  return {
    handleError,
    handleAsyncError,
  }
}