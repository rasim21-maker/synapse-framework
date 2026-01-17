namespace SynapsePlatform.Core.Enums;

/// <summary>
/// SYNAPSE Capability Maturity Model Levels
/// </summary>
public enum SCMMLevel
{
    Level0_Manual = 0,      // Startups <15 people - Excel, Git
    Level1_Instrumented = 1, // Growing teams (15-50) - CI/CD, Docker
    Level2_Automated = 2,    // Established teams (50-200) - Policy-as-code
    Level3_Predictive = 3,   // Large orgs (200+) - ML-based risk forecasting
    Level4_Adaptive = 4      // Enterprise portfolios (1000+) - Autonomous
}

/// <summary>
/// Project phases in SYNAPSE methodology
/// </summary>
public enum ProjectPhase
{
    Initiation,
    Discovery,
    Architecture,
    Development,
    Integration,
    Validation,
    Deployment,
    Operations,
    Closure
}

/// <summary>
/// Work item types
/// </summary>
public enum WorkItemType
{
    Epic,
    Feature,
    UserStory,
    Task,
    Bug,
    Spike,
    TechnicalDebt,
    IntegrationTask
}

/// <summary>
/// Work item status
/// </summary>
public enum WorkItemStatus
{
    Backlog,
    ToDo,
    InProgress,
    InReview,
    Testing,
    Done,
    Blocked,
    Cancelled
}

/// <summary>
/// Priority levels
/// </summary>
public enum Priority
{
    Critical = 1,
    High = 2,
    Medium = 3,
    Low = 4
}

/// <summary>
/// Component types in SYNAPSE Digital Twin architecture
/// </summary>
public enum ComponentType
{
    Hardware,
    Firmware,
    Software,
    Infrastructure,
    Cloud,
    Edge
}

/// <summary>
/// Digital Twin layer types
/// </summary>
public enum DigitalTwinLayer
{
    Hardware,      // SPICE models, thermal FEA
    Firmware,      // Virtual MCU (QEMU/Renode)
    Software,      // Docker environments
    Infrastructure // Kubernetes, service mesh
}

/// <summary>
/// Quality gate enforcement types
/// </summary>
public enum QualityGateEnforcement
{
    PreCommitHook,
    BuildPipeline,
    PullRequest,
    Deployment,
    Manual
}

/// <summary>
/// Quality gate action types
/// </summary>
public enum QualityGateAction
{
    Warn,
    RejectCommit,
    BlockMerge,
    BlockDeployment,
    NotifyStakeholders
}

/// <summary>
/// IDI (Integration Debt Index) health status
/// </summary>
public enum IDIHealthStatus
{
    Healthy,    // IDI < 3.0
    Warning,    // IDI 3.0-5.0
    Critical    // IDI > 5.0 - Mandatory integration
}

/// <summary>
/// User roles in SYNAPSE platform
/// </summary>
public enum UserRole
{
    SystemAdmin,
    PortfolioManager,
    ProjectManager,
    TechLead,
    Developer,
    QAEngineer,
    SteeringCommitteeMember,
    Stakeholder,
    Viewer
}

/// <summary>
/// Project archetype
/// </summary>
public enum ProjectArchetype
{
    IoTEcosystem,
    EmbeddedSystem,
    HardwareSoftware,
    SaaSWithHardware,
    MultiDisciplinary,
    PureSoftware,
    PureHardware
}

/// <summary>
/// Risk level
/// </summary>
public enum RiskLevel
{
    VeryLow = 1,
    Low = 2,
    Medium = 3,
    High = 4,
    VeryHigh = 5
}

/// <summary>
/// Risk status
/// </summary>
public enum RiskStatus
{
    Identified,
    Analyzing,
    Mitigating,
    Monitoring,
    Closed,
    Occurred
}
