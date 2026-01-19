import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Shield, Plus, Check, X } from 'lucide-react'

const gates = [
  { id: '1', name: 'Power Budget', metric: 'power_watts', threshold: 5.0, unit: 'W', enforcement: 'Pre-commit', action: 'Reject', active: true, lastResult: true },
  { id: '2', name: 'Latency Threshold', metric: 'latency_ms', threshold: 100, unit: 'ms', enforcement: 'Build Pipeline', action: 'Fail Build', active: true, lastResult: true },
  { id: '3', name: 'Memory Limit', metric: 'memory_mb', threshold: 512, unit: 'MB', enforcement: 'Build Pipeline', action: 'Warn', active: true, lastResult: false },
  { id: '4', name: 'Code Coverage', metric: 'coverage_pct', threshold: 80, unit: '%', enforcement: 'Pull Request', action: 'Block Merge', active: false, lastResult: null },
]

export default function QualityGates() {
  const { id } = useParams()

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link to={`/projects/${id}`} className="p-2 hover:bg-gray-100 rounded-lg">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Quality Gates</h1>
            <p className="text-gray-500">Policy-as-Code enforcement</p>
          </div>
        </div>
        <button className="btn btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          Add Gate
        </button>
      </div>

      <div className="card bg-synapse-50">
        <h3 className="font-semibold mb-2">About Quality Gates</h3>
        <p className="text-sm text-gray-600">
          Quality gates enforce physical constraints (power, thermal, latency) at commit time.
          They ensure hardware-software co-design constraints are never violated.
        </p>
      </div>

      <div className="grid gap-4">
        {gates.map((gate) => (
          <div key={gate.id} className={`card ${!gate.active ? 'opacity-60' : ''}`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Shield className={`w-8 h-8 ${gate.active ? 'text-synapse-600' : 'text-gray-400'}`} />
                <div className="ml-4">
                  <h3 className="font-semibold text-gray-900">{gate.name}</h3>
                  <p className="text-sm text-gray-500">
                    {gate.metric} &lt; {gate.threshold} {gate.unit}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">{gate.enforcement}</p>
                  <p className="text-xs text-gray-500">{gate.action}</p>
                </div>
                {gate.lastResult !== null && (
                  <div className={`p-2 rounded-full ${gate.lastResult ? 'bg-green-100' : 'bg-red-100'}`}>
                    {gate.lastResult ? (
                      <Check className="w-5 h-5 text-green-600" />
                    ) : (
                      <X className="w-5 h-5 text-red-600" />
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
