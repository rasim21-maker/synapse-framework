# SYNAPSE Platform - Project Type Selector Implementation Specification

**Version:** 1.0
**Date:** 2026-01-20
**Target:** Claude Code Implementation

---

## 1. Overview

### 1.1 Purpose
Implement a comprehensive Project Type Selector (Flavor Selector) that allows users to choose the appropriate SYNAPSE flavor when creating a new project. This selection determines the IDI formula, Quality Gates, Neural Pruning triggers, and Digital Twin configuration for the project.

### 1.2 Supported Flavors

| Flavor | Metric | Target Projects |
|--------|--------|-----------------|
| **IoT** | IDI | IoT devices, hardware-software co-design |
| **Cloud** | IDI | SaaS, microservices, cloud-native apps |
| **Embedded** | IDI | Safety-critical firmware (automotive, medical) |
| **Infra** | CDI | IaC, Terraform, Kubernetes, DevOps |
| **Data** | SDI | Data pipelines, ETL, ML platforms |
| **Mobile** | IDI | iOS/Android native and cross-platform apps |

---

## 2. Technical Architecture

### 2.1 Technology Stack

#### Backend (.NET 8)
```
/src
├── Synapse.Domain/
│   ├── Entities/
│   │   ├── Project.cs
│   │   ├── ProjectFlavor.cs
│   │   └── QualityGate.cs
│   └── Enums/
│       └── FlavorType.cs
├── Synapse.Application/
│   ├── Projects/
│   │   ├── Commands/
│   │   │   └── CreateProjectCommand.cs
│   │   └── Queries/
│   │       └── GetFlavorConfigQuery.cs
│   └── QualityGates/
│       └── Services/
│           └── QualityGateEvaluator.cs
├── Synapse.Infrastructure/
│   ├── Persistence/
│   │   └── Configurations/
│   │       └── ProjectConfiguration.cs
│   └── Services/
│       └── FlavorConfigurationService.cs
└── Synapse.API/
    └── Controllers/
        ├── ProjectsController.cs
        └── FlavorsController.cs
```

#### Frontend (React + TypeScript)
```
/frontend/src
├── components/
│   ├── projects/
│   │   ├── ProjectTypeSelector.tsx
│   │   ├── FlavorCard.tsx
│   │   ├── FlavorThresholdDisplay.tsx
│   │   └── CreateProjectModal.tsx
│   └── quality-gates/
│       ├── QualityGateList.tsx
│       └── GateStatusBadge.tsx
├── hooks/
│   ├── useFlavors.ts
│   └── useQualityGates.ts
├── services/
│   ├── flavorService.ts
│   └── qualityGateService.ts
├── types/
│   ├── flavor.ts
│   └── qualityGate.ts
└── store/
    └── projectSlice.ts
```

#### Database (PostgreSQL)
```sql
-- Tables
projects
project_flavors
quality_gates
quality_gate_results
neural_pruning_triggers
```

---

## 3. API Specification

### 3.1 Endpoints

#### GET /api/v1/flavors
Returns all available SYNAPSE flavors with their configurations.

**Response:**
```json
{
  "flavors": [
    {
      "type": "iot",
      "name": "SYNAPSE/IoT",
      "description": "IoT ve gömülü sistemler için kanonik implementasyon",
      "metricName": "IDI",
      "formula": "(days * loc_changed / 1000 * dependencies / 10) / 10",
      "thresholds": {
        "healthy": 3.0,
        "warning": 5.0,
        "critical": 7.0,
        "quarantine": 10.0
      },
      "icon": "microchip",
      "color": "#0ea5e9",
      "qualityGatesCount": 10,
      "categories": ["hardware", "firmware", "performance", "security"]
    }
    // ... other flavors
  ]
}
```

#### GET /api/v1/flavors/{flavorType}
Returns detailed configuration for a specific flavor.

**Response:**
```json
{
  "type": "cloud",
  "name": "SYNAPSE/Cloud",
  "description": "Bulut-native ve mikroservis mimarileri",
  "metricName": "IDI",
  "formula": "(pr_age_days * changed_files * dependent_services) / 100",
  "thresholds": {
    "healthy": 2.0,
    "warning": 4.0,
    "critical": 6.0,
    "quarantine": 8.0
  },
  "qualityGates": [
    {
      "id": "api_response_time",
      "name": "API Response Time",
      "description": "99th percentile API response time",
      "category": "performance",
      "metric": "api_p99_ms",
      "operator": "less_than",
      "threshold": 200,
      "unit": "ms",
      "severity": "high",
      "enforcement": ["canary", "production"]
    }
    // ... other gates
  ],
  "neuralPruningTriggers": [
    {
      "condition": "idi > 6.0",
      "action": "quarantine"
    }
    // ... other triggers
  ],
  "digitalTwinConfig": {
    "type": "service_mesh",
    "fidelityTarget": 0.90,
    "updateFrequencySeconds": 1000
  }
}
```

