namespace SynapsePlatform.Core.Enums;

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

public enum ProjectArchetype
{
    IoTEcosystem,
    EmbeddedSystem,
    HardwareSoftware,
    SaaSWithHardware,
    MultiDisciplinary,
    PureSoftware
}

public enum ComponentType
{
    Hardware,
    Firmware,
    Software,
    Infrastructure,
    Cloud,
    Edge
}

public enum WorkItemType
{
    Epic,
    Feature,
    UserStory,
    Task,
    Bug,
    TechnicalDebt,
    Spike,
    IntegrationTask
}

public enum WorkItemStatus
{
    New,
    Ready,
    InProgress,
    InReview,
    Testing,
    Done,
    Blocked,
    Cancelled
}

public enum Priority
{
    Critical,
    High,
    Medium,
    Low
}

public enum IDIStatus
{
    Healthy,    // IDI < 3.0
    Warning,    // IDI 3.0-5.0
    Critical    // IDI > 5.0
}

public enum QualityGateEnforcement
{
    PreCommitHook,
    BuildPipeline,
    PullRequest,
    Manual
}

public enum QualityGateAction
{
    Warn,
    RejectCommit,
    FailBuild,
    BlockMerge,
    NotifyOnly
}

public enum RiskLevel
{
    VeryLow,
    Low,
    Medium,
    High,
    VeryHigh
}

public enum RiskStatus
{
    Identified,
    Analyzing,
    Mitigating,
    Monitoring,
    Resolved,
    Accepted,
    Occurred
}

public enum UserRole
{
    Admin,
    PortfolioManager,
    ProjectManager,
    TeamLead,
    Developer,
    Tester,
    SteeringCommittee,
    Stakeholder,
    Viewer
}

public enum DigitalTwinLayer
{
    Hardware,
    Firmware,
    Software,
    Infrastructure
}

public enum MaturityLevel
{
    Level0_Manual = 0,
    Level1_Instrumented = 1,
    Level2_Automated = 2,
    Level3_Predictive = 3,
    Level4_Adaptive = 4
}
