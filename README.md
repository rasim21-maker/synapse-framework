# SYNAPSE Platform

A web-based project management tool implementing the SYNAPSE Framework methodology for hardware-software co-design projects, IoT ecosystems, and complex multi-disciplinary systems.

## Features

- **Project Management**: Create and manage projects with SYNAPSE phases
- **Integration Debt Index (IDI)**: Real-time tracking of integration health
- **Quality Gates**: Policy-as-Code enforcement for physical constraints
- **Sprint Management**: Agile sprint planning and tracking
- **Component Management**: Hardware, Firmware, Software layer tracking
- **Digital Twin Support**: Simulation-to-reality accuracy tracking

## Technology Stack

- **Backend**: .NET 8 Web API
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Database**: PostgreSQL 16
- **Containerization**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Docker & Docker Compose
- .NET 8 SDK (for local development)
- Node.js 20+ (for local development)

### Run with Docker

```bash
docker-compose up -d
```

Access:
- Web UI: http://localhost:5173
- API: http://localhost:5000
- Swagger: http://localhost:5000/swagger

### Local Development

**Backend:**
```bash
cd src/SynapsePlatform.Api
dotnet restore
dotnet run
```

**Frontend:**
```bash
cd src/SynapsePlatform.Web/synapse-ui
npm install
npm run dev
```

## Project Structure

```
synapse-framework/
├── src/
│   ├── SynapsePlatform.Api/        # .NET 8 Web API
│   ├── SynapsePlatform.Core/       # Domain entities & interfaces
│   ├── SynapsePlatform.Infrastructure/  # Data access & services
│   └── SynapsePlatform.Web/
│       └── synapse-ui/             # React frontend
├── docker-compose.yml
└── SynapsePlatform.sln
```

## SYNAPSE Methodology

### Integration Debt Index (IDI)

```
IDI = (Days Since Last Integration) × (LoC Changed / 1000) × (Dependencies / 10)
```

- IDI < 3.0: ✅ Healthy
- IDI 3.0-5.0: ⚠️ Warning
- IDI > 5.0: 🚨 Critical - Mandatory integration required

### SCMM Maturity Levels

| Level | Name | Description |
|-------|------|-------------|
| 0 | Manual | Excel, Git, manual processes |
| 1 | Instrumented | CI/CD, basic dashboards |
| 2 | Automated | Policy-as-code, digital twin |
| 3 | Predictive | ML-based risk forecasting |
| 4 | Adaptive | Autonomous orchestration |

## License

CC BY-SA 4.0
