import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Plus,
  Search,
  Filter,
  MoreVertical,
  FolderKanban,
  Gauge
} from 'lucide-react'
import type { Project, ProjectArchetype, ProjectPhase } from '../types'

// Demo data
const demoProjects: Project[] = [
  {
    id: '1',
    name: 'SmartFactory AI',
    code: 'SFA-001',
    description: 'Industrial IoT platform with AI-powered predictive maintenance',
    archetype: 'IoTEcosystem' as ProjectArchetype,
    currentPhase: 'Development' as ProjectPhase,
    targetMaturityLevel: 2,
    plannedStartDate: '2025-01-01',
    plannedEndDate: '2026-06-30',
    currentIDI: 1.8,
    idiStatus: 'Healthy' as const,
    plannedBudget: 500000,
    actualBudget: 325000,
    projectManagerName: 'John Smith',
    componentCount: 8,
    workItemCount: 156,
  },
  {
    id: '2',
    name: 'IoT Gateway Platform',
    code: 'IGP-001',
    description: 'Universal gateway for connecting edge devices to cloud',
    archetype: 'EmbeddedSystem' as ProjectArchetype,
    currentPhase: 'Integration' as ProjectPhase,
    targetMaturityLevel: 2,
    plannedStartDate: '2024-09-01',
    plannedEndDate: '2025-12-31',
    currentIDI: 4.2,
    idiStatus: 'Warning' as const,
    plannedBudget: 350000,
    actualBudget: 290000,
    projectManagerName: 'Sarah Johnson',
    componentCount: 5,
    workItemCount: 89,
  },
  {
    id: '3',
    name: 'Edge Computing Module',
    code: 'ECM-001',
    description: 'Low-power edge computing module for real-time analytics',
    archetype: 'HardwareSoftware' as ProjectArchetype,
    currentPhase: 'Architecture' as ProjectPhase,
    targetMaturityLevel: 1,
    plannedStartDate: '2025-03-01',
    plannedEndDate: '2025-09-30',
    currentIDI: 0.5,
    idiStatus: 'Healthy' as const,
    plannedBudget: 200000,
    actualBudget: 45000,
    projectManagerName: 'Mike Wilson',
    componentCount: 4,
    workItemCount: 42,
  },
]

function getIDIBadgeClass(status: string) {
  switch (status) {
    case 'Healthy':
      return 'badge-healthy'
    case 'Warning':
      return 'badge-warning'
    case 'Critical':
      return 'badge-critical'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

function getPhaseBadgeClass(phase: string) {
  const colors: Record<string, string> = {
    Initiation: 'bg-gray-100 text-gray-800',
    Discovery: 'bg-blue-100 text-blue-800',
    Architecture: 'bg-purple-100 text-purple-800',
    Development: 'bg-synapse-100 text-synapse-800',
    Integration: 'bg-yellow-100 text-yellow-800',
    Validation: 'bg-orange-100 text-orange-800',
    Deployment: 'bg-green-100 text-green-800',
    Operations: 'bg-teal-100 text-teal-800',
    Closure: 'bg-gray-100 text-gray-800',
  }
  return colors[phase] || 'bg-gray-100 text-gray-800'
}

export default function Projects() {
  const [searchQuery, setSearchQuery] = useState('')
  const [showNewProjectModal, setShowNewProjectModal] = useState(false)

  const filteredProjects = demoProjects.filter(
    (p) =>
      p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.code.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Projects</h1>
          <p className="mt-1 text-gray-500">
            Manage your SYNAPSE projects
          </p>
        </div>
        <button
          onClick={() => setShowNewProjectModal(true)}
          className="btn btn-primary flex items-center"
        >
          <Plus className="w-4 h-4 mr-2" />
          New Project
        </button>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search projects..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input pl-10"
          />
        </div>
        <button className="btn btn-secondary flex items-center">
          <Filter className="w-4 h-4 mr-2" />
          Filters
        </button>
      </div>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProjects.map((project) => (
          <Link
            key={project.id}
            to={`/projects/${project.id}`}
            className="card hover:shadow-lg transition-shadow"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center">
                <div className="p-2 rounded-lg bg-synapse-100">
                  <FolderKanban className="w-5 h-5 text-synapse-600" />
                </div>
                <div className="ml-3">
                  <h3 className="font-semibold text-gray-900">{project.name}</h3>
                  <p className="text-sm text-gray-500">{project.code}</p>
                </div>
              </div>
              <button
                onClick={(e) => {
                  e.preventDefault()
                  // Handle menu
                }}
                className="p-1 rounded hover:bg-gray-100"
              >
                <MoreVertical className="w-4 h-4 text-gray-400" />
              </button>
            </div>

            <p className="mt-3 text-sm text-gray-600 line-clamp-2">
              {project.description}
            </p>

            <div className="mt-4 flex flex-wrap gap-2">
              <span className={`badge ${getPhaseBadgeClass(project.currentPhase)}`}>
                {project.currentPhase}
              </span>
              <span className={`badge ${getIDIBadgeClass(project.idiStatus)}`}>
                <Gauge className="w-3 h-3 mr-1" />
                IDI: {project.currentIDI.toFixed(1)}
              </span>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Components</span>
                <span className="font-medium">{project.componentCount}</span>
              </div>
              <div className="flex justify-between text-sm mt-1">
                <span className="text-gray-500">Work Items</span>
                <span className="font-medium">{project.workItemCount}</span>
              </div>
              {project.projectManagerName && (
                <div className="flex justify-between text-sm mt-1">
                  <span className="text-gray-500">Manager</span>
                  <span className="font-medium">{project.projectManagerName}</span>
                </div>
              )}
            </div>
          </Link>
        ))}
      </div>

      {filteredProjects.length === 0 && (
        <div className="text-center py-12">
          <FolderKanban className="w-12 h-12 mx-auto text-gray-400" />
          <h3 className="mt-4 text-lg font-medium text-gray-900">No projects found</h3>
          <p className="mt-2 text-gray-500">
            {searchQuery
              ? 'Try adjusting your search query'
              : 'Get started by creating a new project'}
          </p>
          <button
            onClick={() => setShowNewProjectModal(true)}
            className="mt-4 btn btn-primary"
          >
            <Plus className="w-4 h-4 mr-2" />
            Create Project
          </button>
        </div>
      )}
    </div>
  )
}
