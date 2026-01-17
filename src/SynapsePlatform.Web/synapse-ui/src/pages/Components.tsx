import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Cpu, Plus, Zap, Clock, GitBranch } from 'lucide-react'

const components = [
  { id: '1', name: 'Edge Processing Module', type: 'Firmware', idi: 1.2, status: 'Healthy', power: { budget: 5.0, actual: 3.2 } },
  { id: '2', name: 'Cloud Gateway', type: 'Software', idi: 4.5, status: 'Warning', latency: { threshold: 100, actual: 85 } },
  { id: '3', name: 'Sensor Driver', type: 'Hardware', idi: 0.8, status: 'Healthy', power: { budget: 2.0, actual: 1.5 } },
  { id: '4', name: 'Data Pipeline', type: 'Software', idi: 2.1, status: 'Healthy', memory: { limit: 512, actual: 380 } },
  { id: '5', name: 'ML Inference Engine', type: 'Software', idi: 5.8, status: 'Critical', memory: { limit: 1024, actual: 950 } },
]

const typeColors: Record<string, string> = {
  Hardware: 'bg-purple-100 text-purple-800',
  Firmware: 'bg-orange-100 text-orange-800',
  Software: 'bg-blue-100 text-blue-800',
  Infrastructure: 'bg-green-100 text-green-800',
}

const statusColors: Record<string, string> = {
  Healthy: 'badge-healthy',
  Warning: 'badge-warning',
  Critical: 'badge-critical',
}

export default function Components() {
  const { id } = useParams()

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link to={`/projects/${id}`} className="p-2 hover:bg-gray-100 rounded-lg">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Components</h1>
            <p className="text-gray-500">Hardware, Firmware, Software layers</p>
          </div>
        </div>
        <button className="btn btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          Add Component
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {components.map((comp) => (
          <div key={comp.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex items-center">
                <div className="p-2 rounded-lg bg-gray-100">
                  <Cpu className="w-5 h-5 text-gray-600" />
                </div>
                <div className="ml-3">
                  <h3 className="font-semibold text-gray-900">{comp.name}</h3>
                  <span className={`badge ${typeColors[comp.type]}`}>{comp.type}</span>
                </div>
              </div>
            </div>

            <div className="mt-4 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">IDI</span>
                <span className={`font-medium ${
                  comp.status === 'Healthy' ? 'text-green-600' :
                  comp.status === 'Warning' ? 'text-yellow-600' : 'text-red-600'
                }`}>{comp.idi.toFixed(1)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Status</span>
                <span className={`badge ${statusColors[comp.status]}`}>{comp.status}</span>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t">
              <button className="btn btn-secondary w-full text-sm">
                <GitBranch className="w-4 h-4 mr-2" />
                Record Integration
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
