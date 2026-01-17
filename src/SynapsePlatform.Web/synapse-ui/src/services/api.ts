import axios from 'axios';
import type {
  Project,
  ProjectDashboard,
  WorkItem,
  CreateWorkItem,
  Sprint,
  Component,
  QualityGate,
  IntegrationRecord,
} from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Projects
export const projectsApi = {
  getAll: (portfolioId?: string) =>
    api.get<Project[]>('/projects', { params: { portfolioId } }),

  getById: (id: string) =>
    api.get<Project>(`/projects/${id}`),

  getDashboard: (id: string) =>
    api.get<ProjectDashboard>(`/projects/${id}/dashboard`),

  create: (data: Partial<Project>) =>
    api.post<Project>('/projects', data),

  update: (id: string, data: Partial<Project>) =>
    api.put(`/projects/${id}`, data),

  advancePhase: (id: string, newPhase: string) =>
    api.post(`/projects/${id}/advance-phase`, JSON.stringify(newPhase)),
};

// Work Items
export const workItemsApi = {
  getByProject: (projectId: string) =>
    api.get<WorkItem[]>('/workitems', { params: { projectId } }),

  getBySprint: (sprintId: string) =>
    api.get<WorkItem[]>('/workitems', { params: { sprintId } }),

  getByAssignee: (assigneeId: string) =>
    api.get<WorkItem[]>('/workitems', { params: { assigneeId } }),

  getById: (id: string) =>
    api.get<WorkItem>(`/workitems/${id}`),

  create: (data: CreateWorkItem) =>
    api.post<WorkItem>('/workitems', data),

  update: (id: string, data: Partial<WorkItem>) =>
    api.put(`/workitems/${id}`, data),

  updateStatus: (id: string, status: string) =>
    api.patch(`/workitems/${id}/status`, JSON.stringify(status)),

  assign: (id: string, assigneeId: string | null) =>
    api.patch(`/workitems/${id}/assign`, JSON.stringify(assigneeId)),

  delete: (id: string) =>
    api.delete(`/workitems/${id}`),
};

// Sprints
export const sprintsApi = {
  getByProject: (projectId: string) =>
    api.get<Sprint[]>('/sprints', { params: { projectId } }),

  getActive: (projectId: string) =>
    api.get<Sprint>('/sprints/active', { params: { projectId } }),

  getMetrics: (id: string) =>
    api.get(`/sprints/${id}/metrics`),

  create: (data: Partial<Sprint> & { projectId: string }) =>
    api.post<Sprint>('/sprints', data),

  start: (id: string) =>
    api.post(`/sprints/${id}/start`),

  complete: (id: string, data: { whatWentWell?: string; whatToImprove?: string }) =>
    api.post(`/sprints/${id}/complete`, data),
};

// Components
export const componentsApi = {
  getByProject: (projectId: string) =>
    api.get<Component[]>('/components', { params: { projectId } }),

  getById: (id: string) =>
    api.get<Component>(`/components/${id}`),

  create: (data: Partial<Component> & { projectId: string }) =>
    api.post<Component>('/components', data),

  update: (id: string, data: Partial<Component>) =>
    api.put(`/components/${id}`, data),

  reportChanges: (id: string, linesChanged: number) =>
    api.post<Component>(`/components/${id}/report-changes`, linesChanged),
};

// Integrations
export const integrationsApi = {
  getByProject: (projectId: string) =>
    api.get<IntegrationRecord[]>('/integrations', { params: { projectId } }),

  record: (data: { projectId: string; componentIds: string[]; description?: string }) =>
    api.post<IntegrationRecord>('/integrations', data),

  getProjectIDI: (projectId: string) =>
    api.get(`/integrations/project/${projectId}/idi`),

  getComponentIDIs: (projectId: string) =>
    api.get(`/integrations/project/${projectId}/component-idi`),
};

// Quality Gates
export const qualityGatesApi = {
  getByProject: (projectId: string) =>
    api.get<QualityGate[]>('/qualitygates', { params: { projectId } }),

  getById: (id: string) =>
    api.get<QualityGate>(`/qualitygates/${id}`),

  create: (data: Partial<QualityGate> & { projectId: string }) =>
    api.post<QualityGate>('/qualitygates', data),

  check: (id: string, actualValue: number) =>
    api.post(`/qualitygates/${id}/check`, actualValue),

  checkAll: (projectId: string) =>
    api.post(`/qualitygates/project/${projectId}/check-all`),

  canCommit: (projectId: string, commitHash: string) =>
    api.get(`/qualitygates/project/${projectId}/can-commit`, { params: { commitHash } }),

  canDeploy: (projectId: string) =>
    api.get(`/qualitygates/project/${projectId}/can-deploy`),

  toggle: (id: string) =>
    api.patch(`/qualitygates/${id}/toggle`),
};

export default api;
