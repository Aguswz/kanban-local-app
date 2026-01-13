import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { 
  AppState, 
  User, 
  Team, 
  Project, 
  Board, 
  ViewFilter,
  AppConfig,
  AIInsight,
  Risk,
  WorkloadData 
} from '../types'
import { apiService } from '../services/api'

interface AppStore extends AppState {
  // Estado de configuración
  config: AppConfig
  
  // Estado de UI
  sidebarCollapsed: boolean
  aiAssistantOpen: boolean
  
  // Datos en tiempo real
  insights: AIInsight[]
  risks: Risk[]
  workloadData: WorkloadData[]
  
  // Actions - Inicialización
  initializeApp: () => Promise<void>
  
  // Actions - Usuario
  setUser: (user: User | null) => void
  
  // Actions - Equipos
  setTeams: (teams: Team[]) => void
  addTeam: (team: Team) => void
  updateTeam: (teamId: string, updates: Partial<Team>) => void
  removeTeam: (teamId: string) => void
  
  // Actions - Proyectos
  setProjects: (projects: Project[]) => void
  addProject: (project: Project) => void
  updateProject: (projectId: string, updates: Partial<Project>) => void
  removeProject: (projectId: string) => void
  
  // Actions - Tableros
  setBoards: (boards: Board[]) => void
  addBoard: (board: Board) => void
  updateBoard: (boardId: string, updates: Partial<Board>) => void
  removeBoard: (boardId: string) => void
  
  // Actions - Vista y filtros
  setCurrentView: (view: string) => void
  setFilters: (filters: Partial<ViewFilter>) => void
  clearFilters: () => void
  
  // Actions - UI
  setSidebarCollapsed: (collapsed: boolean) => void
  setAIAssistantOpen: (open: boolean) => void
  
  // Actions - Estado
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  
  // Actions - Configuración
  updateConfig: (updates: Partial<AppConfig>) => void
  
  // Actions - Datos en tiempo real
  setInsights: (insights: AIInsight[]) => void
  setRisks: (risks: Risk[]) => void
  setWorkloadData: (data: WorkloadData[]) => void
  
  // Actions - Análisis IA
  requestGlobalAnalysis: () => Promise<void>
  requestRiskDetection: () => Promise<void>
  requestFlowOptimization: () => Promise<void>
  
  // Getters computados
  getTeamById: (teamId: string) => Team | undefined
  getProjectById: (projectId: string) => Project | undefined
  getBoardById: (boardId: string) => Board | undefined
  getActiveProjects: () => Project[]
  getOverloadedUsers: () => string[]
  getCriticalRisks: () => Risk[]
}

const defaultConfig: AppConfig = {
  theme: 'system',
  language: 'es',
  notifications: true,
  autoSave: true,
  backupInterval: 300, // 5 minutos
  aiProvider: 'openai',
}

const defaultFilters: ViewFilter = {
  teams: [],
  projects: [],
  users: [],
  priorities: [],
  statuses: [],
  types: [],
}

