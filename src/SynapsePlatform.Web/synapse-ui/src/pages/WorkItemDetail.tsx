import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, MessageSquare, Paperclip, CheckSquare } from 'lucide-react'

export default function WorkItemDetail() {
  const { id } = useParams()

  const item = {
    id,
    title: 'Implement sensor data pipeline',
    description: 'Create a data pipeline to process sensor data from IoT devices in real-time.',
    type: 'Task',
    status: 'InProgress',
    priority: 'High',
    storyPoints: 5,
    assignee: 'John Doe',
    component: 'Edge Processing',
    acceptanceCriteria: '- Data should be processed within 100ms\n- Support for at least 1000 sensors\n- Error handling for malformed data'
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <button onClick={() => window.history.back()} className="p-2 hover:bg-gray-100 rounded-lg">
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <span className="text-sm text-gray-500">{item.type}</span>
          <h1 className="text-2xl font-bold text-gray-900">{item.title}</h1>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="card">
            <h3 className="font-semibold mb-3">Description</h3>
            <p className="text-gray-600">{item.description}</p>
          </div>

          <div className="card">
            <h3 className="font-semibold mb-3">Acceptance Criteria</h3>
            <pre className="text-sm text-gray-600 whitespace-pre-wrap">{item.acceptanceCriteria}</pre>
          </div>

          <div className="card">
            <h3 className="font-semibold mb-3 flex items-center">
              <MessageSquare className="w-4 h-4 mr-2" />
              Comments
            </h3>
            <p className="text-gray-500 text-sm">No comments yet</p>
          </div>
        </div>

        <div className="space-y-6">
          <div className="card">
            <h3 className="font-semibold mb-4">Details</h3>
            <dl className="space-y-3">
              <div className="flex justify-between">
                <dt className="text-gray-500">Status</dt>
                <dd className="badge bg-yellow-100 text-yellow-800">{item.status}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Priority</dt>
                <dd className="font-medium text-orange-600">{item.priority}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Story Points</dt>
                <dd className="font-medium">{item.storyPoints}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Assignee</dt>
                <dd className="font-medium">{item.assignee}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Component</dt>
                <dd className="font-medium">{item.component}</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  )
}
