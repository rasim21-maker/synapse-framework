export type ProjectPhase = 
  | 'Initiation' | 'Discovery' | 'Architecture' | 'Development' 
  | 'Integration' | 'Validation' | 'Deployment' | 'Operations' | 'Closure'

export type ProjectArchetype = 
  | 'IoTEcosystem' | 'EmbeddedSystem' | 'HardwareSoftware' 
  | 'SaaSWithHardware' | 'MultiDisciplinary' | 'PureSoftware'

export type ComponentType = 'Hardware' | 'Firmware' | 'Software' | 'Infrastructure' | 'Cloud' | 'Edge'

export type WorkItemType = 'Epic' | 'Feature' | 'UserStory' | 'Task' | 'Bug' | 'TechnicalDebt' | 'Spike' | 'IntegrationTask'

export type WorkItemStatus = 'New' | 'Ready' | 'InProgress' | 'InReview' | 'Testing' | 'Done' | 'Blocked' | 'Cancelled'

export type Priority = 'Critical' | 'High' | 'Medium' | 'Low'

export type IDIStatus = 'Healthy' | 'Warning' | 'Critical'

export interface Project {
  id: string
  name: string
  code: string
  description?: string
  archetype: ProjectArchetype
  currentPhase: ProjectPhase
  targetMaturityLevel: number
  plannedStartDate: string
  plannedEndDate: string
  currentIDI: number
  idiStatus: IDIStatus
  plannedBudget: number
  actualBudget: number
  projectManagerName?: string
  componentCount: number
  workItemCount: number
}

export interface Sprint {
  id: string
  name: string
  goal?: string
  sprintNumber: number
  startDate: string
  endDate: string
  isActive: boolean
  isCompleted: boolean
  plannedStoryPoints: number
  completedStoryPoints: number
  workItemCount: number
}

export interface WorkItem {
  id: string
  title: string
  description?: string
  type: WorkItemType
  status: WorkItemStatus
  priority: Priority
  storyPoints?: number
  estimatedHours?: number
  dueDate?: string
  projectId: string
  sprintId?: string
  assigneeName?: string
  componentName?: string
}

export interface Component {
  id: string
  name: string
  description?: string
  type: ComponentType
  componentIDI: number
  idiStatus: IDIStatus
  daysSinceLastIntegration: number
  lastIntegrationDate?: string
  linesOfCodeChanged: number
  dependencyCount: number
  powerBudgetWatts?: number
  actualPowerWatts?: number
}

export interface IDIReport {
  projectIDI: number
  status: IDIStatus
  components: ComponentIDI[]
  trends: IDITrend[]
}

export interface ComponentIDI {
  componentId: string
  componentName: string
  idi: number
  status: IDIStatus
  daysSinceLastIntegration: number
}

export interface IDITrend {
  date: string
  idi: number
}

export interface QualityGate {
  id: string
  name: string
  metricName: string
  thresholdValue: number
  thresholdUnit?: string
  enforcement: string
  action: string
  isActive: boolean
}
