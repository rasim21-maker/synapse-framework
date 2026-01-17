using SynapsePlatform.Core.Enums;

namespace SynapsePlatform.Api.DTOs;

// Organization DTOs
public record CreateOrganizationDto(
    string Name,
    string? Description,
    string? Industry,
    int EmployeeCount
);

public record OrganizationDto(
    Guid Id,
    string Name,
    string? Description,
    SCMMLevel MaturityLevel,
    string? Industry,
    int EmployeeCount,
    int PortfolioCount,
    int ProjectCount
);

// Portfolio DTOs
public record CreatePortfolioDto(
    string Name,
    string? Description,
    string? Code,
    decimal? Budget,
    Guid OrganizationId,
    Guid? PortfolioManagerId
);

public record PortfolioDto(
    Guid Id,
    string Name,
    string? Description,
    string? Code,
    decimal? Budget,
    int ProjectCount,
    string? PortfolioManagerName
);

// Project DTOs
public record CreateProjectDto(
    string Name,
    string? Code,
    string? Description,
    ProjectArchetype Archetype,
    SCMMLevel TargetMaturityLevel,
    DateTime? PlannedStartDate,
    DateTime? PlannedEndDate,
    decimal? PlannedBudget,
    Guid PortfolioId,
    Guid? ProjectManagerId,
    Guid? TechLeadId
);

public record UpdateProjectDto(
    string Name,
    string? Description,
    ProjectPhase CurrentPhase,
    DateTime? PlannedStartDate,
    DateTime? PlannedEndDate,
    decimal? PlannedBudget,
    decimal? ActualBudget,
    double MaxAllowedIDI
);

public record ProjectDto(
    Guid Id,
    string Name,
    string Code,
    string? Description,
    ProjectArchetype Archetype,
    ProjectPhase CurrentPhase,
    SCMMLevel TargetMaturityLevel,
    DateTime? PlannedStartDate,
    DateTime? PlannedEndDate,
    double CurrentIDI,
    IDIHealthStatus IDIStatus,
    decimal? PlannedBudget,
    decimal? ActualBudget,
    string? ProjectManagerName,
    int ComponentCount,
    int WorkItemCount
);

// Component DTOs
public record CreateComponentDto(
    string Name,
    string? Description,
    ComponentType Type,
    string? RepositoryUrl,
    Guid ProjectId,
    Guid? OwnerTeamId,
    double? PowerBudgetWatts,
    double? ThermalLimitCelsius,
    double? LatencyThresholdMs,
    double? MemoryLimitMB
);

public record ComponentDto(
    Guid Id,
    string Name,
    string? Description,
    ComponentType Type,
    bool IsIntegrated,
    DateTime? LastIntegrationDate,
    int LinesOfCodeChanged,
    double ComponentIDI,
    IDIHealthStatus IDIStatus
);

// WorkItem DTOs
public record CreateWorkItemDto(
    string Title,
    string? Description,
    WorkItemType Type,
    Priority Priority,
    double? EstimatedHours,
    int? StoryPoints,
    DateTime? DueDate,
    string? AcceptanceCriteria,
    string? Tags,
    Guid ProjectId,
    Guid? SprintId,
    Guid? ComponentId,
    Guid? AssigneeId,
    Guid? ParentWorkItemId
);

public record UpdateWorkItemDto(
    string Title,
    string? Description,
    WorkItemStatus Status,
    Priority Priority,
    double? EstimatedHours,
    double? ActualHours,
    int? StoryPoints,
    DateTime? DueDate,
    int ProgressPercentage,
    string? AcceptanceCriteria,
    string? Tags,
    Guid? SprintId,
    Guid? ComponentId,
    Guid? AssigneeId
);

public record WorkItemDto(
    Guid Id,
    string Code,
    string Title,
    string? Description,
    WorkItemType Type,
    WorkItemStatus Status,
    Priority Priority,
    double? EstimatedHours,
    double? ActualHours,
    int? StoryPoints,
    DateTime? DueDate,
    int ProgressPercentage,
    string? AssigneeName,
    string? SprintName,
    string? ComponentName,
    int ChildCount,
    int CommentCount
);

