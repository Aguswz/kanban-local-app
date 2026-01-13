// 🏗️ Tipos principales de la aplicación

export interface User {
  id: string
  name: string
  email: string
  avatar?: string
  role: UserRole
  skills: string[]
  capacity: number // Horas por día
  availability: Availability[]
  timezone: string
}

export interface Team {
  id: string
  name: string
  description?: string
  color: string
  members: TeamMember[]
  projects: string[] // IDs de proyectos
  wipLimits: WipLimits
  settings: TeamSettings
  createdAt: string
  updatedAt: string
}

export interface TeamMember {
  userId: string
  role: TeamRole
  joinedAt: string
  capacity: number // Override de capacidad para este equipo
  isActive: boolean
}

export interface Project {
  id: string
  name: string
  description?: string
  status: ProjectStatus
  priority: Priority
  teamIds: string[]
  startDate?: string
  endDate?: string
  estimatedHours?: number
  actualHours?: number
  progress: number // 0-100
  tags: string[]
  dependencies: string[] // IDs de otros proyectos
  createdAt: string
  updatedAt: string
}

export interface Card {
  id: string
  title: string
  description?: string
  type: CardType
  priority: Priority
  status: CardStatus
  projectId: string
  teamId: string
  assignedTo?: string
  estimatedHours?: number
  actualHours?: number
  storyPoints?: number
  tags: string[]
  dependencies: string[]
  blockedReason?: string
  acceptanceCriteria: string[]
  comments: Comment[]
  attachments: Attachment[]
  createdAt: string
  updatedAt: string
  startedAt?: string
  completedAt?: string
}

export interface Board {
  id: string
  name: string
  teamId: string
  projectId?: string
  columns: Column[]
  wipLimits: WipLimits
  settings: BoardSettings
}

export interface Column {
  id: string
  name: string
  type: ColumnType
  position: number
  wipLimit?: number
  cards: Card[]
}

export interface Comment {
  id: string
  content: string
  authorId: string
  createdAt: string
  updatedAt?: string
}

export interface Attachment {
  id: string
  name: string
  url: string
  type: string
  size: number
  uploadedBy: string
  uploadedAt: string
}

export interface Availability {
  date: string
  hours: number
  note?: string
}

export interface WorkloadData {
  userId: string
  teamId: string
  date: string
  plannedHours: number
  actualHours: number
  capacity: number
  utilization: number // 0-1
  overloaded: boolean
}

export interface Metric {
  id: string
  name: string
  value: number
  unit: string
  trend: 'up' | 'down' | 'stable'
  change: number
  period: string
}

export interface Risk {
  id: string
  title: string
  description: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  probability: number // 0-1
  impact: number // 0-1
  category: RiskCategory
  affectedTeams: string[]
  affectedProjects: string[]
  mitigation?: string
  owner?: string
  status: 'open' | 'mitigating' | 'resolved'
  detectedAt: string
  resolvedAt?: string
}

export interface AIInsight {
  id: string
  type: InsightType
  title: string
  description: string
  severity: 'info' | 'warning' | 'critical'
  confidence: number // 0-1
  recommendations: string[]
  affectedEntities: {
    teams?: string[]
    projects?: string[]
    users?: string[]
  }
  createdAt: string
  acknowledged: boolean
}

export interface AIAction {
  type: AIActionType
  payload: Record<string, any>
  explanation: string
  confidence: number
}

export interface AIResponse {
  analysis: string
  insights: AIInsight[]
  actions: AIAction[]
  recommendations: string[]
  risks: Risk[]
  timestamp: string
}

// Enums y tipos de unión
export type UserRole = 'admin' | 'manager' | 'member'
export type TeamRole = 'lead' | 'developer' | 'designer' | 'qa' | 'po' | 'sm'
export type ProjectStatus = 'planning' | 'active' | 'on_hold' | 'completed' | 'cancelled'
export type Priority = 'critical' | 'high' | 'medium' | 'low'
export type CardType = 'epic' | 'story' | 'task' | 'bug' | 'improvement'
export type CardStatus = 'backlog' | 'ready' | 'in_progress' | 'review' | 'blocked' | 'done'
export type ColumnType = 'backlog' | 'ready' | 'in_progress' | 'review' | 'blocked' | 'done'
export type RiskCategory = 'technical' | 'resource' | 'timeline' | 'quality' | 'external'
export type InsightType = 'bottleneck' | 'overload' | 'underutilization' | 'dependency' | 'quality' | 'timeline'
export type AIActionType = 
  | 'CREATE_CARD' 
  | 'MOVE_CARD' 
  | 'UPDATE_CARD' 
  | 'REASSIGN_WORK' 
  | 'ADJUST_CAPACITY' 
  | 'SUGGEST_PRIORITY' 
  | 'DETECT_RISK'
  | 'OPTIMIZE_FLOW'

export interface WipLimits {
  ready?: number
  inProgress?: number
  review?: number
  total?: number
}

export interface TeamSettings {
  workingHours: {
    start: string
    end: string
  }
  workingDays: number[]
  timezone: string
  notifications: {
    wipExceeded: boolean
    blockedCards: boolean
    overdueCards: boolean
  }
}

export interface BoardSettings {
  autoMove: boolean
  showMetrics: boolean
  groupBy: 'assignee' | 'priority' | 'type' | 'none'
  cardSize: 'compact' | 'normal' | 'detailed'
}

// Tipos para vistas y filtros
export interface ViewFilter {
  teams?: string[]
  projects?: string[]
  users?: string[]
  priorities?: Priority[]
  statuses?: CardStatus[]
  types?: CardType[]
  dateRange?: {
    start: string
    end: string
  }
}

export interface DashboardConfig {
  layout: 'grid' | 'list'
  widgets: DashboardWidget[]
  refreshInterval: number
}

export interface DashboardWidget {
  id: string
  type: 'metrics' | 'workload' | 'risks' | 'timeline' | 'kanban'
  title: string
  size: 'small' | 'medium' | 'large'
  position: { x: number; y: number }
  config: Record<string, any>
}

// Tipos para comunicación con backend
export interface APIResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
  timestamp: string
}

export interface PaginatedResponse<T> extends APIResponse<T[]> {
  pagination: {
    page: number
    limit: number
    total: number
    pages: number
  }
}

// Tipos para el store global
export interface AppState {
  user: User | null
  teams: Team[]
  projects: Project[]
  boards: Board[]
  currentView: string
  filters: ViewFilter
  loading: boolean
  error: string | null
}

// Tipos para configuración de la aplicación
export interface AppConfig {
  theme: 'light' | 'dark' | 'system'
  language: string
  notifications: boolean
  autoSave: boolean
  backupInterval: number
  aiProvider: 'openai' | 'anthropic' | 'local'
  aiApiKey?: string
}