#### GET /api/v1/flavors/{flavorType}/quality-gates
Returns all quality gates for a specific flavor.

#### POST /api/v1/projects
Creates a new project with selected flavor.

**Request:**
```json
{
  "name": "Smart Factory Gateway",
  "description": "Industrial IoT gateway for factory automation",
  "flavorType": "iot",
  "teamLeadId": "user-123",
  "targetDate": "2026-06-15",
  "customThresholds": null,  // Optional: override default thresholds
  "tags": ["industrial", "iot", "gateway"]
}
```

**Response:**
```json
{
  "id": "proj-456",
  "name": "Smart Factory Gateway",
  "flavorType": "iot",
  "flavorName": "SYNAPSE/IoT",
  "metricName": "IDI",
  "currentScore": 0.0,
  "thresholds": {
    "healthy": 3.0,
    "warning": 5.0,
    "critical": 7.0,
    "quarantine": 10.0
  },
  "qualityGatesEnabled": 10,
  "createdAt": "2026-01-20T10:30:00Z"
}
```

---

## 4. Data Models

### 4.1 Backend Entities (C#)

```csharp
// FlavorType.cs
public enum FlavorType
{
    IoT = 1,
    Cloud = 2,
    Embedded = 3,
    Infra = 4,
    Data = 5,
    Mobile = 6
}

// Project.cs
public class Project
{
    public Guid Id { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public FlavorType FlavorType { get; set; }
    public ProjectFlavor FlavorConfig { get; set; }
    public Guid TeamLeadId { get; set; }
    public DateTime TargetDate { get; set; }
    public DateTime CreatedAt { get; set; }
    public decimal CurrentScore { get; set; }
    public string ScoreStatus { get; set; } // healthy, warning, critical, quarantine

    public ICollection<Component> Components { get; set; }
    public ICollection<QualityGateResult> QualityGateResults { get; set; }
}

// ProjectFlavor.cs
public class ProjectFlavor
{
    public FlavorType Type { get; set; }
    public string Name { get; set; }
    public string MetricName { get; set; } // IDI, CDI, SDI
    public string Formula { get; set; }
    public FlavorThresholds Thresholds { get; set; }
    public List<QualityGate> QualityGates { get; set; }
    public List<NeuralPruningTrigger> NeuralPruningTriggers { get; set; }
    public DigitalTwinConfig DigitalTwinConfig { get; set; }
}

// FlavorThresholds.cs
public class FlavorThresholds
{
    public decimal Healthy { get; set; }
    public decimal Warning { get; set; }
    public decimal Critical { get; set; }
    public decimal Quarantine { get; set; }
}

// QualityGate.cs
public class QualityGate
{
    public string Id { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public string Category { get; set; }
    public string Metric { get; set; }
    public string Operator { get; set; }
    public object Threshold { get; set; }
    public string Unit { get; set; }
    public string Severity { get; set; }
    public List<string> Enforcement { get; set; }
    public List<string> Components { get; set; }
    public string Platform { get; set; }
}
```

### 4.2 Frontend Types (TypeScript)

```typescript
// flavor.ts
export type FlavorType = 'iot' | 'cloud' | 'embedded' | 'infra' | 'data' | 'mobile';

export interface FlavorThresholds {
  healthy: number;
  warning: number;
  critical: number;
  quarantine: number;
}

export interface FlavorSummary {
  type: FlavorType;
  name: string;
  description: string;
  metricName: string;
  formula: string;
  thresholds: FlavorThresholds;
  icon: string;
  color: string;
  qualityGatesCount: number;
  categories: string[];
}

export interface FlavorConfig extends FlavorSummary {
  qualityGates: QualityGate[];
  neuralPruningTriggers: NeuralPruningTrigger[];
  digitalTwinConfig: DigitalTwinConfig;
}

// qualityGate.ts
export type GateSeverity = 'info' | 'low' | 'medium' | 'high' | 'critical';
export type GateOperator = 'equals' | 'less_than' | 'greater_than' | 'less_than_or_equal' | 'greater_than_or_equal';

export interface QualityGate {
  id: string;
  name: string;
  description: string;
  category: string;
  metric: string;
  operator: GateOperator;
  threshold: number | boolean | string;
  unit?: string;
  severity: GateSeverity;
  enforcement: string[];
  components?: string[];
  platform?: string;
}

// project.ts
export interface CreateProjectRequest {
  name: string;
  description?: string;
  flavorType: FlavorType;
  teamLeadId?: string;
  targetDate?: string;
  customThresholds?: Partial<FlavorThresholds>;
  tags?: string[];
}
```

