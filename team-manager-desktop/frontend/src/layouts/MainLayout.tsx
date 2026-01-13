import React, { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Users, 
  FolderOpen, 
  BarChart3, 
  Settings,
  Brain,
  AlertTriangle,
  Menu,
  X,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'

import Sidebar from '../components/layout/Sidebar'
import Header from '../components/layout/Header'
import AIAssistant from '../components/ai/AIAssistant'
import NotificationCenter from '../components/layout/NotificationCenter'
import { useAppStore } from '../store/appStore'

interface MainLayoutProps {
  children: React.ReactNode
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const location = useLocation()
  const { 
    sidebarCollapsed, 
    setSidebarCollapsed,
    aiAssistantOpen,
    setAIAssistantOpen,
    risks,
    insights,
    currentView
  } = useAppStore()

  // Detectar vista actual basada en la ruta
  useEffect(() => {
    const path = location.pathname
    let view = 'dashboard'
    
    if (path.startsWith('/teams')) view = 'teams'
    else if (path.startsWith('/projects')) view = 'projects'
    else if (path.startsWith('/workload')) view = 'workload'
    else if (path.startsWith('/settings')) view = 'settings'
    
    useAppStore.getState().setCurrentView(view)
  }, [location.pathname])

  // Escuchar eventos personalizados del menú de Electron
  useEffect(() => {
    const handleOpenAIAssistant = () => setAIAssistantOpen(true)
    const handleGlobalAnalysis = () => {
      setAIAssistantOpen(true)
      // Trigger análisis global
      setTimeout(() => {
        useAppStore.getState().requestGlobalAnalysis()
      }, 100)
    }
    const handleDetectRisks = () => {
      setAIAssistantOpen(true)
      setTimeout(() => {
        useAppStore.getState().requestRiskDetection()
      }, 100)
    }
    const handleOptimizeFlow = () => {
      setAIAssistantOpen(true)
      setTimeout(() => {
        useAppStore.getState().requestFlowOptimization()
      }, 100)
    }

    document.addEventListener('open-ai-assistant', handleOpenAIAssistant)
    document.addEventListener('ai-global-analysis', handleGlobalAnalysis)
    document.addEventListener('ai-detect-risks', handleDetectRisks)
    document.addEventListener('ai-optimize-flow', handleOptimizeFlow)

    return () => {
      document.removeEventListener('open-ai-assistant', handleOpenAIAssistant)
      document.removeEventListener('ai-global-analysis', handleGlobalAnalysis)
      document.removeEventListener('ai-detect-risks', handleDetectRisks)
      document.removeEventListener('ai-optimize-flow', handleOptimizeFlow)
    }
  }, [setAIAssistantOpen])

  // Calcular alertas críticas
  const criticalAlerts = [
    ...risks.filter(risk => risk.severity === 'critical' && risk.status === 'open'),
    ...insights.filter(insight => insight.severity === 'critical' && !insight.acknowledged)
  ]

  return (
    <div className="flex h-screen bg-secondary-50 overflow-hidden">
      {/* Sidebar */}
      <div className={`
        ${sidebarCollapsed ? 'w-16' : 'w-64'} 
        transition-all duration-300 ease-in-out
        bg-white border-r border-secondary-200 
        flex flex-col shadow-soft
      `}>
        <Sidebar collapsed={sidebarCollapsed} />
      </div>

      {/* Contenido principal */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <Header 
          onToggleSidebar={() => setSidebarCollapsed(!sidebarCollapsed)}
          onOpenAI={() => setAIAssistantOpen(true)}
          criticalAlertsCount={criticalAlerts.length}
        />

        {/* Área de contenido */}
        <main className="flex-1 overflow-hidden bg-secondary-50">
          <div className="h-full overflow-auto">
            {children}
          </div>
        </main>
      </div>

      {/* Asistente de IA - Panel lateral */}
      {aiAssistantOpen && (
        <div className="w-96 bg-white border-l border-secondary-200 shadow-strong flex flex-col">
          <AIAssistant onClose={() => setAIAssistantOpen(false)} />
        </div>
      )}

      {/* Centro de notificaciones flotante */}
      <NotificationCenter />
    </div>
  )
}

export default MainLayout