export const useAppStore = create<AppStore>()(
  persist(
    (set, get) => ({
      // Estado inicial
      user: null,
      teams: [],
      projects: [],
      boards: [],
      currentView: 'dashboard',
      filters: defaultFilters,
      loading: false,
      error: null,
      
      // Configuración
      config: defaultConfig,
      
      // UI
      sidebarCollapsed: false,
      aiAssistantOpen: false,
      
      // Datos en tiempo real
      insights: [],
      risks: [],
      workloadData: [],
      
      // Inicialización
      initializeApp: async () => {
        set({ loading: true, error: null })
        
        try {
          // Cargar datos iniciales del backend
          const [teams, projects, boards] = await Promise.all([
            apiService.getTeams(),
            apiService.getProjects(),
            apiService.getBoards(),
          ])
          
          set({
            teams,
            projects,
            boards,
            loading: false,
          })
          
          // Cargar análisis inicial de IA
          get().requestGlobalAnalysis()
          
        } catch (error) {
          console.error('Error initializing app:', error)
          set({
            error: error instanceof Error ? error.message : 'Error desconocido',
            loading: false,
          })
        }
      },
      
      // Usuario
      setUser: (user) => set({ user }),
      
      // Equipos
      setTeams: (teams) => set({ teams }),
      addTeam: (team) => set((state) => ({ teams: [...state.teams, team] })),
      updateTeam: (teamId, updates) => set((state) => ({
        teams: state.teams.map(team => 
          team.id === teamId ? { ...team, ...updates } : team
        )
      })),
      removeTeam: (teamId) => set((state) => ({
        teams: state.teams.filter(team => team.id !== teamId)
      })),
      
      // Proyectos
      setProjects: (projects) => set({ projects }),
      addProject: (project) => set((state) => ({ projects: [...state.projects, project] })),
      updateProject: (projectId, updates) => set((state) => ({
        projects: state.projects.map(project => 
          project.id === projectId ? { ...project, ...updates } : project
        )
      })),
      removeProject: (projectId) => set((state) => ({
        projects: state.projects.filter(project => project.id !== projectId)
      })),
      
      // Tableros
      setBoards: (boards) => set({ boards }),
      addBoard: (board) => set((state) => ({ boards: [...state.boards, board] })),
      updateBoard: (boardId, updates) => set((state) => ({
        boards: state.boards.map(board => 
          board.id === boardId ? { ...board, ...updates } : board
        )
      })),
      removeBoard: (boardId) => set((state) => ({
        boards: state.boards.filter(board => board.id !== boardId)
      })),
      
      // Vista y filtros
      setCurrentView: (view) => set({ currentView: view }),
      setFilters: (filters) => set((state) => ({
        filters: { ...state.filters, ...filters }
      })),
      clearFilters: () => set({ filters: defaultFilters }),
      
      // UI
      setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
      setAIAssistantOpen: (open) => set({ aiAssistantOpen: open }),
      
      // Estado
      setLoading: (loading) => set({ loading }),
      setError: (error) => set({ error }),
      
      // Configuración
      updateConfig: (updates) => set((state) => ({
        config: { ...state.config, ...updates }
      })),
      
      // Datos en tiempo real
      setInsights: (insights) => set({ insights }),
      setRisks: (risks) => set({ risks }),
      setWorkloadData: (data) => set({ workloadData: data }),
      
      // Análisis IA
      requestGlobalAnalysis: async () => {
        try {
          const analysis = await apiService.requestGlobalAnalysis()
          set({
            insights: analysis.insights,
            risks: analysis.risks,
          })
        } catch (error) {
          console.error('Error in global analysis:', error)
        }
      },
      
      requestRiskDetection: async () => {
        try {
          const risks = await apiService.detectRisks()
          set({ risks })
        } catch (error) {
          console.error('Error detecting risks:', error)
        }
      },
      
      requestFlowOptimization: async () => {
        try {
          const optimization = await apiService.optimizeFlow()
          set({
            insights: optimization.insights,
          })
        } catch (error) {
          console.error('Error optimizing flow:', error)
        }
      },
      
      // Getters
      getTeamById: (teamId) => {
        return get().teams.find(team => team.id === teamId)
      },
      
      getProjectById: (projectId) => {
        return get().projects.find(project => project.id === projectId)
      },
      
      getBoardById: (boardId) => {
        return get().boards.find(board => board.id === boardId)
      },
      
      getActiveProjects: () => {
        return get().projects.filter(project => project.status === 'active')
      },
      
      getOverloadedUsers: () => {
        const workloadData = get().workloadData
        return workloadData
          .filter(data => data.overloaded)
          .map(data => data.userId)
      },
      
      getCriticalRisks: () => {
        return get().risks.filter(risk => 
          risk.severity === 'critical' && risk.status === 'open'
        )
      },
    }),
    {
      name: 'team-manager-store',
      partialize: (state) => ({
        // Solo persistir configuración y preferencias de UI
        config: state.config,
        sidebarCollapsed: state.sidebarCollapsed,
        currentView: state.currentView,
        filters: state.filters,
      }),
    }
  )
)