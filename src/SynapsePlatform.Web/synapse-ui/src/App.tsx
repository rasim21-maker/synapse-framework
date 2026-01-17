import { Routes, Route } from 'react-router-dom'
import MainLayout from './layouts/MainLayout'
import Dashboard from './pages/Dashboard'
import Projects from './pages/Projects'
import ProjectDetail from './pages/ProjectDetail'
import WorkItems from './pages/WorkItems'
import WorkItemDetail from './pages/WorkItemDetail'
import Sprints from './pages/Sprints'
import IDIDashboard from './pages/IDIDashboard'
import QualityGates from './pages/QualityGates'
import Components from './pages/Components'

function App() {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="projects" element={<Projects />} />
        <Route path="projects/:id" element={<ProjectDetail />} />
        <Route path="projects/:id/workitems" element={<WorkItems />} />
        <Route path="projects/:id/sprints" element={<Sprints />} />
        <Route path="projects/:id/idi" element={<IDIDashboard />} />
        <Route path="projects/:id/quality-gates" element={<QualityGates />} />
        <Route path="projects/:id/components" element={<Components />} />
        <Route path="workitems/:id" element={<WorkItemDetail />} />
      </Route>
    </Routes>
  )
}

export default App
