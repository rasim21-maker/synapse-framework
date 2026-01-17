import { Link } from 'react-router-dom'
import {
  FolderKanban,
  Gauge,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Zap
} from 'lucide-react'

const stats = [
  { name: 'Active Projects', value: '3', icon: FolderKanban, color: 'text-synapse-600', bg: 'bg-synapse-100' },
  { name: 'Avg. Project IDI', value: '2.2', icon: Gauge, color: 'text-green-600', bg: 'bg-green-100' },
  { name: 'Open Work Items', value: '287', icon: Clock, color: 'text-yellow-600', bg: 'bg-yellow-100' },
  { name: 'Completed This Week', value: '42', icon: CheckCircle2, color: 'text-blue-600', bg: 'bg-blue-100' },
]

const recentProjects = [
  { id: '1', name: 'SmartFactory AI', code: 'SFA-001', phase: 'Development', idi: 1.8, idiStatus: 'Healthy' },
  { id: '2', name: 'IoT Gateway Platform', code: 'IGP-001', phase: 'Integration', idi: 4.2, idiStatus: 'Warning' },
  { id: '3', name: 'Edge Computing Module', code: 'ECM-001', phase: 'Architecture', idi: 0.5, idiStatus: 'Healthy' },
]

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-1 text-gray-500">Welcome to SYNAPSE Platform</p>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-500">
          <Zap className="w-4 h-4 text-synapse-500" />
          <span>SCMM Level 2</span>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div key={stat.name} className="card">
            <div className="flex items-center">
              <div className={\}>
                <stat.icon className={\} />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">{stat.name}</p>
                <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Recent Projects</h2>
          <Link to="/projects" className="text-sm text-synapse-600 hover:text-synapse-700">
            View all
          </Link>
        </div>
        <table className="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Project</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Phase</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">IDI</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {recentProjects.map((project) => (
              <tr key={project.id} className="hover:bg-gray-50">
                <td className="px-4 py-4">
                  <Link to={\} className="font-medium text-gray-900">
                    {project.name}
                  </Link>
                </td>
                <td className="px-4 py-4">{project.phase}</td>
                <td className="px-4 py-4">{project.idi}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
