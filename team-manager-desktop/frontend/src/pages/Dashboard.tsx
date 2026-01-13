import React, { useEffect, useState } from 'react'
import { 
  Users, 
  FolderOpen, 
  AlertTriangle, 
  TrendingUp,
  Clock,
  CheckCircle,
  XCircle,
  Brain,
  BarChart3,
  Activity
} from 'lucide-react'

import { useAppStore } from '../store/appStore'
import DashboardCard from '../components/dashboard/DashboardCard'
import TeamOverview from '../components/dashboard/TeamOverview'
import ProjectStatus from '../components/dashboard/ProjectStatus'
import WorkloadChart from '../components/dashboard/WorkloadChart'
import RiskAlert from '../components/dashboard/RiskAlert'
import AIInsightCard from '../components/dashboard/AIInsightCard'
import QuickActions from '../components/dashboard/QuickActions'

const Dashboard: React.FC = () => {
  const {
    teams,
    projects,
    risks,
    insights,
    workloadData,
    loading,
    requestGlobalAnalysis,
    getActiveProjects,
    getOverloadedUsers,
    getCriticalRisks,
    setAIAssistantOpen
  } = useAppStore()

  const [refreshing, setRefreshing] = useState(false)

  // Cargar datos iniciales y análisis
  useEffect(() => {
    const loadDashboardData = async () => {
      setRefreshing(true)
      try {
        await requestGlobalAnalysis()
      } finally {
        setRefreshing(false)
      }
    }

    loadDashboardData()
    
    // Refresh automático cada 5 minutos
    const interval = setInterval(loadDashboardData, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [requestGlobalAnalysis])

  // Calcular métricas principales
  const activeProjects = getActiveProjects()
  const overloadedUsers = getOverloadedUsers()
  const criticalRisks = getCriticalRisks()
  const totalUsers = teams.reduce((acc, team) => acc + team.members.length, 0)
  
  // Métricas de productividad
  const completedThisWeek = projects.filter(p => 
    p.status === 'completed' && 
    new Date(p.updatedAt) > new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
  ).length

  const avgUtilization = workloadData.length > 0 
    ? workloadData.reduce((acc, data) => acc + data.utilization, 0) / workloadData.length 
    : 0

  // Insights críticos sin reconocer
  const criticalInsights = insights.filter(insight => 
    insight.severity === 'critical' && !insight.acknowledged
  )

  if (loading && teams.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-secondary-600">Cargando dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header del Dashboard */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-secondary-900">Dashboard Ejecutivo</h1>
          <p className="text-secondary-600 mt-1">
            Vista global de {teams.length} equipos y {projects.length} proyectos
          </p>
        </div>
        
        <div className="flex items-center space-x-3">
          <button
            onClick={() => requestGlobalAnalysis()}
            disabled={refreshing}
            className="btn-secondary"
          >
            <Activity className={`w-4 h-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
            {refreshing ? 'Analizando...' : 'Actualizar'}
          </button>
          
          <button
            onClick={() => setAIAssistantOpen(true)}
            className="btn-primary"
          >
            <Brain className="w-4 h-4 mr-2" />
            Director IA
          </button>
        </div>
      </div>

      {/* Alertas críticas */}
      {(criticalRisks.length > 0 || criticalInsights.length > 0) && (
        <div className="bg-danger-50 border border-danger-200 rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-3">
            <AlertTriangle className="w-5 h-5 text-danger-600" />
            <h3 className="font-semibold text-danger-900">Atención Inmediata Requerida</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {criticalRisks.slice(0, 2).map(risk => (
              <RiskAlert key={risk.id} risk={risk} />
            ))}
            {criticalInsights.slice(0, 2).map(insight => (
              <AIInsightCard key={insight.id} insight={insight} compact />
            ))}
          </div>
        </div>
      )}

      {/* Métricas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <DashboardCard
          title="Equipos Activos"
          value={teams.length}
          icon={Users}
          color="primary"
          subtitle={`${totalUsers} miembros total`}
        />
        
        <DashboardCard
          title="Proyectos Activos"
          value={activeProjects.length}
          icon={FolderOpen}
          color="success"
          subtitle={`${completedThisWeek} completados esta semana`}
          trend={completedThisWeek > 0 ? 'up' : 'stable'}
        />
        
        <DashboardCard
          title="Utilización Promedio"
          value={`${Math.round(avgUtilization * 100)}%`}
          icon={BarChart3}
          color={avgUtilization > 0.9 ? 'warning' : avgUtilization > 0.7 ? 'success' : 'secondary'}
          subtitle={overloadedUsers.length > 0 ? `${overloadedUsers.length} sobrecargados` : 'Carga balanceada'}
          trend={overloadedUsers.length > 0 ? 'down' : 'stable'}
        />
        
        <DashboardCard
          title="Riesgos Críticos"
          value={criticalRisks.length}
          icon={AlertTriangle}
          color={criticalRisks.length > 0 ? 'danger' : 'success'}
          subtitle={criticalRisks.length > 0 ? 'Requieren atención' : 'Bajo control'}
        />
      </div>

      {/* Contenido principal */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Columna izquierda - Equipos y proyectos */}
        <div className="lg:col-span-2 space-y-6">
          {/* Overview de equipos */}
          <div className="bg-white rounded-lg border border-secondary-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-secondary-900">Estado de Equipos</h3>
              <button className="text-sm text-primary-600 hover:text-primary-700">
                Ver todos →
              </button>
            </div>
            <TeamOverview teams={teams} workloadData={workloadData} />
          </div>

          {/* Estado de proyectos */}
          <div className="bg-white rounded-lg border border-secondary-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-secondary-900">Proyectos Críticos</h3>
              <button className="text-sm text-primary-600 hover:text-primary-700">
                Ver todos →
              </button>
            </div>
            <ProjectStatus projects={activeProjects.slice(0, 5)} />
          </div>

          {/* Gráfico de carga de trabajo */}
          <div className="bg-white rounded-lg border border-secondary-200 p-6">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Carga de Trabajo Semanal</h3>
            <WorkloadChart data={workloadData} />
          </div>
        </div>

        {/* Columna derecha - IA y acciones */}
        <div className="space-y-6">
          {/* Insights de IA */}
          <div className="bg-white rounded-lg border border-secondary-200 p-6">
            <div className="flex items-center space-x-2 mb-4">
              <Brain className="w-5 h-5 text-primary-600" />
              <h3 className="text-lg font-semibold text-secondary-900">Insights del Director IA</h3>
            </div>
            
            {insights.length > 0 ? (
              <div className="space-y-3">
                {insights.slice(0, 3).map(insight => (
                  <AIInsightCard key={insight.id} insight={insight} />
                ))}
                
                {insights.length > 3 && (
                  <button 
                    onClick={() => setAIAssistantOpen(true)}
                    className="w-full text-sm text-primary-600 hover:text-primary-700 py-2"
                  >
                    Ver {insights.length - 3} insights más →
                  </button>
                )}
              </div>
            ) : (
              <div className="text-center py-8 text-secondary-500">
                <Brain className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>El Director IA está analizando...</p>
                <button 
                  onClick={() => requestGlobalAnalysis()}
                  className="text-primary-600 hover:text-primary-700 text-sm mt-2"
                >
                  Solicitar análisis
                </button>
              </div>
            )}
          </div>

          {/* Acciones rápidas */}
          <div className="bg-white rounded-lg border border-secondary-200 p-6">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">Acciones Rápidas</h3>
            <QuickActions />
          </div>

          {/* Resumen de riesgos */}
          {risks.length > 0 && (
            <div className="bg-white rounded-lg border border-secondary-200 p-6">
              <h3 className="text-lg font-semibold text-secondary-900 mb-4">Gestión de Riesgos</h3>
              <div className="space-y-3">
                {risks.slice(0, 3).map(risk => (
                  <RiskAlert key={risk.id} risk={risk} compact />
                ))}
                
                {risks.length > 3 && (
                  <button className="w-full text-sm text-primary-600 hover:text-primary-700 py-2">
                    Ver {risks.length - 3} riesgos más →
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard