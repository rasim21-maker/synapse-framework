import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Gauge, Clock, Users, Cpu, Shield, Calendar } from 'lucide-react'

export default function ProjectDetail() {
  const { id } = useParams()
  
  const project = {
    id: id,
    name: 'SmartFactory AI',
    code: 'SFA-001',
    description: 'Industrial IoT platform with AI-powered predictive maintenance',
    currentPhase: 'Development',
    idi: 1.8,
    idiStatus: 'Healthy',
    budget: { planned: 500000, actual: 325000 },
    dates: { start: '2025-01-01', end: '2026-06-30' }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Link to="/projects" className="p-2 hover:bg-gray-100 rounded-lg">
          <ArrowLeft className="w-5 h-5" />
        </Link>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{project.name}</h1>
          <p className="text-gray-500">{project.code}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card">
          <div className="flex items-center">
            <Gauge className="w-8 h-8 text-green-600" />
            <div className="ml-3">
              <p className="text-sm text-gray-500">Project IDI</p>
              <p className="text-xl font-bold">{project.idi}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <Clock className="w-8 h-8 text-synapse-600" />
            <div className="ml-3">
              <p className="text-sm text-gray-500">Current Phase</p>
              <p className="text-xl font-bold">{project.currentPhase}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="font-semibold mb-4">Quick Actions</h3>
          <div className="space-y-2">
            <Link to={`/projects/${id}/workitems`} className="block p-3 rounded-lg hover:bg-gray-50 border">
              View Backlog
            </Link>
            <Link to={`/projects/${id}/sprints`} className="block p-3 rounded-lg hover:bg-gray-50 border">
              Sprint Board
            </Link>
            <Link to={`/projects/${id}/idi`} className="block p-3 rounded-lg hover:bg-gray-50 border">
              IDI Dashboard
            </Link>
            <Link to={`/projects/${id}/components`} className="block p-3 rounded-lg hover:bg-gray-50 border">
              Components
            </Link>
          </div>
        </div>
        <div className="card">
          <h3 className="font-semibold mb-4">Project Info</h3>
          <p className="text-gray-600">{project.description}</p>
        </div>
      </div>
    </div>
  )
}