---

## 5. UI Component Specifications

### 5.1 ProjectTypeSelector Component

**Location:** `frontend/src/components/projects/ProjectTypeSelector.tsx`

**Props:**
```typescript
interface ProjectTypeSelectorProps {
  selectedFlavor: FlavorType | null;
  onFlavorSelect: (flavor: FlavorType) => void;
  showDetails?: boolean;
}
```

**Features:**
- Grid layout (2x3) displaying all 6 flavors
- Visual selection state with border/background highlight
- Shows flavor icon, name, metric, and brief description
- On selection, displays IDI formula and thresholds
- Responsive: stacks to 1 column on mobile

**UI States:**
1. **Unselected**: Gray border, neutral colors
2. **Hover**: Blue border highlight, subtle background
3. **Selected**: Blue border, light blue background, checkmark indicator

### 5.2 FlavorCard Component

**Location:** `frontend/src/components/projects/FlavorCard.tsx`

**Props:**
```typescript
interface FlavorCardProps {
  flavor: FlavorSummary;
  isSelected: boolean;
  onClick: () => void;
}
```

**Structure:**
```
┌─────────────────────────────────────┐
│  [Icon]  [Badge: IoT/Cloud/etc]    │
│                                     │
│  SYNAPSE/IoT                       │
│  IoT ve gömülü sistemler için...   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ IDI = (Days × LoC/1000...)  │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### 5.3 FlavorThresholdDisplay Component

**Location:** `frontend/src/components/projects/FlavorThresholdDisplay.tsx`

**Props:**
```typescript
interface FlavorThresholdDisplayProps {
  metricName: string;
  thresholds: FlavorThresholds;
  formula: string;
}
```

**Structure:**
```
┌─────────────────────────────────────────────┐
│ IDI Thresholds (SYNAPSE/IoT defaults)       │
├──────────┬──────────┬──────────┬───────────┤
│   3.0    │   5.0    │   7.0    │   10.0    │
│ Healthy  │ Warning  │ Critical │ Quarantine│
│  (green) │ (yellow) │ (orange) │   (red)   │
├─────────────────────────────────────────────┤
│ Formula: IDI = (Days × LoC/1000 × Deps/10)  │
└─────────────────────────────────────────────┘
```

### 5.4 CreateProjectModal Component

**Location:** `frontend/src/components/projects/CreateProjectModal.tsx`

**Sections:**
1. **Basic Info**: Name, Description
2. **Flavor Selection**: ProjectTypeSelector component
3. **Threshold Preview**: FlavorThresholdDisplay component
4. **Additional Settings**: Team Lead, Target Date, Tags
5. **Quality Gates Preview**: Collapsible list of gates for selected flavor

---

## 6. Database Schema

### 6.1 Tables

```sql
-- Projects table
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    flavor_type VARCHAR(20) NOT NULL,
    team_lead_id UUID REFERENCES users(id),
    target_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    current_score DECIMAL(10,2) DEFAULT 0,
    score_status VARCHAR(20) DEFAULT 'healthy',
    custom_thresholds JSONB,
    tags TEXT[]
);

-- Project flavor configurations (cached/customized)
CREATE TABLE project_flavor_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    flavor_type VARCHAR(20) NOT NULL,
    metric_name VARCHAR(10) NOT NULL,
    formula TEXT NOT NULL,
    thresholds JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Quality gates per project
CREATE TABLE project_quality_gates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    gate_id VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    metric VARCHAR(100) NOT NULL,
    operator VARCHAR(30) NOT NULL,
    threshold JSONB NOT NULL,
    unit VARCHAR(20),
    severity VARCHAR(20) NOT NULL,
    enforcement TEXT[],
    is_enabled BOOLEAN DEFAULT TRUE,
    custom_threshold JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Quality gate results (audit trail)
CREATE TABLE quality_gate_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    gate_id VARCHAR(100) NOT NULL,
    passed BOOLEAN NOT NULL,
    actual_value JSONB NOT NULL,
    threshold JSONB NOT NULL,
    enforcement_point VARCHAR(50),
    evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    component_id UUID,
    build_id VARCHAR(100)
);

