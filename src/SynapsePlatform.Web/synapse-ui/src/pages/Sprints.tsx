import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Play, Check, Calendar } from 'lucide-react'

const sprints = [
  { id: '1', name: 'Sprint 8', goal: 'Complete sensor integration', startDate: '2025-01-06', endDate: '2025-01-20', isActive: true, planned: 34, completed: 21 },
  { id: '2', name: 'Sprint 7', goal: 'Edge processing foundation', startDate: '2024-12-23', endDate: '2025-01-05', isActive: false, planned: 30, completed: 28 },
  { id: '3', name: 'Sprint 6', goal: 'API gateway setup', startDate: '2024-12-09', endDate: '2024-12-22', isActive: false, planned: 32, completed: 32 },
]

export default function Sprints() {
  const { id } = useParams()

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link to={`/projects/${id}`} className="p-2 hover:bg-gray-100 rounded-lg">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Sprints</h1>
            <p className="text-gray-500">Manage sprint cycles</p>
          </div>
        </div>
        <button className="btn btn-primary">
          <Play className="w-4 h-4 mr-2" />
          New Sprint
        </button>
      </div>

      <div className="space-y-4">
        {sprints.map((sprint) => (
          <div key={sprint.id} className={`card ${sprint.isActive ? 'ring-2 ring-synapse-500' : ''}`}>
            <div className="flex items-center justify-between">
              <div>
                <div className="flex items-center">
                  <h3 className="font-semibold text-gray-900">{sprint.name}</h3>
                  {sprint.isActive && (
                    <span className="ml-2 badge bg-synapse-100 text-synapse-800">Active</span>
                  )}
                </div>
                <p className="text-sm text-gray-500 mt-1">{sprint.goal}</p>
                <div className="flex items-center mt-2 text-sm text-gray-500">
                  <Calendar className="w-4 h-4 mr-1" />
                  <span>{sprint.startDate} - {sprint.endDate}</span>
                </div>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-gray-900">{sprint.completed}/{sprint.planned}</p>
                <p className="text-sm text-gray-500">Story Points</p>
                <div className="mt-2 w-32 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-synapse-600 h-2 rounded-full" 
                    style={{ width: `${(sprint.completed / sprint.planned) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
