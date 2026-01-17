import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Plus, Filter, Search, ArrowLeft } from 'lucide-react'

const workItems = [
  { id: '1', title: 'Implement sensor data pipeline', type: 'Task', status: 'InProgress', priority: 'High', assignee: 'John Doe', storyPoints: 5 },
  { id: '2', title: 'Design edge processing module', type: 'UserStory', status: 'Ready', priority: 'Medium', assignee: 'Jane Smith', storyPoints: 8 },
  { id: '3', title: 'Fix memory leak in data collector', type: 'Bug', status: 'New', priority: 'Critical', assignee: null, storyPoints: 3 },
  { id: '4', title: 'Add authentication to API gateway', type: 'Task', status: 'Done', priority: 'High', assignee: 'Mike Johnson', storyPoints: 5 },
  { id: '5', title: 'Optimize database queries', type: 'TechnicalDebt', status: 'InProgress', priority: 'Medium', assignee: 'Sarah Wilson', storyPoints: 3 },
]

const statusColors: Record<string, string> = {
  New: 'bg-gray-100 text-gray-800',
  Ready: 'bg-blue-100 text-blue-800',
  InProgress: 'bg-yellow-100 text-yellow-800',
  Done: 'bg-green-100 text-green-800',
  Blocked: 'bg-red-100 text-red-800',
}

const priorityColors: Record<string, string> = {
  Critical: 'text-red-600',
  High: 'text-orange-600',
  Medium: 'text-yellow-600',
  Low: 'text-green-600',
}

export default function WorkItems() {
  const { id } = useParams()
  const [search, setSearch] = useState('')

  const filtered = workItems.filter(w => 
    w.title.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link to={`/projects/${id}`} className="p-2 hover:bg-gray-100 rounded-lg">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Backlog</h1>
            <p className="text-gray-500">Manage work items</p>
          </div>
        </div>
        <button className="btn btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          New Work Item
        </button>
      </div>

      <div className="flex gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search work items..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input pl-10"
          />
        </div>
        <button className="btn btn-secondary">
          <Filter className="w-4 h-4 mr-2" />
          Filter
        </button>
      </div>

      <div className="card">
        <table className="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Priority</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Assignee</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Points</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filtered.map((item) => (
              <tr key={item.id} className="hover:bg-gray-50 cursor-pointer">
                <td className="px-4 py-4">
                  <Link to={`/workitems/${item.id}`} className="font-medium text-gray-900 hover:text-synapse-600">
                    {item.title}
                  </Link>
                </td>
                <td className="px-4 py-4 text-sm text-gray-500">{item.type}</td>
                <td className="px-4 py-4">
                  <span className={`badge ${statusColors[item.status]}`}>{item.status}</span>
                </td>
                <td className="px-4 py-4">
                  <span className={`font-medium ${priorityColors[item.priority]}`}>{item.priority}</span>
                </td>
                <td className="px-4 py-4 text-sm text-gray-500">{item.assignee || '-'}</td>
                <td className="px-4 py-4 text-sm font-medium">{item.storyPoints}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