// Sprint DTOs
public record CreateSprintDto(
    string? Name,
    string? Goal,
    DateTime StartDate,
    DateTime EndDate,
    int PlannedCapacityHours,
    Guid ProjectId
);

public record SprintDto(
    Guid Id,
    string Name,
    string? Goal,
    int SprintNumber,
    DateTime StartDate,
    DateTime EndDate,
    bool IsActive,
    bool IsCompleted,
    int PlannedStoryPoints,
    int CompletedStoryPoints,
    int WorkItemCount
);

// Quality Gate DTOs
public record CreateQualityGateDto(
    string Name,
    string? Description,
    string Category,
    double? ThresholdValue,
    string? ThresholdUnit,
    string ThresholdOperator,
    QualityGateEnforcement Enforcement,
    QualityGateAction Action,
    string? PolicyYaml,
    Guid ProjectId,
    Guid? ComponentId
);

public record QualityGateDto(
    Guid Id,
    string Name,
    string? Description,
    string Category,
    double? ThresholdValue,
    string? ThresholdUnit,
    QualityGateEnforcement Enforcement,
    QualityGateAction Action,
    bool IsEnabled,
    bool? LastCheckPassed,
    DateTime? LastCheckedAt
);

// Integration DTOs
public record RecordIntegrationDto(
    Guid ProjectId,
    List<Guid> ComponentIds,
    string? Description
);

public record IntegrationRecordDto(
    Guid Id,
    DateTime IntegrationDate,
    double IDIBeforeIntegration,
    double IDIAfterIntegration,
    int ComponentsIntegrated,
    int LinesOfCodeIntegrated,
    bool WasSuccessful,
    string? PerformedByName
);

// Dashboard DTOs
public record ProjectDashboardDto(
    ProjectDto Project,
    double CurrentIDI,
    IDIHealthStatus IDIStatus,
    int TotalWorkItems,
    int CompletedWorkItems,
    int BlockedWorkItems,
    int OverdueWorkItems,
    int ActiveRisks,
    int FailedQualityGates,
    SprintDto? ActiveSprint,
    double BudgetUtilization,
    int DaysRemaining
);

// Comment DTOs
public record CreateCommentDto(
    string Content,
    Guid WorkItemId,
    Guid? ParentCommentId
);

public record CommentDto(
    Guid Id,
    string Content,
    DateTime CreatedAt,
    bool IsEdited,
    string AuthorName,
    string? AuthorAvatarUrl,
    int ReplyCount
);

// Checklist DTOs
public record CreateChecklistDto(
    string Title,
    Guid WorkItemId,
    List<string> Items
);

public record ChecklistDto(
    Guid Id,
    string Title,
    List<ChecklistItemDto> Items,
    int CompletedCount,
    int TotalCount
);

public record ChecklistItemDto(
    Guid Id,
    string Content,
    bool IsCompleted,
    DateTime? CompletedAt
);

// Team DTOs
public record CreateTeamDto(
    string Name,
    string? Description,
    string? Specialty,
    int DefaultCapacityHoursPerSprint,
    Guid OrganizationId,
    Guid? TeamLeadId
);

public record TeamDto(
    Guid Id,
    string Name,
    string? Description,
    string? Specialty,
    string? TeamLeadName,
    int MemberCount
);

// Risk DTOs
public record CreateRiskDto(
    string Title,
    string? Description,
    string? Category,
    RiskLevel Probability,
    RiskLevel Impact,
    string? MitigationPlan,
    string? ContingencyPlan,
    DateTime? MitigationDeadline,
    Guid ProjectId,
    Guid? OwnerId
);

public record RiskDto(
    Guid Id,
    string Title,
    string? Description,
    string? Category,
    RiskLevel Probability,
    RiskLevel Impact,
    int RiskScore,
    RiskStatus Status,
    string? OwnerName,
    DateTime? MitigationDeadline
);
