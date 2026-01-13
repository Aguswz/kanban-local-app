import React, { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'

// Layouts
import MainLayout from './layouts/MainLayout'

// Pages
import Dashboard from './pages/Dashboard'
import Teams from './pages/Teams'
import Projects from './pages/Projects'
import Workload from './pages/Workload'
import Settings from './pages/Settings'
import TeamDetail from './pages/TeamDetail'
import ProjectDetail from './pages/ProjectDetail'

// Hooks
import { useAppStore } from './store/appStore'
import { useElectronAPI } from './hooks/useElectronAPI'

// Styles
import './styles/globals.css'

function App() {
  const { initializeApp, setCurrentView } = useAppStore()
  const { onMenuAction } = useElectronAPI()

  useEffect(() => {
    // Inicializar la aplicación
    initializeApp()

    // Configurar listeners para acciones del menú de Electron
    onMenuAction((action: string, data?: any) => {
      switch (action) {
        case 'view-dashboard':
          setCurrentView('dashboard')
          window.location.hash = '#/'
          break
        case 'view-teams':
          setCurrentView('teams')
          window.location.hash = '#/teams'
          break
        case 'view-projects':
          setCurrentView('projects')
          window.location.hash = '#/projects'
          break
        case 'view-workload':
          setCurrentView('workload')
          window.location.hash = '#/workload'
          break
        case 'settings':
          setCurrentView('settings')
          window.location.hash = '#/settings'
          break
        case 'new-project':
          // Trigger new project modal
          document.dispatchEvent(new CustomEvent('open-new-project-modal'))
          break
        case 'open-ai-assistant':
          // Trigger AI assistant
          document.dispatchEvent(new CustomEvent('open-ai-assistant'))
          break
        case 'ai-global-analysis':
          // Trigger global analysis
          document.dispatchEvent(new CustomEvent('ai-global-analysis'))
          break
        case 'ai-detect-risks':
          // Trigger risk detection
          document.dispatchEvent(new CustomEvent('ai-detect-risks'))
          break
        case 'ai-optimize-flow':
          // Trigger flow optimization
          document.dispatchEvent(new CustomEvent('ai-optimize-flow'))
          break
        case 'import-data':
          // Handle data import
          if (data) {
            document.dispatchEvent(new CustomEvent('import-data', { detail: data }))
          }
          break
        case 'export-data':
          // Handle data export
          if (data) {
            document.dispatchEvent(new CustomEvent('export-data', { detail: data }))
          }
          break
        default:
          console.log('Unhandled menu action:', action)
      }
    })
  }, [initializeApp, setCurrentView, onMenuAction])

  return (
    <div className="App">
      <Router>
        <MainLayout>
          <Routes>
            {/* Ruta principal - Dashboard */}
            <Route path="/" element={<Dashboard />} />
            
            {/* Gestión de equipos */}
            <Route path="/teams" element={<Teams />} />
            <Route path="/teams/:teamId" element={<TeamDetail />} />
            
            {/* Gestión de proyectos */}
            <Route path="/projects" element={<Projects />} />
            <Route path="/projects/:projectId" element={<ProjectDetail />} />
            
            {/* Control de carga de trabajo */}
            <Route path="/workload" element={<Workload />} />
            
            {/* Configuración */}
            <Route path="/settings" element={<Settings />} />
            
            {/* Redirección por defecto */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </MainLayout>
      </Router>

      {/* Notificaciones toast */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#1f2937',
            color: '#f9fafb',
            fontSize: '14px',
            borderRadius: '8px',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
          },
          success: {
            iconTheme: {
              primary: '#10b981',
              secondary: '#f9fafb',
            },
          },
          error: {
            iconTheme: {
              primary: '#ef4444',
              secondary: '#f9fafb',
            },
          },
        }}
      />
    </div>
  )
}

export default App