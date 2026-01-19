using SynapsePlatform.Core.Enums;

namespace SynapsePlatform.Api.DTOs;

// Project DTOs
public record ProjectDto(
    Guid Id,
    string Name,
    string Code,
    string? Description,
    ProjectArchetype Archetype,
    ProjectPhase CurrentPhase,
    MaturityLevel TargetMaturityLevel,
    DateTime PlannedStartDate,
    DateTime PlannedEndDate,
    double CurrentIDI,
    IDIStatus IDIStatus,
    double PlannedBudget,
    double ActualBudget,
    string? ProjectManagerName,
    int ComponentCount,
    int WorkItemCount
);

public record CreateProjectDto(
    string Name,
    string Code,
    string? Description,
    ProjectArchetype Archetype,
    MaturityLevel TargetMaturityLevel,
    DateTime PlannedStartDate,
    DateTime PlannedEndDate,
    double PlannedBudget,
    Guid? PortfolioId,
    Guid? ProjectManagerId
);

// Sprint DTOs
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

public record CreateSprintDto(
    string? Name,
    string? Goal,
    DateTime StartDate,
    DateTime EndDate,
    double? PlannedCapacityHours,
    Guid ProjectId
);

// WorkItem DTOs
public record WorkItemDto(
    Guid Id,
    string Title,
    string? Description,
    WorkItemType Type,
    WorkItemStatus Status,
    Priority Priority,
    int? StoryPoints,
    double? EstimatedHours,
    DateTime? DueDate,
    Guid ProjectId,
    Guid? SprintId,
    string? AssigneeName,
    string? ComponentName
);

public record CreateWorkItemDto(
    string Title,
    string? Description,
    WorkItemType Type,
    Priority Priority,
    int? StoryPoints,
    double? EstimatedHours,
    DateTime? DueDate,
    string? AcceptanceCriteria,
    Guid ProjectId,
    Guid? SprintId,
    Guid? AssigneeId,
    Guid? ParentWorkItemId,
    Guid? ComponentId
);

// Component DTOs
public record ComponentDto(
    Guid Id,
    string Name,
    string? Description,
    ComponentType Type,
    double ComponentIDI,
    IDIStatus IDIStatus,
    int DaysSinceLastIntegration,
    DateTime? LastIntegrationDate,
    int LinesOfCodeChanged,
    int DependencyCount,
    double? PowerBudgetWatts,
    double? ActualPowerWatts
);

public record CreateComponentDto(
    string Name,
    string? Description,
    ComponentType Type,
    Guid ProjectId,
    double? PowerBudgetWatts,
    double? LatencyThresholdMs,
    double? MemoryLimitMB
);

// IDI DTOs
public record IDIReportDto(
    double ProjectIDI,
    IDIStatus Status,
    IEnumerable<ComponentIDIDto> Components,
    IEnumerable<IDITrendDto> Trends
);

public record ComponentIDIDto(
    Guid ComponentId,
    string ComponentName,
    double IDI,
    IDIStatus Status,
    int DaysSinceLastIntegration
);

public record IDITrendDto(DateTime Date, double IDI);
