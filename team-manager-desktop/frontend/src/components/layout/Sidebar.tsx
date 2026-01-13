import React from 'react'
import { NavLink } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Users, 
  FolderOpen, 
  BarChart3, 
  Settings,
  Brain,
  AlertTriangle,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'

import { useAppStore } from '../../store/appStore'

interface SidebarProps {
  collapsed: boolean
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed }) => {
  const { 
    setSidebarCollapsed,
    risks,
    insights,
    getOverloadedUsers,
    getCriticalRisks
  } = useAppStore()

  // Calcular indicadores
  const overloadedUsers = getOverloadedUsers()
  const criticalRisks = getCriticalRisks()
  const unacknowledgedInsights = insights.filter(insight => !insight.acknowledged)

  const navigationItems = [
    {
      path: '/',
      icon: LayoutDashboard,
      label: 'Dashboard',
      badge: criticalRisks.length > 0 ? criticalRisks.length : null,
      badgeColor: 'bg-danger-500'
    },
    {
      path: '/teams',
      icon: Users,
      label: 'Equipos',
      badge: overloadedUsers.length > 0 ? overloadedUsers.length : null,
      badgeColor: 'bg-warning-500'
    },
    {
      path: '/projects',
      icon: FolderOpen,
      label: 'Proyectos',
      badge: null
    },
    {
      path: '/workload',
      icon: BarChart3,
      label: 'Carga de Trabajo',
      badge: overloadedUsers.length > 0 ? '!' : null,
      badgeColor: 'bg-danger-500'
    }
  ]

  const bottomItems = [
    {
      path: '/settings',
      icon: Settings,
      label: 'Configuración'
    }
  ]

  return (
    <div className="h-full flex flex-col">
      {/* Header del sidebar */}
      <div className="p-4 border-b border-secondary-200">
        <div className="flex items-center justify-between">
          {!collapsed && (
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="font-bold text-secondary-900">Team Manager</h1>
                <p className="text-xs text-secondary-500">Director IA</p>
              </div>
            </div>
          )}
          
          <button
            onClick={() => setSidebarCollapsed(!collapsed)}
            className="p-1.5 rounded-md hover:bg-secondary-100 transition-colors"
          >
            {collapsed ? (
              <ChevronRight className="w-4 h-4 text-secondary-600" />
            ) : (
              <ChevronLeft className="w-4 h-4 text-secondary-600" />
            )}
          </button>
        </div>
      </div>

      {/* Navegación principal */}
      <nav className="flex-1 p-2">
        <div className="space-y-1">
          {navigationItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `
                flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-colors
                ${isActive 
                  ? 'bg-primary-100 text-primary-700 border-r-2 border-primary-600' 
                  : 'text-secondary-600 hover:bg-secondary-100 hover:text-secondary-900'
                }
              `}
            >
              <item.icon className={`w-5 h-5 ${collapsed ? 'mx-auto' : 'mr-3'}`} />
              
              {!collapsed && (
                <>
                  <span className="flex-1">{item.label}</span>
                  {item.badge && (
                    <span className={`
                      inline-flex items-center justify-center px-2 py-1 text-xs font-bold text-white rounded-full
                      ${item.badgeColor || 'bg-primary-500'}
                    `}>
                      {item.badge}
                    </span>
                  )}
                </>
              )}
            </NavLink>
          ))}
        </div>

        {/* Sección de alertas críticas */}
        {!collapsed && (criticalRisks.length > 0 || unacknowledgedInsights.length > 0) && (
          <div className="mt-6 p-3 bg-danger-50 border border-danger-200 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <AlertTriangle className="w-4 h-4 text-danger-600" />
              <span className="text-sm font-medium text-danger-900">Alertas Críticas</span>
            </div>
            
            {criticalRisks.length > 0 && (
              <div className="text-xs text-danger-700 mb-1">
                {criticalRisks.length} riesgo{criticalRisks.length !== 1 ? 's' : ''} crítico{criticalRisks.length !== 1 ? 's' : ''}
              </div>
            )}
            
            {unacknowledgedInsights.length > 0 && (
              <div className="text-xs text-danger-700">
                {unacknowledgedInsights.length} insight{unacknowledgedInsights.length !== 1 ? 's' : ''} sin revisar
              </div>
            )}
            
            <button 
              onClick={() => useAppStore.getState().setAIAssistantOpen(true)}
              className="mt-2 text-xs text-danger-600 hover:text-danger-800 font-medium"
            >
              Revisar con IA →
            </button>
          </div>
        )}

        {/* Indicador de estado de IA */}
        {!collapsed && (
          <div className="mt-4 p-3 bg-primary-50 border border-primary-200 rounded-lg">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-success-500 rounded-full animate-pulse"></div>
              <span className="text-xs font-medium text-primary-900">Director IA Activo</span>
            </div>
            <p className="text-xs text-primary-600 mt-1">
              Monitoreando {navigationItems.length} áreas
            </p>
          </div>
        )}
      </nav>

      {/* Navegación inferior */}
      <div className="p-2 border-t border-secondary-200">
        {bottomItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => `
              flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-colors
              ${isActive 
                ? 'bg-secondary-100 text-secondary-900' 
                : 'text-secondary-600 hover:bg-secondary-100 hover:text-secondary-900'
              }
            `}
          >
            <item.icon className={`w-5 h-5 ${collapsed ? 'mx-auto' : 'mr-3'}`} />
            {!collapsed && <span>{item.label}</span>}
          </NavLink>
        ))}
      </div>
    </div>
  )
}

export default Sidebar