-- Neural pruning triggers
CREATE TABLE neural_pruning_triggers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    condition TEXT NOT NULL,
    action VARCHAR(50) NOT NULL,
    is_enabled BOOLEAN DEFAULT TRUE,
    last_triggered_at TIMESTAMP WITH TIME ZONE,
    trigger_count INTEGER DEFAULT 0
);

-- Indexes
CREATE INDEX idx_projects_flavor_type ON projects(flavor_type);
CREATE INDEX idx_projects_score_status ON projects(score_status);
CREATE INDEX idx_quality_gate_results_project ON quality_gate_results(project_id);
CREATE INDEX idx_quality_gate_results_gate ON quality_gate_results(gate_id);
CREATE INDEX idx_quality_gate_results_evaluated ON quality_gate_results(evaluated_at);
```

---

## 7. Implementation Steps

### Phase 1: Backend Foundation (3-4 days)
1. Create domain entities and enums
2. Implement FlavorConfigurationService with all 6 flavor templates
3. Create Quality Gate evaluation logic
4. Set up database migrations
5. Implement API endpoints for flavors and projects

### Phase 2: Frontend Components (3-4 days)
1. Create TypeScript types and interfaces
2. Implement FlavorCard component with styling
3. Implement ProjectTypeSelector component
4. Implement FlavorThresholdDisplay component
5. Update CreateProjectModal with flavor selection

### Phase 3: Integration (2-3 days)
1. Connect frontend to backend APIs
2. Implement flavor selection state management
3. Add loading states and error handling
4. Implement real-time threshold preview on selection

### Phase 4: Quality Gates Integration (2-3 days)
1. Display quality gates for selected flavor
2. Allow enabling/disabling individual gates
3. Implement custom threshold overrides
4. Add gate evaluation indicators in project dashboard

### Phase 5: Testing & Polish (2-3 days)
1. Unit tests for backend services
2. Component tests for React components
3. E2E tests for project creation flow
4. UI/UX polish and accessibility improvements

---

## 8. Acceptance Criteria

### 8.1 Functional Requirements
- [ ] User can view all 6 SYNAPSE flavors with descriptions
- [ ] User can select a flavor when creating a new project
- [ ] Selected flavor's IDI formula is displayed
- [ ] Selected flavor's thresholds are displayed
- [ ] Project is created with correct flavor configuration
- [ ] Quality gates are automatically assigned based on flavor
- [ ] User can view quality gates for selected flavor before creation
- [ ] Custom thresholds can be set (optional)

### 8.2 Non-Functional Requirements
- [ ] Flavor selection response time < 100ms
- [ ] Project creation response time < 500ms
- [ ] Mobile-responsive design
- [ ] WCAG 2.1 AA accessibility compliance
- [ ] Support for Turkish and English languages

### 8.3 Test Scenarios
1. **Happy Path**: Select IoT flavor → View thresholds → Create project → Verify gates
2. **Flavor Switch**: Select Cloud → Switch to Embedded → Verify thresholds update
3. **Custom Thresholds**: Select Infra → Override CDI thresholds → Verify saved
4. **Validation**: Try to create without selecting flavor → See error message
5. **Mobile**: Complete flow on mobile device → Verify responsive layout

---

## 9. Example Implementation Code

### 9.1 FlavorCard.tsx

```tsx
import React from 'react';
import { FlavorSummary } from '../../types/flavor';

interface FlavorCardProps {
  flavor: FlavorSummary;
  isSelected: boolean;
  onClick: () => void;
}

const flavorIcons: Record<string, string> = {
  iot: 'fa-microchip',
  cloud: 'fa-cloud',
  embedded: 'fa-cog',
  infra: 'fa-server',
  data: 'fa-database',
  mobile: 'fa-mobile-alt',
};

const flavorColors: Record<string, string> = {
  iot: 'from-sky-500 to-sky-600',
  cloud: 'from-purple-500 to-purple-600',
  embedded: 'from-amber-500 to-amber-600',
  infra: 'from-emerald-500 to-emerald-600',
  data: 'from-pink-500 to-pink-600',
  mobile: 'from-indigo-500 to-indigo-600',
};

