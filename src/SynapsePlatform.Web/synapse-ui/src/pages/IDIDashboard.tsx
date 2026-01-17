import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Gauge, AlertTriangle, TrendingUp, RefreshCw } from 'lucide-react'

const components = [
  { id: '1', name: 'Edge Processing Module', type: 'Firmware', idi: 1.2, status: 'Healthy', daysSinceIntegration: 2, loc: 1200, deps: 3 },
  { id: '2', name: 'Cloud Gateway', type: 'Software', idi: 4.5, status: 'Warning', daysSinceIntegration: 5, loc: 3400, deps: 8 },
  { id: '3', name: 'Sensor Driver', type: 'Hardware', idi: 0.8, status: 'Healthy', daysSinceIntegration: 1, loc: 800, deps: 2 },
  { id: '4', name: 'Data Pipeline', type: 'Software', idi: 2.1, status: 'Healthy', daysSinceIntegration: 3, loc: 2100, deps: 5 },
  { id: '5', name: 'ML Inference Engine', type: 'Software', idi: 5.8, status: 'Critical', daysSinceIntegration: 8, loc: 4500, deps: 12 },
]

const statusColors: Record<string, string> = {
  Healthy: 'badge-healthy',
  Warning: 'badge-warning',
  Critical: 'badge-critical',
}

export default function IDIDashboard() {
  const { id } = useParams()
  const avgIDI = components.reduce((sum, c) => sum + c.idi, 0) / components.length

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link to={`/projects/${id}`} className="p-2 hover:bg-gray-100 rounded-lg">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Integration Debt Index</h1>
            <p className="text-gray-500">Monitor integration health</p>
          </div>
        </div>
        <button className="btn btn-secondary">
          <RefreshCw className="w-4 h-4 mr-2" />
          Recalculate
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card bg-gradient-to-br from-synapse-50 to-white">
          <div className="flex items-center">
            <Gauge className="w-10 h-10 text-synapse-600" />
            <div className="ml-4">
              <p className="text-sm text-gray-500">Project IDI</p>
              <p className="text-3xl font-bold text-gray-900">{avgIDI.toFixed(1)}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <AlertTriangle className="w-10 h-10 text-yellow-500" />
            <div className="ml-4">
              <p className="text-sm text-gray-500">Components at Risk</p>
              <p className="text-3xl font-bold text-gray-900">
                {components.filter(c => c.status !== 'Healthy').length}
              </p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <TrendingUp className="w-10 h-10 text-green-500" />
            <div className="ml-4">
              <p className="text-sm text-gray-500">Healthy Components</p>
              <p className="text-3xl font-bold text-gray-900">
                {components.filter(c => c.status === 'Healthy').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="mb-4">
          <h3 className="font-semibold">IDI Formula</h3>
          <code className="text-sm bg-gray-100 px-2 py-1 rounded">
            IDI = (Days Since Last Integration) x (LoC Changed / 1000) x (Dependencies / 10)
          </code>
        </div>
      </div>

      <div className="card">
        <h3 className="font-semibold mb-4">Components</h3>
        <table className="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Component</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">IDI</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Days</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">LoC</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Deps</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {components.map((comp) => (
              <tr key={comp.id} className="hover:bg-gray-50">
                <td className="px-4 py-4 font-medium text-gray-900">{comp.name}</td>
                <td className="px-4 py-4 text-sm text-gray-500">{comp.type}</td>
                <td className="px-4 py-4 font-bold">{comp.idi.toFixed(1)}</td>
                <td className="px-4 py-4">
                  <span className={`badge ${statusColors[comp.status]}`}>{comp.status}</span>
                </td>
                <td className="px-4 py-4 text-sm">{comp.daysSinceIntegration}</td>
                <td className="px-4 py-4 text-sm">{comp.loc}</td>
                <td className="px-4 py-4 text-sm">{comp.deps}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