export const FlavorCard: React.FC<FlavorCardProps> = ({
  flavor,
  isSelected,
  onClick,
}) => {
  return (
    <div
      className={`
        flavor-card p-4 rounded-xl border-2 cursor-pointer transition-all duration-200
        ${isSelected
          ? 'border-sky-500 bg-sky-50 shadow-lg'
          : 'border-gray-200 hover:border-sky-300 hover:bg-gray-50'
        }
      `}
      onClick={onClick}
      role="button"
      aria-pressed={isSelected}
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && onClick()}
    >
      {/* Header */}
      <div className="flex items-center gap-3 mb-3">
        <div className={`
          w-10 h-10 rounded-lg flex items-center justify-center
          bg-gradient-to-br ${flavorColors[flavor.type]}
        `}>
          <i className={`fas ${flavorIcons[flavor.type]} text-white`} />
        </div>
        <span className={`
          px-2 py-1 rounded text-xs font-semibold uppercase text-white
          bg-gradient-to-r ${flavorColors[flavor.type]}
        `}>
          {flavor.type}
        </span>
        {isSelected && (
          <i className="fas fa-check-circle text-sky-500 ml-auto" />
        )}
      </div>

      {/* Title & Description */}
      <h3 className="font-semibold text-gray-900 mb-1">{flavor.name}</h3>
      <p className="text-sm text-gray-600 mb-3">{flavor.description}</p>

      {/* Formula */}
      <div className="bg-gray-100 rounded-lg px-3 py-2">
        <code className="text-xs text-gray-700">
          {flavor.metricName} = {flavor.formula.split('/')[0]}...
        </code>
      </div>

      {/* Stats */}
      <div className="flex items-center gap-4 mt-3 text-xs text-gray-500">
        <span>
          <i className="fas fa-shield-alt mr-1" />
          {flavor.qualityGatesCount} gates
        </span>
        <span>
          <i className="fas fa-tags mr-1" />
          {flavor.categories.length} categories
        </span>
      </div>
    </div>
  );
};
```

### 9.2 Backend Service (C#)

```csharp
// FlavorConfigurationService.cs
public class FlavorConfigurationService : IFlavorConfigurationService
{
    private readonly Dictionary<FlavorType, FlavorConfig> _flavorConfigs;

    public FlavorConfigurationService()
    {
        _flavorConfigs = InitializeFlavorConfigs();
    }

    public FlavorConfig GetFlavorConfig(FlavorType flavorType)
    {
        return _flavorConfigs.TryGetValue(flavorType, out var config)
            ? config
            : throw new ArgumentException($"Unknown flavor type: {flavorType}");
    }

    public IEnumerable<FlavorSummary> GetAllFlavorSummaries()
    {
        return _flavorConfigs.Values.Select(c => new FlavorSummary
        {
            Type = c.Type,
            Name = c.Name,
            Description = c.Description,
            MetricName = c.MetricName,
            Formula = c.Formula,
            Thresholds = c.Thresholds,
            QualityGatesCount = c.QualityGates.Count,
            Categories = c.QualityGates.Select(g => g.Category).Distinct().ToList()
        });
    }

    public decimal CalculateScore(FlavorType flavorType, ScoreInputs inputs)
    {
        return flavorType switch
        {
            FlavorType.IoT => CalculateIoTIDI(inputs),
            FlavorType.Cloud => CalculateCloudIDI(inputs),
            FlavorType.Embedded => CalculateEmbeddedIDI(inputs),
            FlavorType.Infra => CalculateInfraCDI(inputs),
            FlavorType.Data => CalculateDataSDI(inputs),
            FlavorType.Mobile => CalculateMobileIDI(inputs),
            _ => throw new ArgumentException($"Unknown flavor: {flavorType}")
        };
    }

    private decimal CalculateIoTIDI(ScoreInputs inputs)
    {
        return (inputs.Days * (inputs.LocChanged / 1000m) * (inputs.Dependencies / 10m)) / 10m;
    }

    private decimal CalculateCloudIDI(ScoreInputs inputs)
    {
        return (inputs.PrAgeDays * inputs.ChangedFiles * inputs.DependentServices) / 100m;
    }

    // ... other calculation methods
}
```

---

## 10. Notes for Implementation

1. **Performance**: Cache flavor configurations in memory - they don't change frequently
2. **Localization**: All strings should use i18n keys for Turkish/English support
3. **Accessibility**: Ensure keyboard navigation works for flavor selection
4. **Mobile**: Test thoroughly on iOS Safari and Chrome Android
5. **Validation**: Prevent project creation without flavor selection
6. **Telemetry**: Log flavor selection analytics for product insights

---

*Document maintained by: SYNAPSE Platform Team*
*Last updated: 2026-01-20*
